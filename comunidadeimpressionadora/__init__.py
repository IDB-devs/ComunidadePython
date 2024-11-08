from flask import Flask, render_template, url_for, request, flash, redirect #criacao de sites python, juntar paginas do site e url das funcoes, requisicoes e redirecionamento
from flask_sqlalchemy import SQLAlchemy #banco de dados do site
from flask_bcrypt import Bcrypt #cryptografar senhas do site para protecao
from flask_login import LoginManager #gerenciador de login
import os #para deploy
import sqlalchemy #para conferir se criou o banco de dados


app = Flask(__name__) #permite fazer a ligação do frontend pros arquivos

app.config['SECRET_KEY'] = '7478bd7cbdfbf1eaf8c6b7ae309ab145' #token de proteção do site
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') #para deploy no Railway, utilizando banco de dados do railway 
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db' #(URI)caminho local no computador do banco de dados do site .database

database = SQLAlchemy(app) #criado a base de dados
bcrypt = Bcrypt(app) #cryptografando o site
login_manager = LoginManager(app) #criando o gerenciador de login
login_manager.login_view = 'login' #exigir login em paginas exclusivas
login_manager.login_message_category = 'alert-info' # customizar msgm de login obrigatorio

from comunidadeimpressionadora import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI']) #para conferir se criou o banco de dados
inspector = sqlalchemy.inspect(engine) #cria algo para inspecionar o banco de dados
if not inspector.has_table('usuario'): # tabela do models com letra minuscula
    with app.app_context():
        database.drop_all() #deleta atual
        database.create_all() #cria um novo
else:
    print('Base de dados já existente')

from comunidadeimpressionadora import routes #executa o arquivo routes para colocar o site no ar