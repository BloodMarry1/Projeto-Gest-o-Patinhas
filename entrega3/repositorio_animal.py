from conexao import conectar

def inserir_animal(nome, especie, raca, porte, data_nasc, castrado, status):
    """Insere um novo animal no banco de dados."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        sql = """
            INSERT INTO animal (nome, especie, raca, porte, data_nasc, castrado, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nome, especie, raca, porte, data_nasc, castrado, status))
        conexao.commit()

def listar_animais():
    """Retorna todos os animais cadastrados."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id_animal, nome, especie, raca, porte, data_nasc, castrado, status FROM animal")
        return cursor.fetchall()

def atualizar_animal(id_animal, nome, especie, raca, porte, data_nasc, castrado, status):
    """Atualiza os dados de um animal existente."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        sql = """
            UPDATE animal 
            SET nome = %s, especie = %s, raca = %s, porte = %s, data_nasc = %s, castrado = %s, status = %s 
            WHERE id_animal = %s
        """
        cursor.execute(sql, (nome, especie, raca, porte, data_nasc, castrado, status, id_animal))
        conexao.commit()

def excluir_animal(id_animal):
    """Exclui um animal pelo ID."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        sql = "DELETE FROM animal WHERE id_animal = %s"
        cursor.execute(sql, (id_animal,))
        conexao.commit()