from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfgen import canvas

def add_background(canvas, doc, image_path):
    canvas.saveState()
    canvas.drawImage(image_path, 0, 0, width=595, height=842)
    canvas.restoreState()

def add_overlay_text(canvas, size, x, y, text):
    canvas.setFont("Helvetica-Bold", size)
    canvas.setFillColorRGB(0, 0, 0)
    canvas.drawString(x, y, text)

def createPDF(filename):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    # Background images path
    image_page1 = "CTRVend379SB2025-AGRÍCOLA GEMELLIx COFCO BRASIL SA_pages-to-jpg-0001.jpg"
    image_page2 = "CTRVend379SB2025-AGRÍCOLA GEMELLIx COFCO BRASIL SA_pages-to-jpg-0002.jpg"
    image_page3 = "CTRVend379SB2025-AGRÍCOLA GEMELLIx COFCO BRASIL SA_pages-to-jpg-0003.jpg"

    def on_page1(canvas, doc):
        add_background(canvas, doc, image_page1)
        add_overlay_text(canvas, 12, 110, 615, "TESTE TESTE TESTE TESTE TESTE!")

    def on_page2(canvas, doc):
        add_background(canvas, doc, image_page2)

    def on_page3(canvas, doc):
        add_background(canvas, doc, image_page3)

    content.append(Spacer(1, 50))
    content.append(Paragraph("Título sobre a página 1", styles["Title"]))
    content.append(PageBreak())

    content.append(Spacer(1, 50))
    content.append(Paragraph("Título sobre a página 2", styles["Title"]))
    content.append(PageBreak())

    content.append(Spacer(1, 50))
    content.append(Paragraph("Título sobre a página 3", styles["Title"]))

    doc.build(content, onFirstPage=on_page1, onLaterPages=lambda c, d: on_page2(c, d) if d.page == 2 else on_page3(c, d))

    print("created pdf file")


if __name__ == "__main__":
    createPDF("output.pdf")
