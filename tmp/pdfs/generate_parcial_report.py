# -*- coding: utf-8 -*-
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "pdf" / "Reporte_Parcial_Realidad_Aumentada.pdf"


class OrientationDiagram(Flowable):
    def __init__(self, kind):
        super().__init__()
        self.kind = kind
        self.width = 7.1 * inch
        self.height = 2.45 * inch

    def wrap(self, avail_width, avail_height):
        return min(self.width, avail_width), self.height

    def draw(self):
        c = self.canv
        w, h = self.width, self.height
        c.saveState()

        c.setStrokeColor(colors.HexColor("#D5DAE3"))
        c.setFillColor(colors.HexColor("#F7F9FC"))
        c.roundRect(0, 0, w, h, 8, stroke=1, fill=1)

        if self.kind == "horizontal":
            self._draw_horizontal(c, w, h)
        else:
            self._draw_vertical(c, w, h)

        c.restoreState()

    def _draw_horizontal(self, c, w, h):
        c.setFillColor(colors.HexColor("#FFE166"))
        c.setStrokeColor(colors.HexColor("#BFA100"))
        plane = [
            (0.65 * inch, 0.58 * inch),
            (3.25 * inch, 0.58 * inch),
            (3.85 * inch, 1.12 * inch),
            (1.25 * inch, 1.12 * inch),
        ]
        p = c.beginPath()
        p.moveTo(*plane[0])
        for point in plane[1:]:
            p.lineTo(*point)
        p.close()
        c.drawPath(p, stroke=1, fill=1)

        c.setFillColor(colors.HexColor("#FFC82E"))
        c.setStrokeColor(colors.HexColor("#9C7D00"))
        c.ellipse(1.95 * inch, 0.95 * inch, 2.65 * inch, 1.25 * inch, stroke=1, fill=1)
        c.rect(2.23 * inch, 1.18 * inch, 0.72 * inch, 0.28 * inch, stroke=0, fill=1)

        c.setFillColor(colors.HexColor("#18A957"))
        c.rect(2.38 * inch, 1.42 * inch, 0.42 * inch, 0.36 * inch, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#D93636"))
        c.rect(2.22 * inch, 0.72 * inch, 0.74 * inch, 0.14 * inch, stroke=0, fill=1)

        self._label(c, "Plano horizontal", 4.35 * inch, 1.63 * inch, "#7A6500")
        self._body(c, "Material amarillo en el plano detectado. El modelo horizontal se instancia usando la rotacion del hit sobre piso o mesa.", 4.35 * inch, 1.05 * inch)
        self._legend(c, 4.35 * inch, 0.32 * inch)

    def _draw_vertical(self, c, w, h):
        c.setFillColor(colors.HexColor("#5D8DFF"))
        c.setStrokeColor(colors.HexColor("#1B49A8"))
        c.rect(0.85 * inch, 0.42 * inch, 2.45 * inch, 1.65 * inch, stroke=1, fill=1)
        c.setStrokeColor(colors.HexColor("#D5E2FF"))
        for x in [1.35, 1.85, 2.35, 2.85]:
            c.line(x * inch, 0.42 * inch, x * inch, 2.07 * inch)

        c.setFillColor(colors.HexColor("#1F52FF"))
        c.rect(1.9 * inch, 0.78 * inch, 0.42 * inch, 0.95 * inch, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#18A957"))
        c.rect(1.75 * inch, 1.74 * inch, 0.72 * inch, 0.18 * inch, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#D93636"))
        c.rect(1.75 * inch, 0.58 * inch, 0.72 * inch, 0.18 * inch, stroke=0, fill=1)

        self._label(c, "Plano vertical", 4.35 * inch, 1.63 * inch, "#1B49A8")
        self._body(c, "Material azul en paredes. El modelo vertical conserva el frente contra el plano y muestra arriba/abajo con colores auxiliares.", 4.35 * inch, 1.05 * inch)
        self._legend(c, 4.35 * inch, 0.32 * inch)

    def _label(self, c, text, x, y, color):
        c.setFont("Helvetica-Bold", 13)
        c.setFillColor(colors.HexColor(color))
        c.drawString(x, y, text)

    def _body(self, c, text, x, y):
        text_object = c.beginText(x, y)
        text_object.setFont("Helvetica", 9.5)
        text_object.setFillColor(colors.HexColor("#344054"))
        max_chars = 42
        words = text.split()
        line = ""
        for word in words:
            candidate = f"{line} {word}".strip()
            if len(candidate) > max_chars:
                text_object.textLine(line)
                line = word
            else:
                line = candidate
        if line:
            text_object.textLine(line)
        c.drawText(text_object)

    def _legend(self, c, x, y):
        items = [
            ("#18A957", "verde: arriba/frente"),
            ("#D93636", "rojo: abajo"),
        ]
        c.setFont("Helvetica", 8.5)
        for index, (color, label) in enumerate(items):
            xx = x + index * 1.65 * inch
            c.setFillColor(colors.HexColor(color))
            c.rect(xx, y, 0.13 * inch, 0.13 * inch, stroke=0, fill=1)
            c.setFillColor(colors.HexColor("#344054"))
            c.drawString(xx + 0.18 * inch, y, label)


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=23,
            leading=28,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#101828"),
            spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#475467"),
            spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#101828"),
            spaceBefore=8,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=15,
            textColor=colors.HexColor("#1D2939"),
            spaceBefore=8,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.6,
            leading=13.5,
            textColor=colors.HexColor("#344054"),
            alignment=TA_LEFT,
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.6,
            leading=12,
            textColor=colors.HexColor("#475467"),
        ),
        "table_header": ParagraphStyle(
            "table_header",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.6,
            leading=12,
            textColor=colors.white,
        ),
        "code": ParagraphStyle(
            "code",
            parent=base["BodyText"],
            fontName="Courier",
            fontSize=8.2,
            leading=11,
            textColor=colors.HexColor("#344054"),
        ),
    }


def p(text, style):
    return Paragraph(text, style)


def hp(text, styles):
    return Paragraph(f"<b>{text}</b>", styles["table_header"])


def table(data, widths, header=True):
    style = [
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#D0D5DD")),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#EAECF0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#101828")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
    return Table(data, colWidths=widths, repeatRows=1 if header else 0, style=TableStyle(style))


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#EAECF0"))
    canvas.line(doc.leftMargin, 0.55 * inch, letter[0] - doc.rightMargin, 0.55 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#667085"))
    canvas.drawString(doc.leftMargin, 0.34 * inch, "Proyecto Colaborativo RA - Parcial")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.34 * inch, f"Pagina {doc.page}")
    canvas.restoreState()


def build():
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=0.62 * inch,
        rightMargin=0.62 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.72 * inch,
        title="Reporte Parcial Realidad Aumentada",
        author="Proyecto Colaborativo RA",
    )

    story = [
        p("Reporte breve - Parcial Realidad Aumentada", styles["title"]),
        p("Escena evaluada: <b>Assets/Scenes/Parcial.unity</b><br/>Build Android generada: <b>Build/Parcial_RA.apk</b><br/>Fecha: 1 de octubre de 2026", styles["subtitle"]),
        p("Resumen", styles["h1"]),
        p("La escena Parcial fue preparada como una experiencia de realidad aumentada con AR Foundation y ARCore. El flujo principal detecta superficies reales horizontales y verticales, muestra cada plano con un material diferenciado, etiqueta sus dimensiones en metros y permite colocar multiples objetos mediante raycast desde la pantalla del celular.", styles["body"]),
        p("El usuario puede alternar entre dos modelos desde una interfaz en pantalla. El modelo horizontal solo se coloca sobre pisos o mesas, mientras que el modelo vertical solo se coloca sobre paredes. Cada instancia respeta la posicion y la rotacion devuelta por el plano detectado.", styles["body"]),
        p("Requisitos implementados", styles["h1"]),
    ]

    req_rows = [
        [hp("Requisito", styles), hp("Implementacion", styles)],
        [p("Deteccion de planos horizontales y verticales", styles["small"]), p("Se usa <font name='Courier'>ARPlaneManager</font> y se revisa <font name='Courier'>PlaneAlignment</font> para diferenciar superficies horizontales y verticales.", styles["small"])],
        [p("Material amarillo para horizontales y azul para verticales", styles["small"]), p("El componente <font name='Courier'>ARPlaneDimensionLabel</font> asigna materiales transparentes: amarillo para horizontal y azul para vertical.", styles["small"])],
        [p("Mostrar dimensiones del plano", styles["small"]), p("Cada plano recibe una etiqueta TextMeshPro con ancho y alto en metros, actualizada durante la deteccion.", styles["small"])],
        [p("Seleccion entre dos modelos", styles["small"]), p("La UI creada en runtime tiene botones para elegir <i>modelo horizontal</i> o <i>modelo vertical</i>.", styles["small"])],
        [p("Colocar multiples objetos por raycast", styles["small"]), p("El script usa <font name='Courier'>ARRaycastManager.Raycast</font> con <font name='Courier'>TrackableType.PlaneWithinPolygon</font> y permite instanciar varios objetos.", styles["small"])],
        [p("Respetar orientacion del plano", styles["small"]), p("La rotacion de la instancia se calcula con <font name='Courier'>hit.pose.rotation</font> y un offset opcional por tipo de modelo.", styles["small"])],
        [p("Mensajes de estado", styles["small"]), p("Se muestran textos para escaneo, deteccion horizontal, deteccion vertical y colocacion correcta en cada tipo de plano.", styles["small"])],
    ]
    story.append(table(req_rows, [2.15 * inch, 4.9 * inch]))
    story += [
        Spacer(1, 0.18 * inch),
        p("Funciones principales", styles["h1"]),
        p("<b>RaycastController.cs</b> concentra la interaccion de usuario. En <font name='Courier'>Awake</font> localiza los managers AR, crea la UI de seleccion y muestra el mensaje inicial <font name='Courier'>Escaneando entorno ...</font>. En <font name='Courier'>Update</font> escucha el toque del usuario y evita colocar objetos cuando se toca la UI.", styles["body"]),
        p("Cuando el usuario toca la pantalla, <font name='Courier'>TryPlaceSelectedModel</font> ejecuta el raycast, obtiene el plano golpeado, valida si el tipo de plano coincide con el modelo seleccionado y, si corresponde, instancia el prefab o el modelo generado de respaldo. Al terminar muestra <font name='Courier'>Objeto colocado en plano horizontal</font> o <font name='Courier'>Objeto colocado en plano vertical</font>.", styles["body"]),
        p("<b>ARPlaneDimensionLabel.cs</b> se agrega automaticamente a cada plano detectado. Este componente cambia el material segun la alineacion, calcula las dimensiones del plano con <font name='Courier'>plane.size</font> y orienta la etiqueta hacia la camara para que sea legible durante la prueba.", styles["body"]),
        p("Mensajes visibles", styles["h2"]),
    ]

    msg_rows = [
        [hp("Escenario", styles), hp("Mensaje", styles)],
        [p("Busqueda inicial", styles["small"]), p("<font name='Courier'>Escaneando entorno ...</font>", styles["small"])],
        [p("Primer plano horizontal", styles["small"]), p("<font name='Courier'>Superficie horizontal detectada!</font>", styles["small"])],
        [p("Primer plano vertical", styles["small"]), p("<font name='Courier'>Superficie vertical detectada!</font>", styles["small"])],
        [p("Instancia en horizontal", styles["small"]), p("<font name='Courier'>Objeto colocado en plano horizontal</font>", styles["small"])],
        [p("Instancia en vertical", styles["small"]), p("<font name='Courier'>Objeto colocado en plano vertical</font>", styles["small"])],
    ]
    story.append(table(msg_rows, [2.35 * inch, 4.7 * inch]))
    story.append(Spacer(1, 0.18 * inch))

    story += [
        p("Orientacion y materiales", styles["h1"]),
        p("La visualizacion usa colores para comprobar rapidamente que el objeto colocado corresponde al tipo de superficie. Los planos horizontales se muestran en amarillo y los verticales en azul. Los modelos generados de respaldo agregan verde para identificar la parte superior o frontal y rojo para marcar la parte inferior.", styles["body"]),
        KeepTogether([p("Figura 1. Modelo para plano horizontal", styles["h2"]), OrientationDiagram("horizontal")]),
        Spacer(1, 0.18 * inch),
        KeepTogether([p("Figura 2. Modelo para plano vertical", styles["h2"]), OrientationDiagram("vertical")]),
        Spacer(1, 0.18 * inch),
        p("Tabla de materiales", styles["h2"]),
    ]

    mat_rows = [
        [hp("Elemento", styles), hp("Color/material", styles), hp("Uso en la escena", styles)],
        [p("Plano horizontal", styles["small"]), p("Amarillo transparente", styles["small"]), p("Indica superficies como piso o mesa detectadas por ARCore.", styles["small"])],
        [p("Plano vertical", styles["small"]), p("Azul transparente", styles["small"]), p("Indica superficies como paredes detectadas por ARCore.", styles["small"])],
        [p("Modelo horizontal", styles["small"]), p("Base amarilla, frente verde, parte inferior roja", styles["small"]), p("Confirma que el objeto fue colocado en una superficie horizontal.", styles["small"])],
        [p("Modelo vertical", styles["small"]), p("Cuerpo azul, parte superior/frontal verde, parte inferior roja", styles["small"]), p("Confirma que el objeto fue colocado sobre una superficie vertical.", styles["small"])],
    ]
    story.append(table(mat_rows, [1.55 * inch, 2.25 * inch, 3.25 * inch]))

    story += [
        Spacer(1, 0.18 * inch),
        p("Archivos modificados o agregados", styles["h1"]),
    ]
    file_rows = [
        [hp("Archivo", styles), hp("Funcion", styles)],
        [p("<font name='Courier'>Assets/Scripts/RaycastController.cs</font>", styles["small"]), p("Seleccion de modelo, UI, raycast, validacion de tipo de plano e instanciacion multiple.", styles["small"])],
        [p("<font name='Courier'>Assets/Scripts/ARPlaneDimensionLabel.cs</font>", styles["small"]), p("Materiales para planos y etiquetas de dimensiones.", styles["small"])],
        [p("<font name='Courier'>Assets/Scenes/Parcial.unity</font>", styles["small"]), p("Escena principal con AR Session, XR Origin y managers AR.", styles["small"])],
        [p("<font name='Courier'>Assets/Editor/ParcialAndroidBuilder.cs</font>", styles["small"]), p("Metodo auxiliar para generar el APK Android de la escena Parcial.", styles["small"])],
        [p("<font name='Courier'>ProjectSettings/EditorBuildSettings.asset</font>", styles["small"]), p("Configurado para incluir la escena Parcial en la build.", styles["small"])],
    ]
    story.append(table(file_rows, [2.75 * inch, 4.3 * inch]))
    story += [
        Spacer(1, 0.18 * inch),
        KeepTogether([
            p("Evidencia de build", styles["h1"]),
            p("La build Android se genero correctamente con Gradle y se copio como <font name='Courier'>Build/Parcial_RA.apk</font>. Tambien se instalo en el dispositivo Samsung conectado mediante ADB, con resultado <font name='Courier'>Success</font>.", styles["body"]),
        ]),
        Spacer(1, 0.12 * inch),
        p("Checklist de validacion", styles["h1"]),
        p("Para el video de entrega, se recomienda grabar estas acciones en orden para demostrar todos los requisitos solicitados.", styles["body"]),
    ]

    checklist_rows = [
        [hp("Paso", styles), hp("Que se debe mostrar", styles)],
        [p("1", styles["small"]), p("Abrir la app instalada y aceptar el permiso de camara si Android lo solicita.", styles["small"])],
        [p("2", styles["small"]), p("Escanear una mesa o piso hasta que aparezca el plano horizontal amarillo con su etiqueta de dimensiones.", styles["small"])],
        [p("3", styles["small"]), p("Seleccionar el modelo horizontal y colocarlo sobre la superficie horizontal.", styles["small"])],
        [p("4", styles["small"]), p("Escanear una pared hasta que aparezca el plano vertical azul con su etiqueta de dimensiones.", styles["small"])],
        [p("5", styles["small"]), p("Seleccionar el modelo vertical y colocarlo sobre la superficie vertical.", styles["small"])],
        [p("6", styles["small"]), p("Colocar mas de una instancia para evidenciar que la colocacion multiple funciona.", styles["small"])],
    ]
    story.append(table(checklist_rows, [0.6 * inch, 6.45 * inch]))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


if __name__ == "__main__":
    build()
