from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOU_WILL_NEVER_GUESS_THIS_SECRET_KEY'

bootstrap = Bootstrap(app)
moment = Moment(app)

@app.context_processor
def inject_current_time():
    return dict(current_time=datetime.utcnow())

class NameForm(FlaskForm):
    name = StringField('Informe o seu nome', validators=[DataRequired()])
    surname = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    institution = StringField('Informe a sua Insituição de ensino:', validators=[DataRequired()])
    discipline = SelectField(
        'Informe a sua disciplina:',
        choices=[('DSWA5', 'DSWA5'), ('DWBA4', 'DWBA4'), ('Gestão de Projetos', 'Gestão de Projetos')]
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
        session['name'] = form.name.data
        session['surname'] = form.surname.data
        session['institution'] = form.institution.data
        session['discipline'] = form.discipline.data
        
        session['remote_ip'] = request.headers.get('X-Forwarded-For', request.remote_addr)
        session['host'] = request.host
        return redirect(url_for('index'))

    return render_template('index.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect(url_for('login_response'))
        
    return render_template('login.html', form=form)

@app.route('/login_response')
def login_response():
    username = session.get('username')
    return render_template('login_response.html', username=username)