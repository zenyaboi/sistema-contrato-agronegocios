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

def info_text(c):
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

def sb_co_text(c):
    # product info (SB/CO)
    add_overlay_text(c, 40, 342, "TESTE TESTE TESTE\nTESTE TESTE TESTE", 8)
    add_overlay_text(c, 150, 348, "2020", 8)
    add_overlay_text(c, 223, 348, "0", 8)
    add_overlay_text(c, 285, 348, "0", 8)
    add_overlay_text(c, 372, 348, "0", 8)
    add_overlay_text(c, 151, 250, "0000 TONELADAS MÉTRICAS", 9)
    add_overlay_text(c, 151, 240, "R$ 0000,00/SC. 60KG", 9)
    add_overlay_text(c, 151, 228, "00/00/0000", 9)
    add_overlay_text(c, 151, 218, "TESTE TESTE TESTE TESTE TESTE", 9)
    add_overlay_text(c, 151, 206, "TESTE TESTE TESTE TESTE TESTE", 9)

def wh_text(c):
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
    add_overlay_text(c, 151, 315, "R$ 0000,00/TONELADA MÉTRICA", 9)
    add_overlay_text(c, 151, 302, "00/00/0000", 9)
    add_overlay_text(c, 151, 291, "TESTE TESTE TESTE TESTE TESTE", 9)
    add_overlay_text(c, 151, 279, "TESTE TESTE TESTE TESTE TESTE", 9)

def createPDF(filename):
    # Background images path
    # SB/CO model
    image_page1 = "CONTRATO MODELO SB & CO_page-0001.jpg"
    # WH model
    #image_page1 = "CONTRATO MODELO WH_page-0001.jpg"
    image_page2 = "CONTRATO MODELO SB & CO_page-0002.jpg"
    image_page3 = "CONTRATO MODELO SB & CO_page-0003.jpg"
    image_page4 = "CONTRATO MODELO SB & CO_page-0004.jpg"

    # Create a PDF using canvas
    c = canvas.Canvas(filename, pagesize=A4)

    # Page 1
    add_background(c, image_page1)

    info_text(c)
    
    c.showPage() 

    # Page 2
    add_background(c, image_page2)

    sb_co_text(c)
    #wh_text(c)

    c.showPage()

    # Page 3
    add_background(c, image_page3)
    c.showPage()

    # Page 4
    add_background(c, image_page4)
    c.showPage()

    # Save the PDF
    c.save()
    print("created pdf file")

if __name__ == "__main__":
    createPDF("output.pdf")