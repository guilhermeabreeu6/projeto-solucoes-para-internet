import mysql.connector

def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",         # teu usuário MySQL
            password="1234",     # tua senha MySQL
            database="banco_digital"
        )
        print("✅ Conexão com o banco estabelecida!")
        return conexao
    except mysql.connector.Error as erro:
        print(f"❌ Erro ao conectar ao MySQL: {erro}")
        return None
if __name__ == "__main__":
    conectar()