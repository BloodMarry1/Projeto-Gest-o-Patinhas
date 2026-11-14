from conexao import conectar

def registrar_adocao(id_animal, id_adotante, data_adocao, observacoes):
    with conectar() as conexao:
        cursor = conexao.cursor()
        sql_adocao = "INSERT INTO adocao (id_animal, id_adotante, data_adocao, observacoes) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql_adocao, (id_animal, id_adotante, data_adocao, observacoes))
        
        sql_animal = "UPDATE animal SET status = 'Adotado' WHERE id_animal = %s"
        cursor.execute(sql_animal, (id_animal,))
        conexao.commit()

def listar_adocoes():
    with conectar() as conexao:
        cursor = conexao.cursor()
        sql = """
            SELECT ad.id_adocao, a.nome, t.nome, ad.data_adocao, ad.observacoes
            FROM adocao ad
            JOIN animal a ON ad.id_animal = a.id_animal
            JOIN adotante t ON ad.id_adotante = t.id_adotante
        """
        cursor.execute(sql)
        return cursor.fetchall()

def excluir_adocao(id_adocao):
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM adocao WHERE id_adocao = %s", (id_adocao,))
        conexao.commit()