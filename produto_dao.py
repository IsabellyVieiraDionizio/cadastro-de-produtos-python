# comandos sql
from database import conectar

def inserir_produto(nomeProduto, valorProduto, quantidadeProduto, categoriaProduto):
    conexao = conectar()
    cursor = conexao.cursor()

    comando = """
        INSERT INTO Produtos (nomeProduto, valorProduto, quantidadeProduto, categoriaProduto)
        VALUES (?, ?, ?, ?)
    """
    
    dados = nomeProduto, float(valorProduto), int(quantidadeProduto), categoriaProduto
    cursor.execute(comando, dados)
    conexao.commit()

    cursor.close()
    conexao.close()
    
def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT idProduto, nomeProduto, valorProduto, quantidadeProduto, categoriaProduto
        FROM Produtos
    """)

    dados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return dados

def atualizar_produto(idProduto, nomeProduto, valorProduto, quantidadeProduto, categoriaProduto):
    conexao = conectar()
    cursor = conexao.cursor()

    comando = """
        UPDATE Produtos
        SET nomeProduto = ?, valorProduto = ?, quantidadeProduto = ?, categoriaProduto = ?
        WHERE idProduto = ?
    """

    dados = (nomeProduto, valorProduto, quantidadeProduto, categoriaProduto, idProduto)
    cursor.execute(comando, dados)
    conexao.commit()

    cursor.close()
    conexao.close()
    
def excluir_produto(idProduto):
    conexao = conectar()
    cursor = conexao.cursor()
    
    comando = """
        DELETE FROM Produtos WHERE idProduto = ?
        """
    cursor.execute(comando, (idProduto))
    conexao.commit()
    
    cursor.close()
    conexao.close()

def pesquisar_produtos(texto, categoria):
    conexao = conectar()
    cursor = conexao.cursor()

    if categoria == "Todas":
        comando = """
            SELECT idProduto, nomeProduto, valorProduto, quantidadeProduto, categoriaProduto
            FROM Produtos
            WHERE nomeProduto LIKE ?
        """
        cursor.execute(comando, (f"%{texto}%",))
    else:
        comando = """
            SELECT idProduto, nomeProduto, valorProduto, quantidadeProduto, categoriaProduto
            FROM Produtos
            WHERE nomeProduto LIKE ? AND categoriaProduto = ?
        """
        cursor.execute(comando, (f"%{texto}%", categoria))

    resultados = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultados

    