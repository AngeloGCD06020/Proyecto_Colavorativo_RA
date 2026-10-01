# Reporte breve - Parcial Realidad Aumentada

La escena `Assets/Scenes/Parcial.unity` queda configurada para AR Foundation con `AR Session`, `XR Origin`, `ARPlaneManager` y `ARRaycastManager`. La build usa esta escena directamente en `ProjectSettings/EditorBuildSettings.asset`.

## Funciones implementadas

- Deteccion de planos horizontales y verticales con `ARPlaneManager`.
- Visualizacion diferenciada de planos: horizontales en amarillo y verticales en azul.
- Etiqueta por plano con dimensiones en metros.
- Selector en pantalla para elegir entre modelo horizontal y modelo vertical.
- Raycast sobre `TrackableType.PlaneWithinPolygon` para obtener el punto de colocacion.
- Validacion de tipo de plano: el modelo horizontal solo se coloca en planos horizontales, y el vertical solo en planos verticales.
- Instanciacion multiple de objetos, respetando la posicion y rotacion del plano detectado.
- Mensajes de estado: escaneo, superficie horizontal detectada, superficie vertical detectada y objeto colocado.

## Materiales y orientacion

Los modelos generados en runtime usan materiales de color para distinguir su funcion: amarillo para el modelo horizontal, azul para el modelo vertical, verde para indicar arriba/frente y rojo para indicar abajo. Esto permite ver claramente la orientacion de cada instancia al colocarse sobre el plano detectado.

## Archivos principales

- `Assets/Scripts/RaycastController.cs`: seleccion de modelo, UI, raycast, validacion e instanciacion.
- `Assets/Scripts/ARPlaneDimensionLabel.cs`: color de plano y etiqueta de dimensiones.
- `Assets/Editor/ParcialAndroidBuilder.cs`: build de APK de la escena `Parcial`.
