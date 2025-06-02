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
        
        width = 640
        height = 480
        self.setFixedSize(width, height)
        self.setWindowTitle("Contratos")

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
        self.setWindowTitle("Criar Contrato")
        self.setFixedSize(800, 600)

        self.default_values = {
            "SB": {
                "Umidade Máxima": "14",
                "Impureza Máxima": "1 %",
                "Ardidos e Avariados": "8"
            },
            "WH": {
                "Falling Number": "250",
                "Impureza Máxima": "1",
                "Umidade Máxima": "13",
                "P/L": "1",
                "PH Mínimo": "78",
                "W Mínimo": "250",
                "Triguilho": "1,5"
            },
            "CO": {
                "Umidade Máxima": "14",
                "Impureza Máxima": "1 %",
                "Ardidos e Avariados": "8"
            }
        }

        layout = QVBoxLayout()
        self.stackedWidget = QStackedWidget()
        layout.addWidget(self.stackedWidget)

        self.page1 = self.createPage1()
        self.page2 = self.createPage2()
        self.page3 = self.createPage3()
        self.page4 = self.createPage4()
        self.page5 = self.createPage5()

        self.stackedWidget.addWidget(self.page1)
        self.stackedWidget.addWidget(self.page2)
        self.stackedWidget.addWidget(self.page3)
        self.stackedWidget.addWidget(self.page4)
        self.stackedWidget.addWidget(self.page5)

        btn_layout = QHBoxLayout()
        self.btnPrevious = QPushButton("Anterior", self)
        self.btnNext = QPushButton("Próximo", self)
        self.btnPrevious.clicked.connect(self.previousPage)
        self.btnNext.clicked.connect(self.nextPage)
        btn_layout.addWidget(self.btnPrevious)
        btn_layout.addWidget(self.btnNext)
        layout.addLayout(btn_layout)

        btnSave = QPushButton("Salvar Contrato", self)
        btnSave.clicked.connect(self.saveContract)
        layout.addWidget(btnSave)

        self.setLayout(layout)
        self.updatePage3()

    def createPage1(self):
        page = QWidget()
        layout = QFormLayout()

        self.txtContractNumber = QLineEdit(page)
        layout.addRow("Número do Contrato:", self.txtContractNumber)

        self.cmbType = QComboBox(page)
        self.cmbType.addItems(["SB", "WH", "CO"])
        self.cmbType.currentTextChanged.connect(self.updatePage3)
        layout.addRow("Tipo do Contrato:", self.cmbType)

        self.txtDate = FocusAwareLineEdit(page)
        self.txtDate.setPlaceholderText("DD/MM/AAAA")
        self.txtDate.setInputMask("99/99/9999")
        layout.addRow("Data do Contrato:", self.txtDate)

        self.cmbSeller = QComboBox(page)
        self.loadClients(self.cmbSeller)
        layout.addRow("Vendedor:", self.cmbSeller)

        self.cmbBuyer = QComboBox(page)
        self.loadClients(self.cmbBuyer)
        layout.addRow("Comprador:", self.cmbBuyer)

        page.setLayout(layout)
        return page

    def createPage2(self):
        page = QWidget()
        layout = QFormLayout()

        self.txtProduct = QLineEdit(page)
        layout.addRow("Produto:", self.txtProduct)

        self.txtHarvest = QLineEdit(page)
        layout.addRow("Safra:", self.txtHarvest)

        page.setLayout(layout)
        return page

    def createPage3(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.dynamicLayout = QFormLayout()
        layout.addLayout(self.dynamicLayout)

        self.additional_fields_inputs = []

        btnAddField = QPushButton("Adicionar Campo Adicional", page)
        btnAddField.clicked.connect(self.addAdditionalField)
        layout.addWidget(btnAddField)

        page.setLayout(layout)
        return page

    def addAdditionalField(self):
        field_name = QLineEdit(self)
        field_value = QLineEdit(self)
        row = self.dynamicLayout.rowCount()
        self.dynamicLayout.insertRow(row, field_name, field_value)
        self.additional_fields_inputs.append((field_name, field_value))

    def updatePage3(self):
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
        while self.dynamicLayout.rowCount() > 0:
            self.dynamicLayout.removeRow(0)
        self.additional_fields_inputs = []

    def addField(self, label):
        field = QLineEdit(self)
        contract_type = self.cmbType.currentText()
    
        # Preenche com valor padrão se existir
        if contract_type in self.default_values and label.replace(":", "") in self.default_values[contract_type]:
            default_value = self.default_values[contract_type][label.replace(":", "")]
            field.setText(default_value)

        self.dynamicLayout.addRow(label, field)

    def createPage4(self):
        page = QWidget()
        layout = QFormLayout()

        self.txtQuantity = QLineEdit(page)
        layout.addRow("Quantidade (em tons):", self.txtQuantity)

        self.txtPrice = QLineEdit(page)
        layout.addRow("Preço:", self.txtPrice)

        self.txtPayment = QLineEdit(page)
        layout.addRow("Pagamento:", self.txtPayment)

        self.txtWeightQuality = QLineEdit(page)
        layout.addRow("Peso/Qualidade:", self.txtWeightQuality)

        self.txtDelivery = QLineEdit(page)
        layout.addRow("Entrega/Retirada:", self.txtDelivery)

        self.txtDelivPlace = QLineEdit(page)
        layout.addRow("Lugar de entrega/retirada:", self.txtDelivPlace)
        self.txtStateDelivPlace = QLineEdit(page)
        self.txtStateDelivPlace.setInputMask("AA")
        layout.addRow("Estado do lugar de entrega/retirada:", self.txtStateDelivPlace)

        self.textCommission = QLineEdit(page)
        layout.addRow("Comissão:", self.textCommission)

        page.setLayout(layout)
        return page

    def createPage5(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.txtObservations = QTextEdit(page)
        layout.addWidget(QLabel("Observações:"))
        layout.addWidget(self.txtObservations)

        page.setLayout(layout)
        return page

    def loadClients(self, combo_box):
        try:
            conn = sqlite3.connect('clients.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, city FROM clients')
            clients = cursor.fetchall()
            conn.close()

            combo_box.clear()
            combo_box.addItem("", None)

            for client in clients:
                client_id = client[0]
                client_name = client[1]
                client_city = client[2] if client[2] else ""
                display_text = f"{client_name} ({client_city})" if client_city else client_name
                combo_box.addItem(display_text, client_id)

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar clientes: {e}")

    def previousPage(self):
        current_index = self.stackedWidget.currentIndex()
        if current_index > 0:
            self.stackedWidget.setCurrentIndex(current_index - 1)

    def nextPage(self):
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
            "stateDelivPlace": self.txtStateDelivPlace.text(),
            "commission": self.textCommission.text(),
        }

        quality_params = {}
        additional_fields = {}

        for i in range(self.dynamicLayout.rowCount()):
            label = self.dynamicLayout.itemAt(i, QFormLayout.ItemRole.LabelRole)
            field = self.dynamicLayout.itemAt(i, QFormLayout.ItemRole.FieldRole)
            if label and field:
                label_widget = label.widget()
                field_widget = field.widget()

                if isinstance(label_widget, QLabel):
                    field_name = label_widget.text().replace(":", "").strip()
                    field_value = field_widget.text()

                    if contract_type in ("SB", "CO"):
                        if field_name == "Umidade Máxima":
                            quality_params["umidade_maxima"] = field_value
                        elif field_name == "Impureza Máxima":
                            quality_params["impureza_maxima"] = field_value
                        elif field_name == "Ardidos e Avariados":
                            quality_params["ardidos_avariados"] = field_value
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

        for field_name_input, field_value_input in self.additional_fields_inputs:
            field_name = field_name_input.text().strip()
            field_value = field_value_input.text().strip()
            if field_name:
                additional_fields[field_name] = field_value

        columns = [
            "contract_number", "contract_type", "contract_date",
            "seller_id", "buyer_id", "product", "harvest",
            "quantity", "price", "payment", "weight_quality",
            "delivery", "observations", "delivPlace", "stateDelivPlace", "commission"
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
            contract_data["stateDelivPlace"],
            contract_data["commission"]
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
            pdf_data = {**contract_data, **quality_params}
            if additional_fields:
                pdf_data["additional_fields"] = additional_fields
                
            pdf_path = createPDF(pdf_data, self)
            if not pdf_path:  # Usuário cancelou
                return

            # 2. Se PDF gerado com sucesso, salvar no banco
            try:
                conn = sqlite3.connect('contracts.db')
                cursor = conn.cursor()
                
                columns = list(contract_data.keys())
                values = list(contract_data.values())
                
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

                query = f'INSERT INTO contracts ({", ".join(columns)}) VALUES ({", ".join(["?"]*len(columns))})'
                cursor.execute(query, values)
                conn.commit()
                
                QMessageBox.information(self, "Sucesso", f"Contrato salvo com sucesso!\nPDF gerado em:\n{pdf_path}")
                self.close()
                
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar no banco de dados: {e}")
                try:
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
                except:
                    pass
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao gerar PDF: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

class ContractSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Selecionar Contrato para Editar")
        self.setFixedSize(800, 600)
        
        layout = QVBoxLayout()
        label = QLabel("Selecione o contrato que deseja editar:")
        layout.addWidget(label)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Número", "Tipo", "Data", "Vendedor", "Comprador"
        ])
        
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 200)
        self.table.setColumnWidth(5, 200)
        
        layout.addWidget(self.table)
        
        btn_layout = QHBoxLayout()
        btnEdit = QPushButton("Editar Selecionado")
        btnDelete = QPushButton("Excluir Selecionado")
        btnRefresh = QPushButton("Atualizar Lista")
        btnClose = QPushButton("Fechar")
        
        btnEdit.clicked.connect(self.editSelectedContract)
        btnDelete.clicked.connect(self.deleteSelectedContract)
        btnRefresh.clicked.connect(self.loadContracts)
        btnClose.clicked.connect(self.close)
        
        btn_layout.addWidget(btnEdit)
        btn_layout.addWidget(btnDelete)
        btn_layout.addWidget(btnRefresh)
        btn_layout.addWidget(btnClose)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.loadContracts()
    
    def loadContracts(self):
        try:
            conn = sqlite3.connect('contracts.db')
            cursor = conn.cursor()
            cursor.execute("ATTACH DATABASE 'clients.db' AS clientsdb")
            cursor.execute('''
                SELECT c.id, c.contract_number, c.contract_type, c.contract_date,
                    s.name as seller_name, b.name as buyer_name
                FROM contracts c
                LEFT JOIN clientsdb.clients s ON c.seller_id = s.id
                LEFT JOIN clientsdb.clients b ON c.buyer_id = b.id
                ORDER BY c.id 
            ''')
            
            contracts = cursor.fetchall()
            conn.close()
            
            self.table.setRowCount(0)
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
            contract_id = int(self.table.item(current_row, 0).text())
            contract_number = self.table.item(current_row, 1).text()
            contract_type = self.table.item(current_row, 2).text()
            self.edit_window = ContractEditWindow(contract_id, contract_number, contract_type)
            self.edit_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao abrir editor: {str(e)}")
    
    def deleteSelectedContract(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um contrato para excluir.")
            return
        
        try:
            contract_id = int(self.table.item(current_row, 0).text())
            contract_number = self.table.item(current_row, 1).text()
            
            # Confirmar com o usuário
            reply = QMessageBox.question(
                self, 
                "Confirmar Exclusão",
                f"Tem certeza que deseja excluir o contrato {contract_number}?\nEsta ação não pode ser desfeita.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                conn = sqlite3.connect('contracts.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM contracts WHERE id = ?', (contract_id,))
                conn.commit()
                conn.close()
                
                QMessageBox.information(self, "Sucesso", "Contrato excluído com sucesso.")
                self.loadContracts()  # Atualizar a lista
        
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao excluir contrato: {str(e)}")

class ContractEditWindow(ContractWindow):
    def __init__(self, contract_id, contract_number, contract_type):
        try:
            self.contract_id = contract_id
            super().__init__()
            self.setWindowTitle(f"Editar Contrato - Contrato: {contract_number}/{contract_type}")
            self.loadContractData()
        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Falha ao inicializar editor: {str(e)}")
            raise
    
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
            
            cursor.execute("PRAGMA table_info(contracts)")
            columns = [column[1] for column in cursor.fetchall()]
            conn.close()
            
            contract_dict = dict(zip(columns, contract))
            
            self.txtContractNumber.setText(contract_dict.get('contract_number', ''))
            
            contract_type = contract_dict.get('contract_type', 'SB')
            type_index = self.cmbType.findText(contract_type)
            if type_index >= 0:
                self.cmbType.setCurrentIndex(type_index)
            
            self.txtDate.setText(contract_dict.get('contract_date', ''))
            
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
            
            self.txtProduct.setText(contract_dict.get('product', ''))
            self.txtHarvest.setText(contract_dict.get('harvest', ''))
            
            self.txtQuantity.setText(contract_dict.get('quantity', ''))
            self.txtPrice.setText(contract_dict.get('price', ''))
            self.txtPayment.setText(contract_dict.get('payment', ''))
            self.txtWeightQuality.setText(contract_dict.get('weight_quality', ''))
            self.txtDelivery.setText(contract_dict.get('delivery', ''))
            self.txtDelivPlace.setText(contract_dict.get('delivPlace', ''))
            self.txtStateDelivPlace.setText(contract_dict.get('stateDelivPlace', ''))
            self.textCommission.setText(contract_dict.get('commission', ''))
            
            self.txtObservations.setPlainText(contract_dict.get('observations', ''))
            
            self.fillSpecificFields(contract_dict)
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar dados do contrato: {e}")
    
    def fillSpecificFields(self, contract_dict):
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, lambda: self._fillSpecificFieldsDelayed(contract_dict))
    
    def _fillSpecificFieldsDelayed(self, contract_dict):
        contract_type = contract_dict.get('contract_type', 'SB')
        
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
        
        additional_fields_json = contract_dict.get('additional_fields')
        if additional_fields_json:
            try:
                additional_fields = json.loads(additional_fields_json)
                for field_name, field_value in additional_fields.items():
                    self.addAdditionalField()
                    if self.additional_fields_inputs:
                        last_field = self.additional_fields_inputs[-1]
                        last_field[0].setText(field_name)
                        last_field[1].setText(str(field_value))
            except json.JSONDecodeError:
                pass
    
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
            "stateDelivPlace": self.txtStateDelivPlace.text(),
            "commission": self.textCommission.text(),
        }

        quality_params = {}
        additional_fields = {}

        for i in range(self.dynamicLayout.rowCount()):
            label = self.dynamicLayout.itemAt(i, QFormLayout.ItemRole.LabelRole)
            field = self.dynamicLayout.itemAt(i, QFormLayout.ItemRole.FieldRole)
            if label and field:
                label_widget = label.widget()
                field_widget = field.widget()

                if isinstance(label_widget, QLabel):
                    field_name = label_widget.text().replace(":", "").strip()
                    field_value = field_widget.text()

                    if contract_type in ("SB", "CO"):
                        if field_name == "Umidade Máxima":
                            quality_params["umidade_maxima"] = field_value
                        elif field_name == "Impureza Máxima":
                            quality_params["impureza_maxima"] = field_value
                        elif field_name == "Ardidos e Avariados":
                            quality_params["ardidos_avariados"] = field_value
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

        for field_name_input, field_value_input in self.additional_fields_inputs:
            field_name = field_name_input.text().strip()
            field_value = field_value_input.text().strip()
            if field_name:
                additional_fields[field_name] = field_value

        update_fields = []
        update_values = []

        for key, value in contract_data.items():
            update_fields.append(f"{key} = ?")
            update_values.append(value)
        
        if contract_type in ("SB", "CO"):
            quality_fields = ["umidade_maxima", "impureza_maxima", "ardidos_avariados"]
            for field in quality_fields:
                update_fields.append(f"{field} = ?")
                update_values.append(quality_params.get(field, ""))
            
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
            
            update_fields.append("ardidos_avariados = ?")
            update_values.append("")
        
        if additional_fields:
            update_fields.append("additional_fields = ?")
            update_values.append(json.dumps(additional_fields))
        else:
            update_fields.append("additional_fields = ?")
            update_values.append("")
        
        update_values.append(self.contract_id)
        
        try:
            pdf_data = {**contract_data, **quality_params}
            if additional_fields:
                pdf_data["additional_fields"] = additional_fields
                
            pdf_path = createPDF(pdf_data, self)
            if not pdf_path:
                return

            try:
                conn = sqlite3.connect('contracts.db')
                cursor = conn.cursor()
                
                query = f'UPDATE contracts SET {", ".join(update_fields)} WHERE id = ?'
                cursor.execute(query, update_values)
                conn.commit()
                
                QMessageBox.information(self, "Sucesso", f"Contrato atualizado com sucesso!\nPDF gerado em:\n{pdf_path}")
                self.close()
                
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Erro", f"Erro ao atualizar no banco de dados: {e}")
                try:
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
                except:
                    pass
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao gerar PDF: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()