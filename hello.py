from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'piercetheveil'  # Chave secreta para segurança

# Iniciando extensões
bootstrap = Bootstrap(app)
moment = Moment(app)

# IDENTIFICAÇÃO
@app.route('/user/<name>')
@app.route('/user/<name>/<prontuario>')
@app.route('/user/<name>/<prontuario>/<instituicao>')
def user(name, prontuario='PT3035999', instituicao='IFSP-Pirituba'):
    return render_template('id.html', name=name, prontuario=prontuario, instituicao=instituicao)

# REQUISIÇÃO DE CONTEXTO
@app.route('/contextorequisicao/<name>')
def contextorequisicao(name):
    navegador = request.headers.get('User-Agent')
    ip_cliente = request.remote_addr
    host_app = request.host
    return render_template('contexto.html', name=name, navegador=navegador, ip_cliente=ip_cliente, host_app=host_app)

# FORMULÁRIO

from flask import Flask, render_template, session, redirect, url_for, flash
@app.route('/', methods=['GET', 'POST'])
def index():
  form = NameForm()
  if form.validate_on_submit():
    old_name = session.get('name')
    if old_name is not None and old_name != form.name.data:
      flash('Looks like you have changed your name!')
    session['name'] = form.name.data
    return redirect(url_for('index'))
  return render_template('index.html', form = form, name = session.get('name'))

