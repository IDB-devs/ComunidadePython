from flask_wtf import FlaskForm #formularios
from flask_wtf.file import FileField, FileAllowed #campo de colocar arquivos e extensoes permitidas
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField #campos de texto(pequeno), senha, envio, lembrar dados, campo de texto(grande)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError  #campos obrigatorios, tamanho, validador de email, comparador de senha, exibidor de erros de validacao
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), ]) #texto visivel no campo, e lista validadores
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)]) #6 a 20 carcteres
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')]) #confirmacao da senha
    botao_submit_criarconta = SubmitField('Criar Conta')
    
    def validate_email(self, email): #obrigatoriamente nomear comeco com 'validate_' para ser executado automaticamente pelo flask
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')
    
    
class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')
    
    
class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar foto de Perfil', validators=[FileAllowed(['jpg', 'png'])]) #extensoes permitidas de enviar
    curso_excel = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_Python = BooleanField('Python Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionador')
    curso_sql = BooleanField('SQL Impressionador')
    botao_submit_editarperfil = SubmitField('Confirmar Edição')
    
    def validate_email(self, email): #obrigatoriamente nomear comeco com 'validate_' para ser executado automaticamente pelo flask
        #verificar se o cara mudou de email
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse email. Cadastre outro email')
            

class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')