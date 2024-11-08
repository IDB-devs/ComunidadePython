from comunidadeimpressionadora import app, database
from comunidadeimpressionadora.models import Usuario, Post


#with app.app_context():
    #database.create_all() #criando o arquivo database.db(banco de dados) na pasta instance

#with app.app_context():
#    usuario = Usuario(username='Lira', email='lira@gmail.com', senha='123456')
#    usuario2 = Usuario(username='Joao', email='joao@gmail.com', senha='123456')

    #database.session.add(usuario) # adciona o usuario dentro do banco de dados
    #database.session.add(usuario2)

    #database.session.commit() #salva as alteracoes dentro do banco de dados
    
    #meus_usuarios = Usuario.query.all() #pega os dados do banco de dados
    #primeiro_usuario = Usuario.query.first()
    #print(primeiro_usuario.id)
    #print(primeiro_usuario.email)
    #print(primeiro_usuario.posts)
    #usuario_teste = Usuario.query.filter_by(email='lira@gmail.com').first() #lista filtrando qual dado quer pegar