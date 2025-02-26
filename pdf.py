from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfgen import canvas

def createPDF(filename):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Spacer(1, 50))
    content.append(Paragraph("Título sobre a página 1", styles["Title"]))
    content.append(PageBreak())

    content.append(Spacer(1, 50))
    content.append(Paragraph("Título sobre a página 2", styles["Title"]))
    content.append(PageBreak())

    content.append(Spacer(1, 50))
    content.append(Paragraph("Título sobre a página 3", styles["Title"]))

    # Construir o PDF e aplicar a imagem de fundo correta para cada página
    doc.build(content)


if __name__ == "__main__":
    createPDF("output.pdf")
