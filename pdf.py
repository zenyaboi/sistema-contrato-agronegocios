from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def add_background(canvas, image_path):
    canvas.drawImage(image_path, 0, 0, width=595, height=842)

def add_overlay_text(canvas, x, y, text, font_size, font_name="Helvetica-Bold", line_height=17):
    # Cria um objeto de texto
    text_object = canvas.beginText(x, y)
    text_object.setFont(font_name, font_size)
    text_object.setFillColorRGB(0, 0, 0)

    # Divide o texto em linhas
    lines = text.split("\n")  # Quebra o texto em linhas manualmente

    # Adiciona cada linha ao TextObject
    for line in lines:
        text_object.textLine(line)  # Adiciona uma linha e move para a próxima
        text_object.moveCursor(0, -line_height)  # Ajusta o espaçamento entre linhas

    # Desenha o texto no canvas
    canvas.drawText(text_object)

def sb_co_text(c):
    # contract info
    add_overlay_text(c, 130, 651, "000/SB/0000", 10)
    add_overlay_text(c, 324, 651, "00 de Fevereiro de 0000", 10)
    # seller info
    add_overlay_text(c, 110, 615, "TESTE TESTE TESTE TESTE TESTE!", 10)
    add_overlay_text(c, 138, 597, "12.123.123/0001-23", 10)
    add_overlay_text(c, 280, 597, "12300012-31", 10)
    add_overlay_text(c, 155, 579, "RUA TESTE TESTE TESTE TESTE TESTE, 202, NUMERO CASA TERREO AP RODOVIA", 10)
    add_overlay_text(c, 145, 562, "TESTE TESTE", 10)
    add_overlay_text(c, 292, 562, "TT", 10)
    add_overlay_text(c, 140, 543, "BRASIL TESTE", 10)
    add_overlay_text(c, 300, 543, "00.000-000", 10)
    # buyer info
    add_overlay_text(c, 120, 496, "TESTE TESTE TESTE TESTE TESTE!", 10)
    add_overlay_text(c, 160, 474, "12.123.123/0001-23", 10)
    add_overlay_text(c, 290, 474, "12300012-31", 10)
    add_overlay_text(c, 174, 455, "RUA TESTE TESTE TESTE TESTE TESTE, 202, NUMERO CASA TERREO AP RODOVIA", 10)
    add_overlay_text(c, 165, 438, "TESTE TESTE", 10)
    add_overlay_text(c, 289, 438, "TT", 10)
    add_overlay_text(c, 160, 420, "BRASIL TESTE", 10)
    add_overlay_text(c, 300, 420, "00.000-000", 10)
    # product info (SB/CO)
    add_overlay_text(c, 40, 342, "TESTE TESTE TESTE\nTESTE TESTE TESTE", 8)
    add_overlay_text(c, 150, 348, "2020", 8)
    add_overlay_text(c, 223, 348, "0", 8)
    add_overlay_text(c, 285, 348, "0", 8)
    add_overlay_text(c, 372, 348, "0", 8)
    add_overlay_text(c, 151, 250, "0000 TONELADAS MÉTRICAS", 9)

def wh_text(c):
    # contract info
    add_overlay_text(c, 130, 666, "000/SB/0000", 10)
    add_overlay_text(c, 320, 666, "00 de Fevereiro de 0000", 10)
    # seller info
    add_overlay_text(c, 125, 629, "TESTE TESTE TESTE TESTE TESTE!", 10)
    add_overlay_text(c, 155, 612, "12.123.123/0001-23", 10)
    add_overlay_text(c, 322, 612, "12300012-31", 10)
    add_overlay_text(c, 170, 594, "RUA TESTE TESTE TESTE TESTE TESTE, 202, NUMERO CASA TERREO AP RODOVIA", 10)
    add_overlay_text(c, 159, 576, "TESTE TESTE", 10)
    add_overlay_text(c, 309, 576, "TT", 10)
    add_overlay_text(c, 156, 558, "BRASIL TESTE", 10)
    add_overlay_text(c, 315, 558, "00.000-000", 10)
    # buyer info
    add_overlay_text(c, 130, 519, "TESTE TESTE TESTE TESTE TESTE!", 10)
    add_overlay_text(c, 165, 504, "12.123.123/0001-23", 10)
    add_overlay_text(c, 335, 504, "12300012-31", 10)
    add_overlay_text(c, 175, 486, "RUA TESTE TESTE TESTE TESTE TESTE, 202, NUMERO CASA TERREO AP RODOVIA", 10)
    add_overlay_text(c, 165, 468, "TESTE TESTE", 10)
    add_overlay_text(c, 335, 468, "TT", 10)
    add_overlay_text(c, 160, 452, "BRASIL TESTE", 10)
    add_overlay_text(c, 340, 452, "00.000-000", 10)
    # product info (WH)
    add_overlay_text(c, 40, 372, "TESTE TESTE TESTE\nTESTE TESTE TESTE", 8)
    add_overlay_text(c, 150, 379, "2020", 8)
    add_overlay_text(c, 223, 379, "000", 8)
    add_overlay_text(c, 300, 379, "00", 8)
    add_overlay_text(c, 339, 379, "000", 8)
    add_overlay_text(c, 374, 379, "0", 8)
    add_overlay_text(c, 419, 379, "0", 8)
    add_overlay_text(c, 474, 379, "00", 8)
    add_overlay_text(c, 528, 379, "0000", 8)
    add_overlay_text(c, 151, 325, "0000 TONELADAS MÉTRICAS", 9)

def createPDF(filename):
    # Background images path
    #image_page1 = "CTRVend379SB2025-AGRÍCOLA GEMELLIx COFCO BRASIL SA_pages-to-jpg-0001.jpg"
    image_page1 = "CTRVend361WH2025-STRAL GRÃOS  LTDA x MOINHO CIDADE BELLA LTDA_page-0001.jpg"
    image_page2 = "CTRVend379SB2025-AGRÍCOLA GEMELLIx COFCO BRASIL SA_pages-to-jpg-0002.jpg"
    image_page3 = "CTRVend379SB2025-AGRÍCOLA GEMELLIx COFCO BRASIL SA_pages-to-jpg-0003.jpg"

    # Create a PDF using canvas
    c = canvas.Canvas(filename, pagesize=A4)

    # Page 1
    add_background(c, image_page1)

    #sb_co_text(c)
    wh_text(c)
    
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