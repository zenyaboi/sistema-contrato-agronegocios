from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QLineEdit, 
                             QComboBox, QTableWidget, QHBoxLayout, QFormLayout, QTextEdit, QStackedWidget)
from pdf import createPDF

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
        
        '''
        btnCreate = QPushButton("Criar Contrato", self)
        btnCreate.setGeometry(100, 50, 150, 150)

        btnEdit = QPushButton("Editar Contrato", self)
        btnEdit.setGeometry(400, 50, 150, 150)

        btnExit = QPushButton("Sair da Janela", self)
        btnExit.setGeometry(100, 250, 150, 150)
        btnExit.clicked.connect(self.exitWindow)
        '''
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
        #btnSave.clicked.connect(self.saveContract)
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
        self.cmbType.addItems(["Soja (SB)", "Trigo (WH)", "Milho (CO)"])
        self.cmbType.currentTextChanged.connect(self.updatePage3)  # Atualizar Página 3 ao mudar o tipo
        layout.addRow("Tipo do Contrato:", self.cmbType)

        # Data do contrato
        self.txtDate = QLineEdit(page)
        self.txtDate.setPlaceholderText("DD de MM de AAAA")
        layout.addRow("Data do Contrato:", self.txtDate)

        # Vendedor
        self.cmbSeller = QComboBox(page)
        #self.loadClients(self.cmbSeller, "Vendedor")
        layout.addRow("Vendedor:", self.cmbSeller)

        # Comprador
        self.cmbBuyer = QComboBox(page)
        #self.loadClients(self.cmbBuyer, "Comprador")
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
            self.addField("P/L Mínimo:")
            self.addField("PH:")
            self.addField("DON Máximo:")
            self.addField("Cor Mínimo:")
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

    """
    def loadClients(self, combo_box, client_type):
        # Carregar clientes da lista em memória
        combo_box.clear()
        for client in clients:
            if client["type"] == client_type:
                combo_box.addItem(client["name"])
    """
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