from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

isSb = False

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
        canvas.setFont(font_name, font_size)
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_width = canvas.stringWidth(test_line, font_name, font_size)
            
            if test_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)

        text_object = canvas.beginText(x, y)
        text_object.setFont(font_name, font_size)
        for line in lines:
            text_object.textLine(line)

        canvas.drawText(text_object)
        return len(lines) * line_height

    except Exception as e:
        print(f"Erro ao renderizar texto: {e}")
        canvas.setFont(font_name, font_size)
        canvas.drawString(x, y, text[:50] + "...")
        return line_height

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
    isSb = True
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
    isSb = False
    add_wrapped_text(c, 35, 789, "TESTE TESTE TESTE TESTE TESTE TESTE", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 140, 788, "9999", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 194, 788, "99", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 250, 788, "99", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 330, 788, "999", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 396, 788, "999", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 440, 788, "9", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 489, 788, "9", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 552, 788, "9,9", 8, max_width=100, line_height=1)

    add_wrapped_text(c, 150, 722, "0000 TONELADAS MÉTRICAS", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 710, "R$ 0000,00/TONELADA MÉTRICA", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 698, "00/00/0000", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 686, "TESTE TESTE TESTE TESTE TESTE", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 674, "TESTE TESTE TESTE TESTE TESTE", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 27, 620, "Trigo isento de insetos vivos e/ou mortos (caso haja incidência, as cargas serão devolvidas, e o vendedor será responsável pelo custo do frete).", 
                    10, max_width=550, line_height=12)

def additional_text(c):
    # product info
    add_wrapped_text(c, 40, 679, "TESTE TESTE TESTE TESTE TESTE TESTE", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 155, 678, "9999", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 225, 678, "99", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 285, 678, "99%", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 359, 678, "9", 8, max_width=100, line_height=1)

def obs_text(c, obs_list):
    if (isSb):
        y = 454
    else:
        y = 595
    for obs in obs_list:
        used_height = add_wrapped_text(c, 27, y, obs, 10, max_width=550, line_height=12)
        y -= used_height + 5

def payment_info_text(c):
    add_wrapped_text(c, 138, 692, "BANCO: TESTE TESTE TESTE TESTE", 7, max_width=200, line_height=1)
    add_wrapped_text(c, 308, 692, "0000-0", 7, max_width=100, line_height=1)
    add_wrapped_text(c, 408, 692, "000000-0", 7, max_width=100, line_height=1)
    add_wrapped_text(c, 138, 679, "TESTE TESTE TESTE TESTE TESTE TESTE", 7, max_width=100, line_height=1)
    add_wrapped_text(c, 298, 679, "12.123.123/0001-23", 7, max_width=100, line_height=1)
    add_wrapped_text(c, 138, 658, "CIF TESTE TESTE TESTE TESTE", 7, max_width=150, line_height=1)
    add_wrapped_text(c, 290, 658, "TT", 7, max_width=100, line_height=1)
    add_overlay_text(c, 138, 634, "0,20% TESTE TESTE TESTE TESTE TESTE TESTE TESTE TESTE", 7)

def signing_text(c):
    vendedor_height = add_wrapped_text(c, 40, 425, "TESTE TESTE TESTE TESTE TESTE TESTE TESTE TESTE TESTE", 7, max_width=180, line_height=1)
    add_wrapped_text(c, 81, 425 - vendedor_height * 6 - 5, "12.123.123/0001-23", 7, max_width=200, line_height=1)
    comprador_height = add_wrapped_text(c, 345, 425, "TESTE TESTE TESTE TESTE TESTE TESTE", 7, max_width=180, line_height=1)
    add_wrapped_text(c, 400, 425 - comprador_height * 6 - 5, "12.123.123/0001-23", 7, max_width=200, line_height=1)

def createPDF(filename):
    # Background images path
    image_page1 = "CONTRATO MODELO SB & CO_page-0001.jpg"
    # SB/CO model
    #image_page2 = "CONTRATO MODELO SB & CO_page-0002.jpg"
    # WH model
    image_page2 = "CONTRATO MODELO WH_page-0002.jpg"
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

    if (isSb):
        sb_co_text(c)
        additional_text(c)
    else:
        wh_text(c)

    observacoes = [
        "Observação curta.",
        "Observação bem mais longa que provavelmente vai ocupar mais de uma linha dependendo da largura da caixa.",
        "Outra observação compacta.",
        "Uma ainda mais longa para testar se o recuo vertical funciona corretamente ao empilhar vários blocos de texto grandes.",
    ]
    
    obs_text(c, observacoes)

    c.showPage()

    # Page 3
    add_background(c, image_page3)

    payment_info_text(c)
    signing_text(c)

    c.showPage()

    # Page 4
    add_background(c, image_page4)
    c.showPage()

    # Save the PDF
    c.save()
    print("created pdf file")

if __name__ == "__main__":
    createPDF("output.pdf")