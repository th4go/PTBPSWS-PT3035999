from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma-chave-secreta-forte-aqui'

bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('Informe o seu nome', validators=[DataRequired()])
    surname = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    institution = StringField('Informe a sua Insituição de ensino:', validators=[DataRequired()])
    discipline = SelectField(
        'Informe a sua disciplina:',
        choices=[('DSWA5', 'DSWA5'), ('GPSA5', 'GPSA5'), ('IHCA5', 'IHCA5')]
    )
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Usuário ou e-mail', validators=[DataRequired()])
    password = PasswordField('Informe a sua senha', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        session['surname'] = form.surname.data
        session['institution'] = form.institution.data
        session['discipline'] = form.discipline.data
        return redirect(url_for('index'))

    # Obtém o IP remoto real (mesmo atrás do proxy do PythonAnywhere)
    remote_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    host = request.host

    return render_template(
        'index.html',
        form=form,
        current_time=datetime.utcnow(),
        remote_ip=remote_ip,
        host=host
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        return render_template(
            'login_response.html',
            username=username,
            current_time=datetime.utcnow()
        )
        
    return render_template(
        'login.html',
        form=form,
        current_time=datetime.utcnow()
    )