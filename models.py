from flask_login import UserMixin
import mysql.connector as sql
import smtplib
import email.message

def obter_conexao():
    db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'biblioteca'
}
    conn = sql.connect(**db_config)
    return conn

class User(UserMixin):
    id: str
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha


# Inserir funções de controle de login

    @classmethod
    def get(cls, id):
        conexao = obter_conexao()
        cursor = conexao.cursor()
        SELECT = 'SELECT * FROM tb_usuarios WHERE usu_id=%s'
        cursor.execute(SELECT, (id,))
        dados = cursor.fetchone()
        if dados:
            user = User(dados[1],dados[2], dados[3])
            user.id = dados[0]
        else: 
            user = None
        return user








# Funções do banco de dados nas tabelas usuarios e livros

# SELECIONAR USER POR EMAIL   
    @classmethod
    def select_data_user_email(cls, email):
        conexao = obter_conexao()
        cursor = conexao.cursor(buffered=True)
        SELECT = 'SELECT * FROM tb_usuarios WHERE usu_email=%s'
        cursor.execute(SELECT, (email,))
        dados = cursor.fetchone()
        if dados:
            user = User(dados[1], dados[2], dados[3])
            user.id = dados[0]

            conexao.commit()
            cursor.close()

            return user
    
# SELECIONAR USER POR ID   
    @classmethod
    def select_data_user_id(cls, id):
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        SELECT = 'SELECT * FROM tb_usuarios WHERE usu_email=%s'
        cursor.execute(SELECT, (id,))
        dados = cursor.fetchone()
        if dados:
            user = User(dados['usu_nome'], dados['usu_email'], dados['usu_senha'])
            user.id = dados['usu_id']

            cursor.close()
            conexao.close()

            return user
        

# SELECIONAR LIVRO  
    @classmethod
    def select_data_livro(cls, id):
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        SELECT = 'SELECT * FROM tb_livros WHERE liv_id=%s'
        cursor.execute(SELECT, (id,))
        dados = cursor.fetchone()
        if dados:
            user = User(dados['liv_titulo'], dados['liv_genero'])
            user.id = dados['liv_id']

            cursor.close()
            conexao.close()

            return user
        return None

# SELECIONAR LIVROS       
    @classmethod
    def select_data_livros(cls, id):
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        SELECT = 'SELECT * FROM tb_livros WHERE liv_usuarios_id=%s'
        cursor.execute(SELECT, (id,))
        dados = cursor.fetchall()
        

        return dados
    
    
    @classmethod
    def delete_data_livro(cls, id):
        conexao = obter_conexao()
        cursor = conexao.cursor()
        DELETE = 'DELETE FROM tb_livros WHERE liv_id=%s'
        cursor.execute(DELETE, (id,))
        conexao.commit()

# INSERIR USER
    @classmethod
    def insert_data_user(cls, nome, email, senha):
        conexao = obter_conexao()

        cursor = conexao.cursor()
        INSERT = 'INSERT INTO tb_usuarios (usu_nome, usu_email, usu_senha) VALUES (%s, %s, %s)'
        cursor.execute(INSERT, (nome, email, senha,))
        conexao.commit()

        cursor.close()
        conexao.close()

# INSERIR LIVRO
    @classmethod
    def insert_data_livro(cls, titulo, genero, autor, id):
        conexao = obter_conexao()
    
        cursor = conexao.cursor()
        INSERT = 'INSERT INTO tb_livros (liv_titulo, liv_genero, liv_autor, liv_usuarios_id) VALUES (%s, %s, %s, %s)'
        cursor.execute(INSERT, (titulo, genero, autor, id))
        conexao.commit()

        cursor.close()
        conexao.close()

# INSERIR CONTATO
    @classmethod
    def insert_data_contato(cls, nome, email, id):
        conexao = obter_conexao()
    
        cursor = conexao.cursor()
        INSERT = 'INSERT INTO tb_contatos (con_nome, con_email, con_usuarios_id) VALUES (%s, %s, %s)'
        cursor.execute(INSERT, (nome, email, id))
        conexao.commit()

        cursor.close()
        conexao.close()
# INSERIR COMENTARIO
    @classmethod
    def insert_data_comentario(cls, conteudo, usuario, livro):
        conexao = obter_conexao()
    
        cursor = conexao.cursor()
        INSERT = 'INSERT INTO tb_comentarios (com_conteudo, com_usu_id, com_livro_id) VALUES (%s, %s, %s)'
        cursor.execute(INSERT, (conteudo, usuario, livro))
        conexao.commit()
        cursor.close()
        conexao.close()



#ENVIAR EMAIL

    @classmethod
    def enviar_email(cls, corpo, assunto, destinatario):
        
        corpo_email = corpo

        msg = email.message.Message()
        msg["Subject"] = assunto
        msg["From"] = "bibliotecavirtual432@gmail.com"
        msg["To"] = destinatario
        password = "mjdiinyyrzelbicy"
        msg.add_header("Content-Type", "text/html")
        msg.set_payload(corpo_email)

        s = smtplib.SMTP("smtp.gmail.com: 587")
        s.starttls()
        s.login(msg["From"], password)
        s.sendmail(msg["From"], [msg["To"]], msg.as_string().encode("utf-8"))



