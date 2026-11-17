import configparser
import pymysql

def conectar():
    """Lê o config.ini e retorna a conexão segura com o TiDB Cloud via PyMySQL."""
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    banco = config['banco']

    return pymysql.connect(
        host=banco['host'],
        port=int(banco['porta']),
        user=banco['usuario'],
        password=banco['senha'],
        database=banco['nome'],
        charset='utf8mb4',
        ssl={'ssl': {'reject_unauthorized': False}}
    )
