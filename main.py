# apenas inicia o sistema
from PyQt5 import uic, QtWidgets
import sys
import os
import pyodbc
from produto_dao import inserir_produto, listar_produtos, atualizar_produto, excluir_produto, pesquisar_produtos

id_produto_selecionado = None

def funcao_principal():
    nomeProduto = Cadastro.lineEdit.text().strip()
    valorProduto = Cadastro.lineEdit_2.text().strip()
    quantidadeProduto = Cadastro.lineEdit_3.text().strip()

    categoriaProduto = ""
    if Cadastro.radioButton.isChecked():
        categoriaProduto = "Eletrônicos"
    elif Cadastro.radioButton_2.isChecked():
        categoriaProduto = "Alimentos"
    elif Cadastro.radioButton_3.isChecked():
        categoriaProduto = "Produto de Limpeza"
    elif Cadastro.radioButton_4.isChecked():
        categoriaProduto = "Produto de Higiene"

    
    if not nomeProduto or not valorProduto or not quantidadeProduto or not categoriaProduto:
        QtWidgets.QMessageBox.warning(
            Cadastro,
            "Erro",
            "Preencha todos os campos e selecione uma categoria."
        )
        return

    try:
        valorProduto = float(valorProduto.replace(",", "."))
        quantidadeProduto = int(quantidadeProduto)
    except ValueError:
        QtWidgets.QMessageBox.warning(
            Cadastro,
            "Erro",
            "Preço deve ser número e quantidade deve ser inteira."
        )
        return

    inserir_produto(nomeProduto, valorProduto, quantidadeProduto, categoriaProduto)

    QtWidgets.QMessageBox.information(
        Cadastro,
        "Cadastro Feito!",
        "Produto cadastrado com sucesso!"
    )

    limpar_label()
    carregar_tabela()
        
    
    
    
def limpar_label():
    Cadastro.lineEdit.clear()
    Cadastro.lineEdit_2.clear()
    Cadastro.lineEdit_3.clear()

def carregar_tabela():
    dados = listar_produtos()

    Cadastro.tableWidget.setRowCount(len(dados))
    Cadastro.tableWidget.setColumnCount(5)

    Cadastro.tableWidget.setHorizontalHeaderLabels([
        "ID PRODUTO", "DESCRIÇÃO", "PREÇO", "QUANTIDADE", "CATEGORIA"
    ])

    for linha, produto in enumerate(dados):
        for coluna, valor in enumerate(produto):
            Cadastro.tableWidget.setItem(
                linha,
                coluna,
                QtWidgets.QTableWidgetItem(str(valor))
            )

    Cadastro.tableWidget.resizeColumnsToContents()

def selecionar_produto():
    global id_produto_selecionado

    linha = Cadastro.tableWidget.currentRow()
    if linha < 0:
        return

    id_produto_selecionado = Cadastro.tableWidget.item(linha, 0).text()

    Cadastro.lineEdit.setText(
        Cadastro.tableWidget.item(linha, 1).text()
    )
    Cadastro.lineEdit_2.setText(
        Cadastro.tableWidget.item(linha, 2).text()
    )
    Cadastro.lineEdit_3.setText(
        Cadastro.tableWidget.item(linha, 3).text()
    )

    categoria = Cadastro.tableWidget.item(linha, 4).text()

    Cadastro.radioButton.setChecked(categoria == "Eletrônicos")
    Cadastro.radioButton_2.setChecked(categoria == "Alimentos")
    Cadastro.radioButton_3.setChecked(categoria == "Produto de Limpeza")
    Cadastro.radioButton_4.setChecked(categoria == "Produto de Higiene")


def atualizar():
    if id_produto_selecionado is None:
        QtWidgets.QMessageBox.warning(
            Cadastro, "Aviso", "Selecione um produto na tabela."
        )
        return

    nome = Cadastro.lineEdit.text().strip()
    preco = Cadastro.lineEdit_2.text().strip()
    quantidade = Cadastro.lineEdit_3.text().strip()

    if not nome or not preco or not quantidade:
        QtWidgets.QMessageBox.warning(
            Cadastro, "Erro", "Preencha todos os campos."
        )
        return

    try:
        preco = float(preco.replace(",", "."))
        quantidade = int(quantidade)
    except ValueError:
        QtWidgets.QMessageBox.warning(
            Cadastro, "Erro", "Preço inválido ou quantidade inválida."
        )
        return

    categoria = ""
    if Cadastro.radioButton.isChecked():
        categoria = "Eletrônicos"
    elif Cadastro.radioButton_2.isChecked():
        categoria = "Alimentos"
    elif Cadastro.radioButton_3.isChecked():
        categoria = "Produto de Limpeza"
    elif Cadastro.radioButton_4.isChecked():
        categoria = "Produto de Higiene"

    atualizar_produto(
    id_produto_selecionado,
    nome,
    preco,
    quantidade,
    categoria
)
    
    carregar_tabela()

    QtWidgets.QMessageBox.information(
        Cadastro, "Sucesso", "Produto atualizado com sucesso!"
    )

def excluir():
    linha = Cadastro.tableWidget.currentRow()

    if linha < 0:
        QtWidgets.QMessageBox.warning(
            Cadastro, "Aviso", "Selecione um produto para excluir."
        )
        return

    idProduto = Cadastro.tableWidget.item(linha, 0).text()

    resposta = QtWidgets.QMessageBox.question(
        Cadastro,
        "Confirmar exclusão",
        "Tem certeza que deseja excluir este produto?",
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
    )

    if resposta == QtWidgets.QMessageBox.Yes:
        excluir_produto(idProduto)
        carregar_tabela()
    
def pesquisar():
    texto = Cadastro.lineEdit_4.text()
    categoria = Cadastro.comboBox.currentText()

    dados = pesquisar_produtos(texto, categoria)

    Cadastro.tableWidget.setRowCount(len(dados))

    for linha, produto in enumerate(dados):
        for coluna, valor in enumerate(produto):
            Cadastro.tableWidget.setItem(
                linha,
                coluna,
                QtWidgets.QTableWidgetItem(str(valor))
            )

    Cadastro.tableWidget.resizeColumnsToContents()
        
        


app = QtWidgets.QApplication(sys.argv)

# garante que o Python encontre o .ui
arquivo_ui = os.path.join(os.path.dirname(__file__), "Cadastro.ui")
Cadastro = uic.loadUi(arquivo_ui)
carregar_tabela()
Cadastro.tableWidget.itemClicked.connect(selecionar_produto)


Cadastro.pushButton.clicked.connect(funcao_principal)
Cadastro.pushButton_2.clicked.connect(limpar_label)
Cadastro.pushButton_3.clicked.connect(carregar_tabela)
Cadastro.pushButton_5.clicked.connect(atualizar)
Cadastro.pushButton_4.clicked.connect(excluir)
Cadastro.pushButton_6.clicked.connect(pesquisar)
Cadastro.lineEdit_4.textChanged.connect(pesquisar)
Cadastro.comboBox.currentIndexChanged.connect(pesquisar)


Cadastro.show()
sys.exit(app.exec())
    
    