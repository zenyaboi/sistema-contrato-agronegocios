from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


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

def add_wrapped_text(canvas, x, y, text, font_size, font_name="Helvetica-Bold", 
                    max_width=100, line_height=12):
    try:
        # Configurações iniciais
        canvas.setFont(font_name, font_size)
        text_object = canvas.beginText(x, y)
        
        words = text.split()
        current_line = []
        current_width = 0
        
        for word in words:
            word_width = canvas.stringWidth(word + ' ', font_name, font_size)
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                # Desenha a linha atual e reinicia
                text_object.textLine(' '.join(current_line))
                text_object.moveCursor(0, -line_height)
                current_line = [word]
                current_width = word_width
        
        # Desenha a última linha
        if current_line:
            text_object.textLine(' '.join(current_line))
        
        canvas.drawText(text_object)
    except Exception as e:
        print(f"Erro ao renderizar texto: {e}")
        # Fallback: desenha o texto em uma linha só
        canvas.setFont(font_name, font_size)
        canvas.drawString(x, y, text[:50] + "...")

def info_text(c):
    # contract info
    add_overlay_text(c, 130, 648, "000/SB/0000", 10)
    add_overlay_text(c, 325, 648, "00 de Fevereiro de 0000", 10)
    # seller info
    add_overlay_text(c, 115, 613, "TESTE TESTE TESTE TESTE TESTE!", 10)
    add_overlay_text(c, 155, 595, "12.123.123/0001-23", 10)
    add_overlay_text(c, 333, 595, "12300012-31", 10)
    add_overlay_text(c, 170, 577, "RUA TESTE TESTE TESTE TESTE TESTE, 202, NUMERO CASA TERREO AP RODOVIA", 10)
    add_overlay_text(c, 158, 559, "TESTE TESTE", 10)
    add_overlay_text(c, 336, 559, "TT", 10)
    add_overlay_text(c, 145, 541, "BRASIL TESTE", 10)
    add_overlay_text(c, 345, 541, "00.000-000", 10)
    # buyer info
    add_overlay_text(c, 125, 502, "TESTE TESTE TESTE TESTE TESTE!", 10)
    add_overlay_text(c, 160, 487, "12.123.123/0001-23", 10)
    add_overlay_text(c, 338, 487, "12300012-31", 10)
    add_overlay_text(c, 174, 469, "RUA TESTE TESTE TESTE TESTE TESTE, 202, NUMERO CASA TERREO AP RODOVIA", 10)
    add_overlay_text(c, 165, 452, "TESTE TESTE", 10)
    add_overlay_text(c, 335, 452, "TT", 10)
    add_overlay_text(c, 160, 434, "BRASIL TESTE", 10)
    add_overlay_text(c, 343, 434, "00.000-000", 10)

def sb_co_text(c):
    # product info (SB/CO)
    add_wrapped_text(c, 40, 792, "TESTE TESTE TESTE TESTE TESTE TESTE", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 155, 791, "9999", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 225, 791, "99", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 285, 791, "99%", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 359, 791, "9", 8, max_width=100, line_height=1)

    add_wrapped_text(c, 150, 556, "0000 TONELADAS MÉTRICAS", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 544, "R$ 0000,00/SC. 60KG", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 532, "00/00/0000", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 521, "TESTE TESTE TESTE TESTE TESTE", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 509, "TESTE TESTE TESTE TESTE TESTE", 9, max_width=200, line_height=1)

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

def additional_text(c):
    # product info
    add_wrapped_text(c, 40, 679, "TESTE TESTE TESTE TESTE TESTE TESTE", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 155, 678, "9999", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 225, 678, "99", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 285, 678, "99%", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 359, 678, "9", 8, max_width=100, line_height=1)

def obs_text(c, count):
    for number in range(count):
        print(number)
        add_wrapped_text(c, 27, 454 - number * 20, "TESTE TESTE TESTE TESTE TESTE TESTE TESTE", 10, max_width=550, line_height=1)

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
    additional_text(c)
    obs_text(c, 10)

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