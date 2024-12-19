CREATE DATABASE IF NOT EXISTS biblioteca;
USE biblioteca;

CREATE TABLE IF NOT EXISTS tb_usuarios (
    usu_id INT(11) AUTO_INCREMENT PRIMARY KEY NOT NULL,
    usu_nome VARCHAR(200) NOT NULL,
    usu_email VARCHAR(200) NOT NULL,
    usu_senha VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_comentarios (
    com_id INT(11) AUTO_INCREMENT PRIMARY KEY NOT NULL,
    com_conteudo VARCHAR(1000) NOT NULL,
    com_usu_id INT(11) NOT NULL,
    com_livro_id INT(11) NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_livros (
    liv_id INT(11) AUTO_INCREMENT PRIMARY KEY NOT NULL,
    liv_titulo VARCHAR(200) NOT NULL,
    liv_genero VARCHAR(200) NOT NULL,
    liv_autor VARCHAR(200) NOT NULL,
    liv_usuarios_id INT(11) NOT NULL
);

