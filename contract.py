from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QLineEdit, 
                             QComboBox, QTableWidget, QHBoxLayout, QFormLayout, QTextEdit, QStackedWidget)
from pdf import createPDF
import sqlite3
from database import create_contracts_db
import json
import os

class FocusAwareLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursorPosition(0)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.setCursorPosition(0)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if not self.hasSelectedText():
            self.setCursorPosition(0)

if not os.path.exists('contracts.db'):
    print("Banco de dados 'contracts.db' não encontrado. Criando...")
    create_contracts_db()
else:
    print("Banco de dados 'contracts.db' já existe. Verificando tabelas...")
    create_contracts_db()

class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # setting the window size
        width = 640
        height = 480

        # setting a fixed size for the app (unable to resize)
        self.setFixedSize(width, height)

        # window title
        self.setWindowTitle("Contratos")

        # layout
        layout = QVBoxLayout()
        
        btnCreate = QPushButton("Criar Contrato")
        btnEdit = QPushButton("Editar Contrato")
        btnExit = QPushButton("Sair da Janela")

        layout.addWidget(btnCreate)
        layout.addWidget(btnEdit)
        layout.addWidget(btnExit)

        btnCreate.clicked.connect(self.createContract)
        btnEdit.clicked.connect(self.editContract)
        btnExit.clicked.connect(self.close)

        self.setLayout(layout)
    
    def createContract(self):
        self.contract_window = ContractWindow()
        self.contract_window.show()

    def editContract(self):
        QMessageBox.information(self, "Editar Contrato", "Funcionalidade em desenvolvimento.")

class ContractWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowTitle("Criar Contrato")
        self.setFixedSize(800, 600)

        # Layout principal
        layout = QVBoxLayout()

        # Widget de páginas
        self.stackedWidget = QStackedWidget()
        layout.addWidget(self.stackedWidget)

        # Página 1: Informações básicas
        self.page1 = self.createPage1()
        self.stackedWidget.addWidget(self.page1)

        # Página 2: Produto e Safra
        self.page2 = self.createPage2()
        self.stackedWidget.addWidget(self.page2)

        # Página 3: Detalhes específicos do tipo de contrato
        self.page3 = self.createPage3()
        self.stackedWidget.addWidget(self.page3)

        # Página 4: Quantidade, Preço, Pagamento, Peso/Qualidade, Entrega/Retirada
        self.page4 = self.createPage4()
        self.stackedWidget.addWidget(self.page4)

        # Página 5: Observações
        self.page5 = self.createPage5()
        self.stackedWidget.addWidget(self.page5)

        # Botões de navegação
        btn_layout = QHBoxLayout()
        self.btnPrevious = QPushButton("Anterior", self)
        self.btnNext = QPushButton("Próximo", self)
        self.btnPrevious.clicked.connect(self.previousPage)
        self.btnNext.clicked.connect(self.nextPage)
        btn_layout.addWidget(self.btnPrevious)
        btn_layout.addWidget(self.btnNext)
        layout.addLayout(btn_layout)

        # Botão para salvar contrato
        btnSave = QPushButton("Salvar Contrato", self)
        btnSave.clicked.connect(self.saveContract)
        layout.addWidget(btnSave)

        # Definir layout
        self.setLayout(layout)

        # Atualizar a Página 3 com os campos do tipo de contrato padrão (Soja)
        self.updatePage3()

    def createPage1(self):
        # Página 1: Informações básicas
        page = QWidget()
        layout = QFormLayout()

        # Número do contrato
        self.txtContractNumber = QLineEdit(page)
        layout.addRow("Número do Contrato:", self.txtContractNumber)

        # Tipo do contrato
        self.cmbType = QComboBox(page)
        self.cmbType.addItems(["SB", "WH", "CO"])
        self.cmbType.currentTextChanged.connect(self.updatePage3)  # Atualizar Página 3 ao mudar o tipo
        layout.addRow("Tipo do Contrato:", self.cmbType)

        # Data do contrato
        self.txtDate = FocusAwareLineEdit(page)
        self.txtDate.setPlaceholderText("DD/MM/AAAA")
        self.txtDate.setInputMask("99/99/9999")
        layout.addRow("Data do Contrato:", self.txtDate)

        # Vendedor
        self.cmbSeller = QComboBox(page)
        self.loadClients(self.cmbSeller)
        layout.addRow("Vendedor:", self.cmbSeller)

        # Comprador
        self.cmbBuyer = QComboBox(page)
        self.loadClients(self.cmbBuyer)
        layout.addRow("Comprador:", self.cmbBuyer)

        page.setLayout(layout)
        return page

    def createPage2(self):
        # Página 2: Produto e Safra
        page = QWidget()
        layout = QFormLayout()

        # Produto
        self.txtProduct = QLineEdit(page)
        layout.addRow("Produto:", self.txtProduct)

        # Safra
        self.txtHarvest = QLineEdit(page)
        layout.addRow("Safra:", self.txtHarvest)

        page.setLayout(layout)
        return page

    def createPage3(self):
        # Página 3: Detalhes específicos do tipo de contrato
        page = QWidget()
        layout = QVBoxLayout()

        # Layout dinâmico para campos específicos
        self.dynamicLayout = QFormLayout()
        layout.addLayout(self.dynamicLayout)

        # Botão para adicionar campo adicional
        btnAddField = QPushButton("Adicionar Campo Adicional", page)
        btnAddField.clicked.connect(self.addAdditionalField)
        layout.addWidget(btnAddField)

        page.setLayout(layout)
        return page

    def updatePage3(self):
        # Atualizar a Página 3 com campos específicos do tipo de contrato
        self.clearDynamicLayout()

        contract_type = self.cmbType.currentText()

        if "SB" in contract_type:
            self.addField("Umidade Máxima:")
            self.addField("Impureza Máxima:")
            self.addField("Ardidos e Avariados:")
        elif "WH" in contract_type:
            self.addField("Falling Number:")
            self.addField("Impureza Máxima:")
            self.addField("Umidade Máxima:")
            self.addField("P/L:")
            self.addField("PH Mínimo:")
            self.addField("W Mínimo:")
            self.addField("Triguilho:")
        elif "CO" in contract_type:
            self.addField("Umidade Máxima:")
            self.addField("Impureza Máxima:")
            self.addField("Ardidos e Avariados:")

    def clearDynamicLayout(self):
        # Limpar todos os campos dinâmicos
        while self.dynamicLayout.rowCount() > 0:
            self.dynamicLayout.removeRow(0)

    def addField(self, label):
        # Adicionar campo específico ao layout dinâmico
        field = QLineEdit(self)
        self.dynamicLayout.addRow(label, field)

    def addAdditionalField(self):
        # Adicionar campo adicional dinâmico
        field_name = QLineEdit(self)
        field_value = QLineEdit(self)
        self.dynamicLayout.addRow(field_name, field_value)

    def createPage4(self):
        # Página 4: Quantidade, Preço, Pagamento, Peso/Qualidade, Entrega/Retirada
        page = QWidget()
        layout = QFormLayout()

        # Quantidade
        self.txtQuantity = QLineEdit(page)
        layout.addRow("Quantidade (em tons):", self.txtQuantity)

        # Preço
        self.txtPrice = QLineEdit(page)
        layout.addRow("Preço:", self.txtPrice)

        # Pagamento
        self.txtPayment = QLineEdit(page)
        layout.addRow("Pagamento:", self.txtPayment)

        # Peso/Qualidade
        self.txtWeightQuality = QLineEdit(page)
        layout.addRow("Peso/Qualidade:", self.txtWeightQuality)

        # Entrega/Retirada
        self.txtDelivery = QLineEdit(page)
        layout.addRow("Entrega/Retirada:", self.txtDelivery)

        # Lugar de entrega
        self.txtDelivPlace = QLineEdit(page)
        layout.addRow("Lugar de entrega/retirada:", self.txtDelivPlace)
        self.txtStateDelivPlace = QLineEdit(page)
        self.txtStateDelivPlace.setInputMask("AA")
        layout.addRow("Estado do lugar de entrega/retirada:", self.txtStateDelivPlace)

        page.setLayout(layout)
        return page

    def createPage5(self):
        # Página 5: Observações
        page = QWidget()
        layout = QVBoxLayout()

        # Observações
        self.txtObservations = QTextEdit(page)
        layout.addWidget(QLabel("Observações:"))
        layout.addWidget(self.txtObservations)

        page.setLayout(layout)
        return page

    def loadClients(self, combo_box):
    # Carregar todos os clientes do banco de dados
        try:
            conn = sqlite3.connect('clients.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM clients')  # Removido o filtro por tipo
            clients = cursor.fetchall()
            conn.close()

            # Adicionar item vazio no início
            combo_box.clear()
            combo_box.addItem("", None)

            # Adicionar clientes ao combobox
            for client in clients:
                combo_box.addItem(client[1], client[0])  # Nome do cliente e ID
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar clientes: {e}")

    def previousPage(self):
        # Navegar para a página anterior
        current_index = self.stackedWidget.currentIndex()
        if current_index > 0:
            self.stackedWidget.setCurrentIndex(current_index - 1)

    def nextPage(self):
        # Navegar para a próxima página
        current_index = self.stackedWidget.currentIndex()
        if current_index < self.stackedWidget.count() - 1:
            self.stackedWidget.setCurrentIndex(current_index + 1)

    def saveContract(self):
        if not self.cmbSeller.currentData() or not self.cmbBuyer.currentData():
            QMessageBox.warning(self, "Erro", "Selecione vendedor e comprador.")
            return

        contract_type = self.cmbType.currentText()

        contract_data = {
            "contract_number": self.txtContractNumber.text(),
            "contract_type": contract_type,
            "contract_date": self.txtDate.text(),
            "seller_id": self.cmbSeller.currentData(),
            "buyer_id": self.cmbBuyer.currentData(),
            "product": self.txtProduct.text(),
            "harvest": self.txtHarvest.text(),
            "quantity": self.txtQuantity.text(),
            "price": self.txtPrice.text(),
            "payment": self.txtPayment.text(),
            "weight_quality": self.txtWeightQuality.text(),
            "delivery": self.txtDelivery.text(),
            "observations": self.txtObservations.toPlainText(),
            "delivPlace": self.txtDelivPlace.text(),
            "stateDelivPlace": self.txtStateDelivPlace.text()
        }

        quality_params = {}
        additional_fields = {}
        
        for i in range(self.dynamicLayout.rowCount()):
            label = self.dynamicLayout.itemAt(i, QFormLayout.ItemRole.LabelRole)
            field = self.dynamicLayout.itemAt(i, QFormLayout.ItemRole.FieldRole)
            if label and field:
                label_widget = label.widget()
                field_widget = field.widget()

                if isinstance(label_widget, QLineEdit):
                    field_name = label_widget.text()
                    field_value = field_widget.text()
                    additional_fields[field_name] = field_value
                else:
                    field_name = label.widget().text().replace(":", "").strip()
                    field_value = field.widget().text()
                
                    if contract_type in ("SB", "CO"):
                        if field_name == "Umidade Máxima":
                            quality_params["umidade_maxima"] = field_value
                        elif field_name == "Impureza Máxima":
                            quality_params["impureza_maxima"] = field_value
                        elif field_name == "Ardidos e Avariados":
                            quality_params["ardidos_avariados"] = field_value
                        else:
                            additional_fields[field_name] = field_value
                    elif contract_type == "WH":
                        if field_name == "Falling Number":
                            quality_params["falling_number"] = field_value
                        elif field_name == "Impureza Máxima":
                            quality_params["impureza_maxima"] = field_value
                        elif field_name == "Umidade Máxima":
                            quality_params["umidade_maxima"] = field_value
                        elif field_name == "P/L":
                            quality_params["pl_minimo"] = field_value
                        elif field_name == "PH Mínimo":
                            quality_params["ph"] = field_value
                        elif field_name == "W Mínimo":
                            quality_params["w_minimo"] = field_value
                        elif field_name == "Triguilho":
                            quality_params["triguilho"] = field_value

        columns = [
            "contract_number", "contract_type", "contract_date",
            "seller_id", "buyer_id", "product", "harvest",
            "quantity", "price", "payment", "weight_quality",
            "delivery", "observations", "delivPlace", "stateDelivPlace"
        ]
        values = [
            contract_data["contract_number"],
            contract_data["contract_type"],
            contract_data["contract_date"],
            contract_data["seller_id"],
            contract_data["buyer_id"],
            contract_data["product"],
            contract_data["harvest"],
            contract_data["quantity"],
            contract_data["price"],
            contract_data["payment"],
            contract_data["weight_quality"],
            contract_data["delivery"],
            contract_data["observations"],
            contract_data["delivPlace"],
            contract_data["stateDelivPlace"]
        ]

        if contract_type in ("SB", "CO"):
            columns.extend(["umidade_maxima", "impureza_maxima", "ardidos_avariados"])
            values.extend([
                quality_params.get("umidade_maxima", ""),
                quality_params.get("impureza_maxima", ""),
                quality_params.get("ardidos_avariados", "")
            ])
        elif contract_type == "WH":
            columns.extend([
                "falling_number", "impureza_maxima", "umidade_maxima",
                "pl_minimo", "ph", "w_minimo", "triguilho"
            ])
            values.extend([
                quality_params.get("falling_number", ""),
                quality_params.get("impureza_maxima", ""),
                quality_params.get("umidade_maxima", ""),
                quality_params.get("pl_minimo", ""),
                quality_params.get("ph", ""),
                quality_params.get("w_minimo", ""),
                quality_params.get("triguilho", "")
            ])

        if additional_fields:
            columns.append("additional_fields")
            values.append(json.dumps(additional_fields))

        try:
            conn = sqlite3.connect('contracts.db')
            cursor = conn.cursor()
            
            query = f'''
            INSERT INTO contracts ({", ".join(columns)})
            VALUES ({", ".join(["?"]*len(columns))})
            '''
            cursor.execute(query, values)
            conn.commit()
            
            # Generate PDF with complete data
            pdf_data = {**contract_data, **quality_params}
            if additional_fields:
                pdf_data["additional_fields"] = additional_fields
            createPDF(pdf_data)
            
            QMessageBox.information(self, "Sucesso", "Contrato salvo com sucesso!")
            self.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar contrato: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar PDF: {e}")
        finally:
            conn.close()