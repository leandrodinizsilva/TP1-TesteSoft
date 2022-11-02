from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from provasonline.constants import usuario_urole_roles

class LoginForm(FlaskForm):
    login = StringField("login", validators = [DataRequired()])
    senha = PasswordField("senha", validators = [DataRequired()])
    remember_me = BooleanField("remember_me")

class UsuarioForm(FlaskForm):
	nome = StringField('Nome', validators = [DataRequired()])
	login = StringField('Login', validators = [DataRequired()])
	senha = PasswordField('Senha', validators = [DataRequired()])
	urole = SelectField('Função no sistema', choices=[(usuario_urole_roles['ALUNO'], 'Aluno'),(usuario_urole_roles['PROFESSOR'], 'Professor')])
	submit = SubmitField('Cadastrar')	