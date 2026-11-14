from conexao import conectar

def inserir_adotante(nome, telefone, cpf):
    """Insere um novo adotante no banco de dados."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        sql = "INSERT INTO adotante (nome, telefone, cpf) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, telefone, cpf))
        conexao.commit()

def listar_adotantes():
    """Retorna todos os adotantes cadastrados."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id_adotante, nome, telefone, cpf FROM adotante")
        return cursor.fetchall()

def atualizar_adotante(id_adotante, nome, telefone, cpf):
    """Atualiza os dados de um adotante."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        sql = "UPDATE adotante SET nome = %s, telefone = %s, cpf = %s WHERE id_adotante = %s"
        cursor.execute(sql, (nome, telefone, cpf, id_adotante))
        conexao.commit()

def excluir_adotante(id_adotante):
    """Exclui um adotante pelo ID."""
    with conectar() as conexao:
        cursor = conexao.cursor()
        sql = "DELETE FROM adotante WHERE id_adotante = %s"
        cursor.execute(sql, (id_adotante,))
        conexao.commit()