#Aplicativo principal
from flask import Flask, render_template, url_for, redirect, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
import email.message


login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERMEGADIFICIL'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)





@app.route('/', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        user = User.select_data_user_email(email)
        hash = user.senha
        if user and check_password_hash(hash, senha):
            login_user(user)

            return redirect(url_for('inicial'))
    return render_template('index.html')

@app.route('/cadastro', methods = ["POST", "GET"])
def cadastro():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        nome = request.form["nome"]
        hash = generate_password_hash(senha)

        User.insert_data_user(nome, email, hash)
        user = User.select_data_user_email(email)
        login_user(user)

        corpo = f"""
        <html lang="pt-BR">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email da Biblioteca</title>
  </head>
  <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
    <!-- Container principal -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f4f4; padding: 20px;">
      <tr>
        <td>
          <!-- Tabela interna para layout do email -->
          <table align="center" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <!-- Cabeçalho -->
            <tr>
              <td align="center" style="background-color: #0056b3; padding: 20px 0; border-radius: 8px 8px 0 0;">
                <h1 style="color: #ffffff; margin: 0;">Bem-vindo à Biblioteca</h1>
              </td>
            </tr>
            <!-- Conteúdo principal -->
            <tr>
              <td style="padding: 20px;">
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Prezado(a) Leitor(a) {current_user.nome},
                </p>
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Estamos felizes em recebê-lo em nossa comunidade de leitores! A partir de agora, você terá acesso a uma vasta coleção de livros, eBooks, audiolivros e eventos exclusivos em nossa biblioteca.
                </p>
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Para começar, sugerimos que explore nossa <a href="{url_for("livros")}" style="color: #00796b; text-decoration: none;">seção de livros</a> ou participe de um dos nossos <strong>clubes de leitura</strong> semanais!
                </p>
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Se precisar de ajuda, nossa equipe está à disposição para oferecer orientações e recomendações personalizadas.
                </p>
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Aproveite ao máximo tudo o que nossa biblioteca tem a oferecer. Esperamos vê-lo em breve!
                </p>
              </td>
            </tr>
            <!-- Rodapé -->
            <tr>
              <td align="center" style="background-color: #0056b3; padding: 10px; border-radius: 0 0 8px 8px;">
                <p style="color: #ffffff; font-size: 14px; margin: 0;">
                  Biblioteca Virtual | Endereço: Rua IFRN, 123, Caicó | Telefone: (84) 99827-2514
                </p>
                <p style="color: #ffffff; font-size: 14px; margin: 0;">
                  <a href="{url_for("inicial")}" style="color: #80cbc4; text-decoration: none;">Visite nosso site</a> | <a href="mailto:bibliotecavirtual432@gmail.com" style="color: #80cbc4; text-decoration: none;">Entre em contato</a>
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
        """
        assunto = "Cadastro Bem Sucedido!"
        destinatario = current_user.email


        User.enviar_email(corpo, assunto, destinatario)



        return redirect(url_for("inicial"))
    return render_template('cadastro.html')




@app.route("/inicial")
@login_required
def inicial():
    user = current_user.nome
    return render_template("inicial.html", user = user)







@app.route("/livros", methods = ["POST", "GET"])
@login_required
def livros():

    if request.method == "POST":
        titulo = request.form["titulo"]
        genero = request.form["genero"]
        autor = request.form["autor"]
        id = current_user.id
        User.insert_data_livro(titulo, genero, autor, id)

        corpo = f"""
        <!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Novo Livro Cadastrado</title>
  </head>
  <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
    <!-- Container principal -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f4f4; padding: 20px;">
      <tr>
        <td>
          <!-- Tabela interna para layout do email -->
          <table align="center" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <!-- Cabeçalho -->
            <tr>
              <td align="center" style="background-color: #0056b3; padding: 20px 0; border-radius: 8px 8px 0 0;">
                <h1 style="color: #ffffff; margin: 0;">Novo Livro Cadastrado!</h1>
              </td>
            </tr>
            <!-- Conteúdo principal -->
            <tr>
              <td style="padding: 20px;">
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Olá, Leitor(a) {current_user.nome},
                </p>
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Temos o prazer de anunciar que um novo livro foi cadastrado ao nosso acervo! Confira os detalhes abaixo:
                </p>

                <!-- Detalhes do Livro -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f9f9f9; padding: 15px; border-radius: 8px;">
                  <tr>
                    <td style="color: #333333; font-size: 16px;">
                      <strong>Título:</strong> {titulo}<br>
                      <strong>Autor:</strong> {autor}<br>
                      <strong>Gênero:</strong> {genero}<br>
                      
                    </td>
                  </tr>
                </table>

                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Estamos ansiosos para que você explore este novo título. Não perca a oportunidade de ser um dos primeiros a ler!
                </p>
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Reserve já sua cópia acessando o catálogo online da biblioteca ou venha nos visitar para pegar seu exemplar.
                </p>
                <p style="text-align: center;">
                  <a href="{url_for("livros")}" style="background-color: #0056b3; color: #ffffff; text-decoration: none; padding: 10px 20px; border-radius: 5px; font-size: 16px;">Ver Catálogo</a>
                </p>
              </td>
            </tr>
            <!-- Rodapé -->
            <tr>
              <td align="center" style="background-color: #0056b3; padding: 10px; border-radius: 0 0 8px 8px;">
                <p style="color: #ffffff; font-size: 14px; margin: 0;">
                  Biblioteca Virtual | Endereço: Rua IFRN, 123, Caicó | Telefone: (84) 199827-2514
                </p>
                <p style="color: #ffffff; font-size: 14px; margin: 0;">
                  <a href="{url_for("inicial")}" style="color: #c5cae9; text-decoration: none;">Visite nosso site</a> | <a href="mailto:bibliotecavirtual432@gmail.com" style="color: #c5cae9; text-decoration: none;">Entre em contato</a>
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>


        """
        assunto = f"Novo Livro na Biblioteca do Gênero {genero}"
        destinatario = current_user.email


        User.enviar_email(corpo, assunto, destinatario)

    id = current_user.id
    livros = User.select_data_livros(id)

    return render_template("livros.html", livros = livros)

@app.route('/<int:id>/remove_livro', methods=['POST'])
@login_required
def remove_livro(id):
    User.delete_data_livro(id)
    return redirect(url_for("livros"))









@app.route("/comentarios", methods = ["POST", "GET"])
@login_required
def comentarios():
    if request.method == "POST":
        livro = request.form["livro"]
        conteudo = request.form["conteudo"]
        id = current_user.id

        User.insert_data_comentario(conteudo, id, livro)

        corpo = f"""
        <!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Novos Comentários sobre o Livro</title>
  </head>
  <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
    <!-- Container principal -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f4f4; padding: 20px;">
      <tr>
        <td>
          <!-- Tabela interna para layout do email -->
          <table align="center" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <!-- Cabeçalho -->
            <tr>
              <td align="center" style="background-color: #0056b3; padding: 20px 0; border-radius: 8px 8px 0 0;">
                <h1 style="color: #ffffff; margin: 0;">Novos Comentários sobre o Livro</h1>
              </td>
            </tr>
            <!-- Conteúdo principal -->
            <tr>
              <td style="padding: 20px;">
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Olá, Leitor(a) {current_user.nome},
                </p>
                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Ficamos felizes em informar que o livro <strong>"{livro}"</strong> recebeu novo comentário! Aqui está o que está dizendo:
                </p>

                <!-- Comentários -->
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f9f9f9; padding: 15px; border-radius: 8px;">
                  <tr>
                    <td style="color: #333333; font-size: 14px;">
                      <strong>Comentário 1:</strong><br>
                      <em>"{conteudo}"</em><br>
                      <span style="color: #555555;">- {current_user.nome}</span><br><br>

                    </td>
                  </tr>
                </table>

                <p style="color: #333333; font-size: 16px; line-height: 1.6;">
                  Você também pode deixar sua opinião e ajudar outros leitores! Acesse o livro no catálogo online e compartilhe o que achou.
                </p>

                <p style="text-align: center;">
                  <a href="{url_for("livros")}" style="background-color: #0056b3; color: #ffffff; text-decoration: none; padding: 10px 20px; border-radius: 5px; font-size: 16px;">Ver Comentários e Comentar</a>
                </p>
              </td>
            </tr>
            <!-- Rodapé -->
            <tr>
              <td align="center" style="background-color: #0056b3; padding: 10px; border-radius: 0 0 8px 8px;">
                <p style="color: #ffffff; font-size: 14px; margin: 0;">
                  Biblioteca Virtual | Endereço: Rua IFRN, 123, Caicó | Telefone: (84) 199827-2514
                </p>
                <p style="color: #ffffff; font-size: 14px; margin: 0;">
                  <a href="{url_for("inicial")}" style="color: #ffe0b2; text-decoration: none;">Visite nosso site</a> | <a href="mailto:bibliotecavirtual432@gmail.com" style="color: #c5cae9; text-decoration: none;">Entre em contato</a>
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
        """
        assunto = f"Comentário Sobre o Livro {livro}"
        destinatario = current_user.email


        User.enviar_email(corpo, assunto, destinatario)


    livros = User.select_data_livros(current_user.id)

    return render_template("comentarios.html", livros = livros)
   





@app.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    if request.method == "POST":
        logout_user()
        return redirect(url_for("login"))
    return render_template("logout.html")