from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QLineEdit, 
                             QComboBox, QTableWidget, QHBoxLayout, QFormLayout, QTextEdit, QStackedWidget, QTableWidgetItem)
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
        self.selection_window = ContractSelectionWindow()
        self.selection_window.show()

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
            cursor.execute('SELECT id, name, city FROM clients')  # Removido o filtro por tipo
            clients = cursor.fetchall()
            conn.close()

            # Adicionar item vazio no início
            combo_box.clear()
            combo_box.addItem("", None)

            # Adicionar clientes ao combobox
            for client in clients:
                client_id = client[0]
                client_name = client[1]
                client_city = client[2] if client[2] else ""

                if client_city:
                    display_text = f"{client_name} ({client_city})"
                else:
                    display_text = client_name
                
                combo_box.addItem(display_text, client_id)

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

# Adicione estas classes ao seu arquivo contract.py

class ContractSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Selecionar Contrato para Editar")
        self.setFixedSize(800, 600)
        
        layout = QVBoxLayout()
        
        # Label de instruções
        label = QLabel("Selecione o contrato que deseja editar:")
        layout.addWidget(label)
        
        # Tabela para mostrar contratos
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Número", "Tipo", "Data", "Vendedor", "Comprador"
        ])
        
        # Ajustar largura das colunas
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 200)
        self.table.setColumnWidth(5, 200)
        
        layout.addWidget(self.table)
        
        # Botões
        btn_layout = QHBoxLayout()
        
        btnEdit = QPushButton("Editar Selecionado")
        btnRefresh = QPushButton("Atualizar Lista")
        btnClose = QPushButton("Fechar")
        
        btnEdit.clicked.connect(self.editSelectedContract)
        btnRefresh.clicked.connect(self.loadContracts)
        btnClose.clicked.connect(self.close)
        
        btn_layout.addWidget(btnEdit)
        btn_layout.addWidget(btnRefresh)
        btn_layout.addWidget(btnClose)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        # Carregar contratos ao abrir
        self.loadContracts()
    
    def loadContracts(self):
        try:
            conn = sqlite3.connect('contracts.db')
            cursor = conn.cursor()
            
            # Anexar o banco de dados clients.db
            cursor.execute("ATTACH DATABASE 'clients.db' AS clientsdb")
            
            # Query modificada para usar o banco anexado
            cursor.execute('''
                SELECT c.id, c.contract_number, c.contract_type, c.contract_date,
                    s.name as seller_name, b.name as buyer_name
                FROM contracts c
                LEFT JOIN clientsdb.clients s ON c.seller_id = s.id
                LEFT JOIN clientsdb.clients b ON c.buyer_id = b.id
                ORDER BY c.contract_number 
            ''')
            
            contracts = cursor.fetchall()
            conn.close()
            
            # Limpar tabela (MANTENHA ESTAS LINHAS)
            self.table.setRowCount(0)
            
            # Adicionar contratos à tabela (MANTENHA ESTAS LINHAS)
            for row, contract in enumerate(contracts):
                self.table.insertRow(row)
                for col, data in enumerate(contract):
                    self.table.setItem(row, col, QTableWidgetItem(str(data or "")))
        
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar contratos: {e}")
    
    def editSelectedContract(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um contrato para editar.")
            return
        
        try:
            contract_id = int(self.table.item(current_row, 0).text())  # Converta para int
            self.edit_window = ContractEditWindow(contract_id)
            self.edit_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao abrir editor: {str(e)}")


class ContractEditWindow(ContractWindow):
    def __init__(self, contract_id):
        try:
            self.contract_id = contract_id
            super().__init__()
            self.setWindowTitle(f"Editar Contrato - ID: {contract_id}")
            self.loadContractData()
        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Falha ao inicializar editor: {str(e)}")
            raise  # Remove isso depois de debugar
    
    def loadContractData(self):
        try:
            conn = sqlite3.connect('contracts.db')
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM contracts WHERE id = ?', (self.contract_id,))
            contract = cursor.fetchone()
            
            if not contract:
                QMessageBox.critical(self, "Erro", "Contrato não encontrado.")
                self.close()
                return
            
            # Obter nomes das colunas
            cursor.execute("PRAGMA table_info(contracts)")
            columns = [column[1] for column in cursor.fetchall()]
            
            conn.close()
            
            # Criar dicionário com os dados
            contract_dict = dict(zip(columns, contract))
            
            # Preencher campos - Página 1
            self.txtContractNumber.setText(contract_dict.get('contract_number', ''))
            
            # Definir tipo de contrato
            contract_type = contract_dict.get('contract_type', 'SB')
            type_index = self.cmbType.findText(contract_type)
            if type_index >= 0:
                self.cmbType.setCurrentIndex(type_index)
            
            self.txtDate.setText(contract_dict.get('contract_date', ''))
            
            # Definir vendedor e comprador
            seller_id = contract_dict.get('seller_id')
            buyer_id = contract_dict.get('buyer_id')
            
            if seller_id:
                for i in range(self.cmbSeller.count()):
                    if self.cmbSeller.itemData(i) == seller_id:
                        self.cmbSeller.setCurrentIndex(i)
                        break
            
            if buyer_id:
                for i in range(self.cmbBuyer.count()):
                    if self.cmbBuyer.itemData(i) == buyer_id:
                        self.cmbBuyer.setCurrentIndex(i)
                        break
            
            # Preencher campos - Página 2
            self.txtProduct.setText(contract_dict.get('product', ''))
            self.txtHarvest.setText(contract_dict.get('harvest', ''))
            
            # Preencher campos - Página 4
            self.txtQuantity.setText(contract_dict.get('quantity', ''))
            self.txtPrice.setText(contract_dict.get('price', ''))
            self.txtPayment.setText(contract_dict.get('payment', ''))
            self.txtWeightQuality.setText(contract_dict.get('weight_quality', ''))
            self.txtDelivery.setText(contract_dict.get('delivery', ''))
            self.txtDelivPlace.setText(contract_dict.get('delivPlace', ''))
            self.txtStateDelivPlace.setText(contract_dict.get('stateDelivPlace', ''))
            
            # Preencher campos - Página 5
            self.txtObservations.setPlainText(contract_dict.get('observations', ''))
            
            # Aguardar a página 3 ser atualizada e depois preencher os campos específicos
            self.fillSpecificFields(contract_dict)
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar dados do contrato: {e}")
    
    def fillSpecificFields(self, contract_dict):
        # Aguardar um momento para que os campos sejam criados
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, lambda: self._fillSpecificFieldsDelayed(contract_dict))
    
    def _fillSpecificFieldsDelayed(self, contract_dict):
        contract_type = contract_dict.get('contract_type', 'SB')
        
        # Mapeamento dos campos específicos
        field_mapping = {}
        
        if contract_type in ("SB", "CO"):
            field_mapping = {
                "Umidade Máxima:": contract_dict.get('umidade_maxima', ''),
                "Impureza Máxima:": contract_dict.get('impureza_maxima', ''),
                "Ardidos e Avariados:": contract_dict.get('ardidos_avariados', '')
            }
        elif contract_type == "WH":
            field_mapping = {
                "Falling Number:": contract_dict.get('falling_number', ''),
                "Impureza Máxima:": contract_dict.get('impureza_maxima', ''),
                "Umidade Máxima:": contract_dict.get('umidade_maxima', ''),
                "P/L:": contract_dict.get('pl_minimo', ''),
                "PH Mínimo:": contract_dict.get('ph', ''),
                "W Mínimo:": contract_dict.get('w_minimo', ''),
                "Triguilho:": contract_dict.get('triguilho', '')
            }
        
        # Preencher campos específicos
        for i in range(self.dynamicLayout.rowCount()):
            label_item = self.dynamicLayout.itemAt(i, QFormLayout.ItemRole.LabelRole)
            field_item = self.dynamicLayout.itemAt(i, QFormLayout.ItemRole.FieldRole)
            
            if label_item and field_item:
                label_widget = label_item.widget()
                field_widget = field_item.widget()
                
                if isinstance(label_widget, QLabel):
                    label_text = label_widget.text()
                    if label_text in field_mapping:
                        field_widget.setText(field_mapping[label_text])
        
        # Preencher campos adicionais se existirem
        additional_fields_json = contract_dict.get('additional_fields')
        if additional_fields_json:
            try:
                additional_fields = json.loads(additional_fields_json)
                # Aqui você pode implementar a lógica para adicionar campos extras
                # se necessário
            except json.JSONDecodeError:
                pass
    
    def saveContract(self):
        # Validação básica
        if not self.cmbSeller.currentData() or not self.cmbBuyer.currentData():
            QMessageBox.warning(self, "Erro", "Selecione vendedor e comprador.")
            return
        
        contract_type = self.cmbType.currentText()
        
        # Preparar dados para atualização
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
        
        # Coletar parâmetros de qualidade
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
        
        try:
            conn = sqlite3.connect('contracts.db')
            cursor = conn.cursor()
            
            # Preparar campos para UPDATE
            update_fields = []
            update_values = []
            
            # Campos básicos
            for key, value in contract_data.items():
                update_fields.append(f"{key} = ?")
                update_values.append(value)
            
            # Campos de qualidade específicos
            if contract_type in ("SB", "CO"):
                quality_fields = ["umidade_maxima", "impureza_maxima", "ardidos_avariados"]
                for field in quality_fields:
                    update_fields.append(f"{field} = ?")
                    update_values.append(quality_params.get(field, ""))
                
                # Limpar campos de wheat
                wheat_fields = ["falling_number", "pl_minimo", "ph", "w_minimo", "triguilho"]
                for field in wheat_fields:
                    update_fields.append(f"{field} = ?")
                    update_values.append("")
                    
            elif contract_type == "WH":
                wheat_fields = ["falling_number", "impureza_maxima", "umidade_maxima", 
                               "pl_minimo", "ph", "w_minimo", "triguilho"]
                for field in wheat_fields:
                    update_fields.append(f"{field} = ?")
                    update_values.append(quality_params.get(field, ""))
                
                # Limpar campos de soja/milho
                soy_corn_fields = ["ardidos_avariados"]
                for field in soy_corn_fields:
                    update_fields.append(f"{field} = ?")
                    update_values.append("")
            
            # Campos adicionais
            if additional_fields:
                update_fields.append("additional_fields = ?")
                update_values.append(json.dumps(additional_fields))
            else:
                update_fields.append("additional_fields = ?")
                update_values.append("")
            
            # Adicionar ID para WHERE clause
            update_values.append(self.contract_id)
            
            # Executar UPDATE
            query = f"UPDATE contracts SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, update_values)
            conn.commit()
            
            # Gerar PDF atualizado
            pdf_data = {**contract_data, **quality_params}
            if additional_fields:
                pdf_data["additional_fields"] = additional_fields
            createPDF(pdf_data)
            
            QMessageBox.information(self, "Sucesso", "Contrato atualizado com sucesso!")
            self.close()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao atualizar contrato: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar PDF: {e}")
        finally:
            conn.close()