from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def add_background(canvas, image_path):
    canvas.drawImage(image_path, 0, 0, width=595, height=842)

def add_overlay_text(canvas, x, y, text, font_size=12, font_name="Helvetica-Bold"):
    canvas.setFont(font_name, font_size)
    canvas.setFillColorRGB(0, 0, 0)
    canvas.drawString(x, y, text)

def createPDF(filename):
    # Background images path
    image_page1 = "CTRVend379SB2025-AGRÍCOLA GEMELLIx COFCO BRASIL SA_pages-to-jpg-0001.jpg"
    image_page2 = "CTRVend379SB2025-AGRÍCOLA GEMELLIx COFCO BRASIL SA_pages-to-jpg-0002.jpg"
    image_page3 = "CTRVend379SB2025-AGRÍCOLA GEMELLIx COFCO BRASIL SA_pages-to-jpg-0003.jpg"

    # Create a PDF using canvas
    c = canvas.Canvas(filename, pagesize=A4)

    # Page 1
    add_background(c, image_page1)
    add_overlay_text(c, 110, 615, "TESTE TESTE TESTE TESTE TESTE!")
    c.showPage()  # Finalize the current page and start a new one

    # Page 2
    add_background(c, image_page2)
    c.showPage()  # Finalize the current page and start a new one

    # Page 3
    add_background(c, image_page3)
    c.showPage()  # Finalize the current page

    # Save the PDF
    c.save()
    print("created pdf file")

if __name__ == "__main__":
    createPDF("output.pdf")