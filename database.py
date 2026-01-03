# apenas conecta com o banco de dados

import pyodbc

def conectar():
    return pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=DESKTOP-HQTVRPJ\\SQLEXPRESS01;"
        "Database=CadastrodeProdutos;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
