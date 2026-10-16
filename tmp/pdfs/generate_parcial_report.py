# -*- coding: utf-8 -*-
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Flowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "pdf" / "Reporte_Parcial_Realidad_Aumentada.pdf"


class MiniDiagram(Flowable):
    def __init__(self):
        super().__init__()
        self.width = 7.1 * inch
        self.height = 2.0 * inch

    def wrap(self, avail_width, avail_height):
        return min(self.width, avail_width), self.height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setStrokeColor(colors.HexColor("#D5DAE3"))
        c.setFillColor(colors.HexColor("#F8FAFC"))
        c.roundRect(0, 0, self.width, self.height, 8, stroke=1, fill=1)

        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor("#7A6500"))
        c.drawString(0.35 * inch, 1.63 * inch, "Modelo horizontal")
        c.setFillColor(colors.HexColor("#FFE166"))
        c.setStrokeColor(colors.HexColor("#BFA100"))
        path = c.beginPath()
        path.moveTo(0.45 * inch, 0.35 * inch)
        path.lineTo(2.25 * inch, 0.35 * inch)
        path.lineTo(2.65 * inch, 0.72 * inch)
        path.lineTo(0.85 * inch, 0.72 * inch)
        path.close()
        c.drawPath(path, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#FFC82E"))
        c.ellipse(1.25 * inch, 0.68 * inch, 1.75 * inch, 0.96 * inch, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#18A957"))
        c.rect(1.42 * inch, 1.0 * inch, 0.28 * inch, 0.34 * inch, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#D93636"))
        c.rect(1.25 * inch, 0.42 * inch, 0.62 * inch, 0.11 * inch, stroke=0, fill=1)

        c.setFillColor(colors.HexColor("#1B49A8"))
        c.drawString(3.9 * inch, 1.63 * inch, "Modelo vertical")
        c.setFillColor(colors.HexColor("#5D8DFF"))
        c.setStrokeColor(colors.HexColor("#1B49A8"))
        c.rect(4.0 * inch, 0.35 * inch, 1.75 * inch, 1.0 * inch, stroke=1, fill=1)
        c.setFillColor(colors.HexColor("#1F52FF"))
        c.rect(4.75 * inch, 0.52 * inch, 0.32 * inch, 0.66 * inch, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#18A957"))
        c.rect(4.58 * inch, 1.17 * inch, 0.66 * inch, 0.13 * inch, stroke=0, fill=1)
        c.setFillColor(colors.HexColor("#D93636"))
        c.rect(4.58 * inch, 0.42 * inch, 0.66 * inch, 0.13 * inch, stroke=0, fill=1)

        c.setFont("Helvetica", 8.5)
        c.setFillColor(colors.HexColor("#344054"))
        c.drawString(0.35 * inch, 0.08 * inch, "Amarillo: plano horizontal   Azul: plano vertical   Verde: frente/arriba   Rojo: abajo")
        c.restoreState()


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=26,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#101828"),
            spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10.2,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#475467"),
            spaceAfter=16,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=13.5,
            leading=17,
            textColor=colors.HexColor("#101828"),
            spaceBefore=7,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.7,
            leading=13.4,
            textColor=colors.HexColor("#344054"),
            alignment=TA_LEFT,
            spaceAfter=5,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            leftIndent=14,
            firstLineIndent=-8,
            textColor=colors.HexColor("#344054"),
            spaceAfter=3,
        ),
    }


def p(text, style):
    return Paragraph(text, style)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#EAECF0"))
    canvas.line(doc.leftMargin, 0.55 * inch, letter[0] - doc.rightMargin, 0.55 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#667085"))
    canvas.drawString(doc.leftMargin, 0.34 * inch, "Proyecto Colaborativo RA - Parcial")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.34 * inch, f"Pagina {doc.page}")
    canvas.restoreState()


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=0.68 * inch,
        rightMargin=0.68 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.72 * inch,
        title="Reporte Parcial Realidad Aumentada",
        author="Proyecto Colaborativo RA",
    )

    story = [
        p("Reporte breve - Parcial Realidad Aumentada", s["title"]),
        p("Escena Parcial - Build Android<br/>1 de octubre de 2026", s["subtitle"]),
        p("Resumen", s["h1"]),
        p("En este parcial realizamos una escena de realidad aumentada para Android. La aplicacion detecta superficies reales con la camara del celular y permite colocar modelos dependiendo del tipo de plano encontrado. La idea principal fue separar los planos horizontales, como piso o mesa, de los planos verticales, como una pared.", s["body"]),
        p("Tambien agregamos mensajes en pantalla para que el usuario sepa cuando la aplicacion esta escaneando, cuando ya encontro una superficie y cuando se coloco correctamente un objeto.", s["body"]),
        p("Funciones realizadas", s["h1"]),
        p("- Detectamos planos horizontales y verticales con AR Foundation.", s["bullet"]),
        p("- Pintamos los planos horizontales de amarillo y los verticales de azul para identificarlos rapidamente.", s["bullet"]),
        p("- Mostramos las dimensiones aproximadas del plano detectado en metros.", s["bullet"]),
        p("- Agregamos dos opciones de modelo: uno para superficies horizontales y otro para superficies verticales.", s["bullet"]),
        p("- Usamos raycast desde la pantalla para colocar objetos justo sobre el plano tocado.", s["bullet"]),
        p("- Permitimos colocar mas de un objeto durante la prueba.", s["bullet"]),
        p("Colocacion de modelos", s["h1"]),
        p("El modelo horizontal solo se puede colocar en superficies horizontales. Si el usuario toca una pared con ese modelo seleccionado, no se coloca y se mantiene la validacion del tipo de plano. De la misma forma, el modelo vertical solo se coloca sobre superficies verticales.", s["body"]),
        p("Para que la orientacion fuera clara, cada objeto toma la posicion y rotacion del plano detectado. Asi el modelo horizontal queda apoyado sobre piso o mesa, mientras que el modelo vertical queda alineado con la pared.", s["body"]),
        Spacer(1, 0.12 * inch),
        MiniDiagram(),
        PageBreak(),
        p("Materiales y orientacion", s["h1"]),
        p("Se usaron colores simples para comprobar visualmente que cada parte estuviera bien orientada. El amarillo representa el plano horizontal, el azul representa el plano vertical, el verde marca la parte de arriba o frente del modelo y el rojo marca la parte inferior.", s["body"]),
        p("Durante la prueba se puede ver que el modelo horizontal queda acostado sobre el plano amarillo, mientras que el modelo vertical queda de frente al plano azul. Esto ayuda a confirmar que la posicion y la rotacion se estan aplicando correctamente.", s["body"]),
        p("Build y prueba", s["h1"]),
        p("Al final se genero el APK de Android y se instalo en el celular para probarlo fuera del editor de Unity. En la build se reviso que la camara abriera correctamente, que aparecieran los planos detectados y que los objetos se pudieran colocar en el tipo de superficie correspondiente.", s["body"]),
        p("Conclusion", s["h1"]),
        p("La escena cumple con los puntos principales del parcial: deteccion de planos, materiales diferenciados, dimensiones visibles, seleccion de modelos y colocacion multiple mediante raycast. La prueba en celular permite comprobar el funcionamiento real de la aplicacion en realidad aumentada.", s["body"]),
    ]

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
