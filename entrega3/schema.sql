CREATE DATABASE IF NOT EXISTS gestao_patinhas;
USE gestao_patinhas;

CREATE TABLE IF NOT EXISTS animal (
    id_animal INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raca VARCHAR(50),
    porte VARCHAR(20),
    data_nasc DATE,
    castrado VARCHAR(3),
    status VARCHAR(30) DEFAULT 'Disponível'
);

CREATE TABLE IF NOT EXISTS adotante (
    id_adotante INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    cpf VARCHAR(14)
);

CREATE TABLE IF NOT EXISTS vacina (
    id_vacina INT AUTO_INCREMENT PRIMARY KEY,
    id_animal INT NOT NULL,
    nome_vacina VARCHAR(50) NOT NULL,
    data_aplicacao DATE NOT NULL,
    data_proxima_dose DATE,
    FOREIGN KEY (id_animal) REFERENCES animal(id_animal) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS adocao (
    id_adocao INT AUTO_INCREMENT PRIMARY KEY,
    id_animal INT NOT NULL,
    id_adotante INT NOT NULL,
    data_adocao DATE NOT NULL,
    observacoes TEXT,
    FOREIGN KEY (id_animal) REFERENCES animal(id_animal),
    FOREIGN KEY (id_adotante) REFERENCES adotante(id_adotante)
);