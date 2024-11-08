from comunidadeimpressionadora import database, login_manager #importando base de dados e gerenciador de login
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario)) #encontra usuario dentro da base de dados


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True) #chave primaria da tabela, nunca igual a outra
    username = database.Column(database.String, nullable=False) #nullabel, nunca podera estar vazio, mas podera haver iguais
    email = database.Column(database.String, nullable=False, unique=True) #n pode haver 2 emails iguais
    senha = database.Column(database.String, nullable=False) #codificar depois
    foto_perfil = database.Column(database.String, default='default.jpg') #armazenar o nome do arquivo da foto do
    posts = database.relationship('Post', backref='autor', lazy=True) #mostrar autores dos posts, lazy mostra todas as inf fo autor
    cursos = database.Column(database.String, nullable=False, default='Não Informado')
    
    def contar_posts(self): #retorna como resposta a quantidade de posts do ususario
        return len(self.posts)
    
    
class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False) #campo de texto ao inves de uma string podendo ter mais paragrafos
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False) #id do usuario q criou o post, e chave q cria a relacao ddo usuario com o post
    
