from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import sqlite3
import json

isSb = False

def get_client_data(client_id):
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
    client = cursor.fetchone()
    conn.close()
    print(client)

    if client:
        return {
            'id': client[0],
            'name': client[1],
            'cnpj': client[2],
            'address': client[3],
            'ie': client[4],
            'city': client[5],
            'state': client[6],
            'cep': client[7],
            'bank': client[8],
            'agency': client[9],
            'account': client[10]
        }
    return None

def get_separate_date(date_str, default_year=None):
    try:
        # Try splitting by slash first (DD/MM/YYYY)
        if '/' in date_str:
            day, month, year = date_str.split('/')
            if len(year) == 4 and year.isdigit():
                return year
            
        from datetime import datetime
        # Try parsing with datetime as fallback
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        return str(date_obj.year)
    
    except (ValueError, AttributeError, IndexError):
        # Return default year if provided, otherwise current year
        if default_year is not None:
            return str(default_year)
        return str(datetime.now().year)

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

def info_text(c, contract_data):
    seller = get_client_data(contract_data["seller_id"])
    buyer = get_client_data(contract_data["buyer_id"])
    year = get_separate_date(contract_data["contract_date"])

    # contract info
    add_overlay_text(c, 130, 648, f"{contract_data['contract_number']}/{contract_data['contract_type']}/{year}", 10)
    add_overlay_text(c, 325, 648, f"{contract_data['contract_date']}", 10)

    # seller info
    add_overlay_text(c, 115, 613, f"{seller['name']}", 10)
    add_overlay_text(c, 155, 595, f"{seller['cnpj']}", 10)
    add_overlay_text(c, 333, 595, f"{seller['ie']}", 10)
    add_overlay_text(c, 170, 577, f"{seller['address']}", 10)
    add_overlay_text(c, 158, 559, f"{seller['city']}", 10)
    add_overlay_text(c, 336, 559, f"{seller['state']}", 10)
    add_overlay_text(c, 145, 541, f"BRASIL", 10)
    add_overlay_text(c, 345, 541, f"{seller['cep']}", 10)

    # buyer info
    add_overlay_text(c, 125, 502, f"{buyer['name']}", 10)
    add_overlay_text(c, 160, 487, f"{buyer['cnpj']}", 10)
    add_overlay_text(c, 338, 487, f"{buyer['ie']}", 10)
    add_overlay_text(c, 174, 469, f"{buyer['address']}", 10)
    add_overlay_text(c, 165, 452, f"{buyer['city']}", 10)
    add_overlay_text(c, 335, 452, f"{buyer['state']}", 10)
    add_overlay_text(c, 160, 434, f"BRASIL", 10)
    add_overlay_text(c, 343, 434, f"{buyer['cep']}", 10)

def sb_co_text(c, contract_data):
    # product info (SB/CO)
    add_wrapped_text(c, 40, 792, f"{contract_data['product']}", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 155, 791, f"{contract_data['harvest']}", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 225, 791, f"{contract_data['umidade_maxima']}", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 285, 791, f"{contract_data['impureza_maxima']}%", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 359, 791, f"{contract_data['ardidos_avariados']}", 8, max_width=100, line_height=1)

    add_wrapped_text(c, 150, 556, f"{contract_data['quantity']} MÉTRICAS", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 544, f"R${contract_data['price']}/SC. 60KG", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 532, f"{contract_data['payment']}", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 521, f"{contract_data['weight_quality']}", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 509, f"{contract_data['delivery']}", 9, max_width=200, line_height=1)

def wh_text(c, contract_data):
    # product info (WH)
    add_wrapped_text(c, 35, 789, f"{contract_data['product']}", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 140, 788, f"{contract_data['harvest']}", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 194, 788, f"{contract_data['umidade_maxima']}", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 250, 788, f"{contract_data['ph']}", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 330, 788, f"{contract_data['falling_number']}", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 396, 788, f"{contract_data['w_minimo']}", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 440, 788, f"{contract_data['pl_minimo']}", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 489, 788, f"{contract_data['impureza_maxima']}", 8, max_width=100, line_height=1)
    add_wrapped_text(c, 552, 788, f"{contract_data['triguilho']}", 8, max_width=100, line_height=1)

    add_wrapped_text(c, 150, 722, f"{contract_data['quantity']} TONELADAS MÉTRICAS", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 710, f"R${contract_data['price']}/TONELADA MÉTRICA", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 698, f"{contract_data['payment']}", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 686, f"{contract_data['weight_quality']}", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 150, 674, f"{contract_data['delivery']}", 9, max_width=200, line_height=1)
    add_wrapped_text(c, 27, 620, "Trigo isento de insetos vivos e/ou mortos (caso haja incidência, as cargas serão devolvidas, e o vendedor será responsável pelo custo do frete).", 
                    10, max_width=550, line_height=12)

def additional_text(c, contract_data):
    if 'additional_fields' not in contract_data:
        return

    additional_fields = contract_data['additional_fields']
    if isinstance(additional_fields, str):
        try:
            additional_fields = json.loads(additional_fields)
        except:
            return
    
    if not additional_fields:
        return

    # Obter as chaves e valores dos campos adicionais (limitados a 5 campos)
    field_keys = list(additional_fields.keys())[:5]
    field_values = list(additional_fields.values())[:5]
    
    # Preencher arrays com strings vazias para garantir 5 elementos
    field_keys = field_keys + [""] * (5 - len(field_keys))
    field_values = field_values + [""] * (5 - len(field_values))
    
    # Nomes dos campos (mantendo as posições exatas)
    add_wrapped_text(c, 55, 708, field_keys[0], 9, max_width=80, line_height=1)
    add_wrapped_text(c, 150, 708, field_keys[1], 9, max_width=60, line_height=1)
    add_wrapped_text(c, 213, 708, field_keys[2], 9, max_width=60, line_height=1)
    add_wrapped_text(c, 278, 708, field_keys[3], 9, max_width=60, line_height=1)
    add_wrapped_text(c, 344, 708, field_keys[4], 9, max_width=60, line_height=1)

    # Valores dos campos (mantendo as posições exatas)
    add_wrapped_text(c, 40, 679, str(field_values[0]), 8, max_width=100, line_height=1)
    add_wrapped_text(c, 155, 678, str(field_values[1]), 8, max_width=100, line_height=1)
    add_wrapped_text(c, 225, 678, str(field_values[2]), 8, max_width=100, line_height=1)
    add_wrapped_text(c, 285, 678, str(field_values[3]), 8, max_width=100, line_height=1)
    add_wrapped_text(c, 359, 678, str(field_values[4]), 8, max_width=100, line_height=1)

def obs_text(c, obs_list, contract_data):
    isSb = "SB" in contract_data['contract_type'] or "CO" in contract_data['contract_type']
    if (isSb):
        y = 454
    else:
        y = 595
    for obs in obs_list:
        used_height = add_wrapped_text(c, 27, y, obs, 10, max_width=550, line_height=12)
        y -= used_height + 5

def payment_info_text(c, contract_data):
    seller = get_client_data(contract_data["seller_id"])

    add_wrapped_text(c, 138, 692, f"BANCO: {seller['bank']}", 7, max_width=200, line_height=1)
    add_wrapped_text(c, 308, 692, f"{seller['agency']}", 7, max_width=100, line_height=1)
    add_wrapped_text(c, 408, 692, f"{seller['account']}", 7, max_width=100, line_height=1)
    add_wrapped_text(c, 138, 679, f"{seller['name']}", 7, max_width=100, line_height=1)
    add_wrapped_text(c, 298, 679, f"{seller['cnpj']}", 7, max_width=100, line_height=1)
    add_wrapped_text(c, 138, 658, f"CIF {contract_data['delivPlace']}", 7, max_width=150, line_height=1)
    add_wrapped_text(c, 290, 658, f"{contract_data['stateDelivPlace']}", 7, max_width=100, line_height=1)
    add_overlay_text(c, 138, 634, f"0,20% sobre o valor da operação, a ser pago pela Vendedora", 7)

def signing_text(c, contract_data):
    seller = get_client_data(contract_data['seller_id'])
    buyer = get_client_data(contract_data['buyer_id'])

    vendedor_height = add_wrapped_text(c, 40, 425, f"{seller['name']}", 7, max_width=180, line_height=1)
    add_wrapped_text(c, 81, 425 - vendedor_height * 6 - 5, f"{seller['cnpj']}", 7, max_width=200, line_height=1)
    comprador_height = add_wrapped_text(c, 345, 425, f"{buyer['name']}", 7, max_width=180, line_height=1)
    add_wrapped_text(c, 400, 425 - comprador_height * 6 - 5, f"{buyer['cnpj']}", 7, max_width=200, line_height=1)

def createPDF(contract_data):
    isSb = "SB" in contract_data['contract_type'] or "CO" in contract_data['contract_type']

    seller = get_client_data(contract_data["seller_id"])
    buyer = get_client_data(contract_data["buyer_id"])
    year = get_separate_date(contract_data["contract_date"])
    
    filename = f"CTRVend_{contract_data['contract_number']}{contract_data["contract_type"]}{year} - {seller['name']} x {buyer['name']}.pdf"

    # Background images path
    image_page1 = "CONTRATO MODELO SB & CO_page-0001.jpg"

    if (isSb):
        # SB/CO model
        image_page2 = "CONTRATO MODELO SB & CO_page-0002.jpg"
    else:
        # WH model
        image_page2 = "CONTRATO MODELO WH_page-0002.jpg"

    image_page3 = "CONTRATO MODELO SB & CO_page-0003.jpg"
    image_page4 = "CONTRATO MODELO SB & CO_page-0004.jpg"

    # Create a PDF using canvas
    c = canvas.Canvas(filename, pagesize=A4)

    # Page 1
    add_background(c, image_page1)

    info_text(c, contract_data)
    
    c.showPage() 

    # Page 2
    add_background(c, image_page2)

    if (isSb):
        sb_co_text(c, contract_data)
        additional_text(c, contract_data)
    else:
        wh_text(c, contract_data)

    observacoes = [
        "Observação curta.",
        "Observação bem mais longa que provavelmente vai ocupar mais de uma linha dependendo da largura da caixa.",
        "Outra observação compacta.",
        "Uma ainda mais longa para testar se o recuo vertical funciona corretamente ao empilhar vários blocos de texto grandes.",
    ]
    
    obs_text(c, observacoes, contract_data)

    c.showPage()

    # Page 3
    add_background(c, image_page3)

    payment_info_text(c, contract_data)
    signing_text(c, contract_data)

    c.showPage()

    # Page 4
    add_background(c, image_page4)
    c.showPage()

    # Save the PDF
    c.save()
    print("created pdf file")

if __name__ == "__main__":
    createPDF("output.pdf")