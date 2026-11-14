from conexao import conectar

def inserir_vacina(id_animal, nome_vacina, data_aplicacao, data_proxima_dose):
    with conectar() as conexao:
        cursor = conexao.cursor()
        sql = "INSERT INTO vacina (id_animal, nome_vacina, data_aplicacao, data_proxima_dose) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (id_animal, nome_vacina, data_aplicacao, data_proxima_dose))
        conexao.commit()

def listar_vacinas():
    with conectar() as conexao:
        cursor = conexao.cursor()
        sql = """
            SELECT v.id_vacina, a.nome, v.nome_vacina, v.data_aplicacao, v.data_proxima_dose, v.id_animal
            FROM vacina v
            JOIN animal a ON v.id_animal = a.id_animal
        """
        cursor.execute(sql)
        return cursor.fetchall()

def excluir_vacina(id_vacina):
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM vacina WHERE id_vacina = %s", (id_vacina,))
        conexao.commit()