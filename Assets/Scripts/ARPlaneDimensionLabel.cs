using TMPro;
using UnityEngine;
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;

[RequireComponent(typeof(ARPlane))]
[RequireComponent(typeof(MeshRenderer))]
public class ARPlaneDimensionLabel : MonoBehaviour
{
    [SerializeField] Color horizontalColor = new(1f, 0.88f, 0f, 0.45f);
    [SerializeField] Color verticalColor = new(0f, 0.24f, 1f, 0.45f);
    [SerializeField] float labelOffset = 0.04f;

    ARPlane plane;
    MeshRenderer meshRenderer;
    TextMeshPro label;
    Camera targetCamera;
    Material horizontalMaterial;
    Material verticalMaterial;
    PlaneAlignment lastAlignment = PlaneAlignment.None;

    public void Configure(Camera camera)
    {
        targetCamera = camera;
    }

    void Awake()
    {
        plane = GetComponent<ARPlane>();
        meshRenderer = GetComponent<MeshRenderer>();
        EnsureLabel();
        Refresh();
    }

    void Update()
    {
        Refresh();
        FaceCamera();
    }

    public void Refresh()
    {
        if (plane == null)
            plane = GetComponent<ARPlane>();

        if (meshRenderer == null)
            meshRenderer = GetComponent<MeshRenderer>();

        EnsureLabel();
        ApplyPlaneMaterial();

        if (label == null || plane == null)
            return;

        var size = plane.size;
        var typeName = plane.alignment.IsVertical() ? "Plano vertical" : "Plano horizontal";
        label.text = $"{typeName}\n{size.x:0.00} m x {size.y:0.00} m";
        label.transform.position = plane.center + plane.normal * labelOffset;
    }

    void ApplyPlaneMaterial()
    {
        if (meshRenderer == null || plane == null || plane.alignment == lastAlignment)
            return;

        lastAlignment = plane.alignment;

        if (plane.alignment.IsVertical())
        {
            verticalMaterial ??= CreateMaterial(verticalColor);
            meshRenderer.sharedMaterial = verticalMaterial;
        }
        else
        {
            horizontalMaterial ??= CreateMaterial(horizontalColor);
            meshRenderer.sharedMaterial = horizontalMaterial;
        }
    }

    void EnsureLabel()
    {
        if (label != null)
            return;

        var labelObject = new GameObject("Dimensiones del plano");
        labelObject.transform.SetParent(transform, false);
        labelObject.transform.localScale = Vector3.one * 0.05f;

        label = labelObject.AddComponent<TextMeshPro>();
        label.alignment = TextAlignmentOptions.Center;
        label.color = Color.white;
        label.fontSize = 2.2f;
        label.fontStyle = FontStyles.Bold;
        label.textWrappingMode = TextWrappingModes.NoWrap;
        label.outlineColor = Color.black;
        label.outlineWidth = 0.25f;

        var rectTransform = label.rectTransform;
        rectTransform.sizeDelta = new Vector2(6f, 1.2f);
    }

    void FaceCamera()
    {
        if (label == null)
            return;

        if (targetCamera == null)
            targetCamera = Camera.main;

        if (targetCamera == null)
            return;

        var direction = label.transform.position - targetCamera.transform.position;
        if (direction.sqrMagnitude > 0.0001f)
            label.transform.rotation = Quaternion.LookRotation(direction.normalized, Vector3.up);
    }

    Material CreateMaterial(Color color)
    {
        var baseMaterial = meshRenderer != null ? meshRenderer.sharedMaterial : null;
        Material material;

        if (baseMaterial != null)
        {
            material = new Material(baseMaterial);
        }
        else
        {
            var shader = Shader.Find("Universal Render Pipeline/Lit");
            if (shader == null)
                shader = Shader.Find("Standard");

            material = new Material(shader);
        }

        material.color = color;

        if (material.HasProperty("_BaseColor"))
            material.SetColor("_BaseColor", color);

        if (material.HasProperty("_Color"))
            material.SetColor("_Color", color);

        if (material.HasProperty("_Surface"))
            material.SetFloat("_Surface", 1f);

        if (material.HasProperty("_ZWrite"))
            material.SetFloat("_ZWrite", 0f);

        material.renderQueue = 3000;
        material.EnableKeyword("_SURFACE_TYPE_TRANSPARENT");
        material.EnableKeyword("_ALPHAPREMULTIPLY_ON");
        return material;
    }
}
