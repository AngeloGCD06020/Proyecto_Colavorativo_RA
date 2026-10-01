using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem.EnhancedTouch;
using UnityEngine.UI;
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;

public class RaycastController : MonoBehaviour
{
    enum PlacementPlaneKind
    {
        Horizontal,
        Vertical
    }

    [Header("AR")]
    [SerializeField] ARRaycastManager raycastManager;
    [SerializeField] ARPlaneManager planeManager;

    [Header("Modelos")]
    [SerializeField] GameObject horizontalModelPrefab;
    [SerializeField] GameObject verticalModelPrefab;
    [SerializeField] Vector3 horizontalEulerOffset;
    [SerializeField] Vector3 verticalEulerOffset;
    [SerializeField] float placedModelScale = 0.18f;

    [Header("UI")]
    [SerializeField] TMP_Text statusText;

    readonly List<ARRaycastHit> hits = new();
    readonly HashSet<TrackableId> configuredPlanes = new();

    PlacementPlaneKind selectedPlaneKind = PlacementPlaneKind.Horizontal;
    Button horizontalButton;
    Button verticalButton;
    TMP_Text selectedModelText;
    Camera arCamera;
    bool horizontalDetected;
    bool verticalDetected;
    Material fallbackHorizontalMaterial;
    Material fallbackVerticalMaterial;
    Material fallbackTopMaterial;
    Material fallbackBottomMaterial;

    void Awake()
    {
        if (raycastManager == null)
            raycastManager = FindFirstObjectByType<ARRaycastManager>();

        if (planeManager == null)
            planeManager = FindFirstObjectByType<ARPlaneManager>();

        arCamera = Camera.main;
        EnsureRuntimeUi();
        SelectModel(PlacementPlaneKind.Horizontal);
        ShowStatus("Escaneando entorno ...");
    }

    void OnEnable()
    {
        EnhancedTouchSupport.Enable();

        if (planeManager != null)
            planeManager.trackablesChanged.AddListener(OnPlanesChanged);
    }

    void OnDisable()
    {
        if (planeManager != null)
            planeManager.trackablesChanged.RemoveListener(OnPlanesChanged);

        EnhancedTouchSupport.Disable();
    }

    void Update()
    {
        var activeTouches = UnityEngine.InputSystem.EnhancedTouch.Touch.activeTouches;

        if (activeTouches.Count == 0)
            return;

        var touch = activeTouches[0];

        if (touch.phase != UnityEngine.InputSystem.TouchPhase.Began)
            return;

        if (EventSystem.current != null && EventSystem.current.IsPointerOverGameObject(touch.touchId))
            return;

        TryPlaceSelectedModel(touch.screenPosition);
    }

    void OnPlanesChanged(ARTrackablesChangedEventArgs<ARPlane> args)
    {
        foreach (var plane in args.added)
            ConfigurePlane(plane, true);

        foreach (var plane in args.updated)
            ConfigurePlane(plane, false);
    }

    void ConfigurePlane(ARPlane plane, bool isNewPlane)
    {
        if (plane == null)
            return;

        var label = plane.GetComponent<ARPlaneDimensionLabel>();
        if (label == null)
            label = plane.gameObject.AddComponent<ARPlaneDimensionLabel>();

        label.Configure(arCamera != null ? arCamera : Camera.main);
        label.Refresh();

        if (!isNewPlane && configuredPlanes.Contains(plane.trackableId))
            return;

        configuredPlanes.Add(plane.trackableId);

        if (plane.alignment.IsHorizontal() && !horizontalDetected)
        {
            horizontalDetected = true;
            ShowStatus("Superficie horizontal detectada!");
        }
        else if (plane.alignment.IsVertical() && !verticalDetected)
        {
            verticalDetected = true;
            ShowStatus("Superficie vertical detectada!");
        }
    }

    void TryPlaceSelectedModel(Vector2 screenPosition)
    {
        if (raycastManager == null || planeManager == null)
        {
            ShowStatus("Escaneando entorno ...");
            return;
        }

        if (!raycastManager.Raycast(screenPosition, hits, TrackableType.PlaneWithinPolygon))
        {
            ShowStatus("Escaneando entorno ...");
            return;
        }

        var hit = hits[0];
        var plane = planeManager.GetPlane(hit.trackableId);

        if (plane == null)
        {
            ShowStatus("Escaneando entorno ...");
            return;
        }

        if (!TryGetPlaneKind(plane, out var hitPlaneKind))
        {
            ShowStatus("Escaneando entorno ...");
            return;
        }

        if (hitPlaneKind != selectedPlaneKind)
        {
            ShowStatus(selectedPlaneKind == PlacementPlaneKind.Horizontal
                ? "El modelo horizontal solo puede colocarse en planos horizontales"
                : "El modelo vertical solo puede colocarse en planos verticales");
            return;
        }

        var prefab = selectedPlaneKind == PlacementPlaneKind.Horizontal ? horizontalModelPrefab : verticalModelPrefab;
        var offset = selectedPlaneKind == PlacementPlaneKind.Horizontal ? horizontalEulerOffset : verticalEulerOffset;
        var rotation = hit.pose.rotation * Quaternion.Euler(offset);

        GameObject instance = prefab != null
            ? Instantiate(prefab, hit.pose.position, rotation)
            : CreateFallbackModel(selectedPlaneKind, hit.pose.position, rotation);

        instance.name = selectedPlaneKind == PlacementPlaneKind.Horizontal
            ? "Modelo horizontal colocado"
            : "Modelo vertical colocado";
        instance.transform.localScale = Vector3.one * placedModelScale;
        instance.SetActive(true);

        ShowStatus(selectedPlaneKind == PlacementPlaneKind.Horizontal
            ? "Objeto colocado en plano horizontal"
            : "Objeto colocado en plano vertical");
    }

    static bool TryGetPlaneKind(ARPlane plane, out PlacementPlaneKind planeKind)
    {
        if (plane.alignment.IsHorizontal())
        {
            planeKind = PlacementPlaneKind.Horizontal;
            return true;
        }

        if (plane.alignment.IsVertical())
        {
            planeKind = PlacementPlaneKind.Vertical;
            return true;
        }

        planeKind = PlacementPlaneKind.Horizontal;
        return false;
    }

    void EnsureRuntimeUi()
    {
        EnsureEventSystem();

        var canvasObject = new GameObject("Parcial UI");
        var canvas = canvasObject.AddComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        canvas.sortingOrder = 20;
        canvasObject.AddComponent<GraphicRaycaster>();

        var scaler = canvasObject.AddComponent<CanvasScaler>();
        scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
        scaler.referenceResolution = new Vector2(1080f, 1920f);
        scaler.matchWidthOrHeight = 0.5f;

        if (statusText == null)
            statusText = CreateStatusLabel(canvasObject.transform);

        selectedModelText = CreateSelectedModelLabel(canvasObject.transform);

        var buttonRow = CreatePanel("Selector de modelos", canvasObject.transform, new Vector2(0.5f, 0f), new Vector2(0.5f, 0f), new Vector2(0.5f, 0f));
        var rowRect = buttonRow.GetComponent<RectTransform>();
        rowRect.anchoredPosition = new Vector2(0f, 72f);
        rowRect.sizeDelta = new Vector2(900f, 150f);

        var layout = buttonRow.AddComponent<HorizontalLayoutGroup>();
        layout.spacing = 24f;
        layout.padding = new RectOffset(20, 20, 20, 20);
        layout.childControlHeight = true;
        layout.childControlWidth = true;
        layout.childForceExpandHeight = true;
        layout.childForceExpandWidth = true;

        horizontalButton = CreateSelectionButton(buttonRow.transform, "Modelo horizontal\nSolo pisos/mesas", () => SelectModel(PlacementPlaneKind.Horizontal));
        verticalButton = CreateSelectionButton(buttonRow.transform, "Modelo vertical\nSolo paredes", () => SelectModel(PlacementPlaneKind.Vertical));
    }

    static void EnsureEventSystem()
    {
        if (EventSystem.current != null)
            return;

        var eventSystemObject = new GameObject("EventSystem");
        eventSystemObject.AddComponent<EventSystem>();
        eventSystemObject.AddComponent<UnityEngine.InputSystem.UI.InputSystemUIInputModule>();
    }

    TMP_Text CreateStatusLabel(Transform canvasTransform)
    {
        var panel = CreatePanel("Estado", canvasTransform, new Vector2(0.5f, 1f), new Vector2(0.5f, 1f), new Vector2(0.5f, 1f));
        var panelRect = panel.GetComponent<RectTransform>();
        panelRect.anchoredPosition = new Vector2(0f, -74f);
        panelRect.sizeDelta = new Vector2(920f, 100f);

        var text = CreateText("Texto Estado", panel.transform, 35f, FontStyles.Bold);
        text.alignment = TextAlignmentOptions.Center;
        text.rectTransform.anchorMin = Vector2.zero;
        text.rectTransform.anchorMax = Vector2.one;
        text.rectTransform.offsetMin = new Vector2(20f, 12f);
        text.rectTransform.offsetMax = new Vector2(-20f, -12f);
        return text;
    }

    TMP_Text CreateSelectedModelLabel(Transform canvasTransform)
    {
        var text = CreateText("Modelo Seleccionado", canvasTransform, 28f, FontStyles.Bold);
        text.alignment = TextAlignmentOptions.Center;
        text.rectTransform.anchorMin = new Vector2(0.5f, 0f);
        text.rectTransform.anchorMax = new Vector2(0.5f, 0f);
        text.rectTransform.pivot = new Vector2(0.5f, 0f);
        text.rectTransform.anchoredPosition = new Vector2(0f, 230f);
        text.rectTransform.sizeDelta = new Vector2(880f, 64f);
        return text;
    }

    static GameObject CreatePanel(string name, Transform parent, Vector2 anchorMin, Vector2 anchorMax, Vector2 pivot)
    {
        var panel = new GameObject(name);
        panel.transform.SetParent(parent, false);

        var rect = panel.AddComponent<RectTransform>();
        rect.anchorMin = anchorMin;
        rect.anchorMax = anchorMax;
        rect.pivot = pivot;

        var image = panel.AddComponent<Image>();
        image.color = new Color(0.02f, 0.025f, 0.03f, 0.78f);
        return panel;
    }

    Button CreateSelectionButton(Transform parent, string label, UnityEngine.Events.UnityAction onClick)
    {
        var buttonObject = new GameObject(label.Replace("\n", " "));
        buttonObject.transform.SetParent(parent, false);

        var image = buttonObject.AddComponent<Image>();
        var button = buttonObject.AddComponent<Button>();
        button.targetGraphic = image;
        button.onClick.AddListener(onClick);

        var layoutElement = buttonObject.AddComponent<LayoutElement>();
        layoutElement.minHeight = 96f;
        layoutElement.preferredHeight = 110f;

        var text = CreateText("Etiqueta", buttonObject.transform, 25f, FontStyles.Bold);
        text.text = label;
        text.alignment = TextAlignmentOptions.Center;
        text.rectTransform.anchorMin = Vector2.zero;
        text.rectTransform.anchorMax = Vector2.one;
        text.rectTransform.offsetMin = new Vector2(18f, 8f);
        text.rectTransform.offsetMax = new Vector2(-18f, -8f);

        return button;
    }

    static TMP_Text CreateText(string name, Transform parent, float fontSize, FontStyles style)
    {
        var textObject = new GameObject(name);
        textObject.transform.SetParent(parent, false);

        var text = textObject.AddComponent<TextMeshProUGUI>();
        text.fontSize = fontSize;
        text.fontStyle = style;
        text.color = Color.white;
        text.textWrappingMode = TextWrappingModes.Normal;
        text.overflowMode = TextOverflowModes.Ellipsis;
        return text;
    }

    void SelectModel(PlacementPlaneKind planeKind)
    {
        selectedPlaneKind = planeKind;

        if (selectedModelText != null)
            selectedModelText.text = planeKind == PlacementPlaneKind.Horizontal
                ? "Seleccionado: modelo para plano horizontal"
                : "Seleccionado: modelo para plano vertical";

        UpdateButtonVisuals();
    }

    void UpdateButtonVisuals()
    {
        SetButtonColor(horizontalButton, selectedPlaneKind == PlacementPlaneKind.Horizontal, new Color(1f, 0.88f, 0.2f, 0.95f));
        SetButtonColor(verticalButton, selectedPlaneKind == PlacementPlaneKind.Vertical, new Color(0.18f, 0.38f, 1f, 0.95f));
    }

    static void SetButtonColor(Button button, bool selected, Color accent)
    {
        if (button == null)
            return;

        var image = button.GetComponent<Image>();
        if (image != null)
            image.color = selected ? accent : new Color(0.12f, 0.13f, 0.15f, 0.92f);

        var label = button.GetComponentInChildren<TMP_Text>();
        if (label != null)
            label.color = selected ? Color.black : Color.white;
    }

    void ShowStatus(string message)
    {
        if (statusText != null)
            statusText.text = message;
    }

    GameObject CreateFallbackModel(PlacementPlaneKind planeKind, Vector3 position, Quaternion rotation)
    {
        EnsureFallbackMaterials();

        var root = new GameObject("Modelo generado");
        root.transform.SetPositionAndRotation(position, rotation);

        if (planeKind == PlacementPlaneKind.Horizontal)
        {
            AddPrimitive(root.transform, PrimitiveType.Cylinder, "Base amarilla", new Vector3(0f, 0.12f, 0f), new Vector3(0.6f, 0.24f, 0.6f), fallbackHorizontalMaterial);
            AddPrimitive(root.transform, PrimitiveType.Cube, "Frente verde", new Vector3(0f, 0.78f, 0.18f), new Vector3(0.34f, 0.28f, 0.16f), fallbackTopMaterial);
            AddPrimitive(root.transform, PrimitiveType.Cube, "Abajo rojo", new Vector3(0f, -0.28f, 0f), new Vector3(0.48f, 0.16f, 0.48f), fallbackBottomMaterial);
        }
        else
        {
            AddPrimitive(root.transform, PrimitiveType.Cube, "Cuerpo azul", new Vector3(0f, 0f, 0.08f), new Vector3(0.34f, 0.9f, 0.16f), fallbackVerticalMaterial);
            AddPrimitive(root.transform, PrimitiveType.Cube, "Arriba verde", new Vector3(0f, 0.52f, 0.12f), new Vector3(0.52f, 0.18f, 0.22f), fallbackTopMaterial);
            AddPrimitive(root.transform, PrimitiveType.Cube, "Abajo rojo", new Vector3(0f, -0.52f, 0.12f), new Vector3(0.52f, 0.18f, 0.22f), fallbackBottomMaterial);
        }

        return root;
    }

    void EnsureFallbackMaterials()
    {
        fallbackHorizontalMaterial ??= CreateRuntimeMaterial(new Color(1f, 0.88f, 0.15f, 1f));
        fallbackVerticalMaterial ??= CreateRuntimeMaterial(new Color(0.12f, 0.32f, 1f, 1f));
        fallbackTopMaterial ??= CreateRuntimeMaterial(new Color(0.05f, 1f, 0.32f, 1f));
        fallbackBottomMaterial ??= CreateRuntimeMaterial(new Color(1f, 0.08f, 0.08f, 1f));
    }

    static Material CreateRuntimeMaterial(Color color)
    {
        var shader = Shader.Find("Universal Render Pipeline/Lit");
        if (shader == null)
            shader = Shader.Find("Standard");

        var material = new Material(shader);
        material.color = color;

        if (material.HasProperty("_BaseColor"))
            material.SetColor("_BaseColor", color);

        return material;
    }

    static GameObject AddPrimitive(Transform parent, PrimitiveType primitiveType, string name, Vector3 localPosition, Vector3 localScale, Material material)
    {
        var primitive = GameObject.CreatePrimitive(primitiveType);
        primitive.name = name;
        primitive.transform.SetParent(parent, false);
        primitive.transform.localPosition = localPosition;
        primitive.transform.localScale = localScale;

        var renderer = primitive.GetComponent<Renderer>();
        if (renderer != null)
            renderer.sharedMaterial = material;

        return primitive;
    }
}
