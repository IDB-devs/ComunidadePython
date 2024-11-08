from flask import Flask, render_template, url_for, request, flash, redirect, abort #criacao de sites python, juntar paginas do site e url das funcoes, requisicoes e redirecionamento, abortar ação não autorizada
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost # formularios de criar conta, validacao de login, editar perfil, criar post
from comunidadeimpressionadora.models import Usuario, Post #importando as classses do models
from flask_login import login_user, logout_user, current_user, login_required #logar e deslogar usuarios, e verificar se esta logado, acessar paginas exclusivas de usuarios logados
import secrets #deixar o nome da imagem como um codigo
import os #caminhos de pastas
from PIL import Image #compactar arquivos de imagens


@app.route('/') #caminho da url homepage
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/contato') #caminho url alternativo
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required # apenas para pessoas logadas
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios) #criando uma lista de usuarios


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()    
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            # fez login com sucesso e clicou no botao login
            # exibir msgm de login bem sucedido
            flash(message=f'login feito com sucesso no email: ({form_login.email.data})', category='alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home')) # redirecionar para a homepage
        else:
            flash(message=f'Falha no login. E-mail ou Senha Incorretos', category='alert-danger') 
        
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        with app.app_context():
            senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8') #tranasforma a senha em uma senha criptografada # decode para funcionar no deploy
            # criar usuario
            usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
            # adcionar a sessao no banco de dados
            database.session.add(usuario)
            # commit na sessao para salvar no banco de dados
            database.session.commit()
            # criou a conta com sucesso e clicou no botao criar conta
            # exibir msgm de criar conta bem sucedido
            flash(message=f'Conta criada com sucesso para o email: ({form_criarconta.email.data})', category='alert-success')
            return redirect(url_for('home')) # redirecionar para a homepage
        
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user() #desloga o usuario
    flash(message=f'Logout feito com Sucesso', category='alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit(): #se o form foi preenchido e está correto
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash(message='Post Criado com Sucesso', category='alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    # adcionar um codigo aleatorio no nome da imagem
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext() # separa o nome da extensao cada um em uma variavel
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    # reduzir o tamanho da imagem
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo) # salvar a imagem na pasta fotos_perfil
    return nome_arquivo


def atualizar_cursos(form):
    for campo in form:
        lista_cursos = []
        if 'curso_' in campo.name:
            if campo.data:
                #adicionar texto do campo.label('Excel Impressionador') na lista de cursos
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit(): 
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            # mudar o campo  foto_perfil do usuario para o novo nome da imagem
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash(message='Perfil atualizado com Sucesso', category='alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET': # deixar formulario preenchido com dados atuais
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST']) #variavel chamada post_id
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor: #deixar o autor do post editar o post 
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash(message='Post atualizado com Sucesso', category='alert-success')
            return redirect(url_for('home'))  
    else:
        form=None #caso não edite
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id) #achar o post na base de dados
    if current_user == post.autor:
        database.session.delete(post) #deletar post
        database.session.commit
        flash(message='Post Excluído com Sucesso', category='alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403) #erro de tentativa de entrar em link sem autorização