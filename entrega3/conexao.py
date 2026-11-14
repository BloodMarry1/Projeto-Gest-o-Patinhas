import configparser
import mysql.connector

def conectar():
    """Lê o config.ini e retorna a conexão com o banco de dados."""
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    banco = config['banco']
    
    return mysql.connector.connect(
        host=banco['host'],
        port=int(banco['porta']),
        user=banco['usuario'],
        password=banco['senha'],
        database=banco['nome']
    )