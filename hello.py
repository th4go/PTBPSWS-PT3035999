import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from wtforms import StringField, SubmitField, SelectField
import resend

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['RESEND_API_KEY'] = os.environ.get('RESEND_API_KEY')
resend.api_key = app.config['RESEND_API_KEY']

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.context_processor
def inject_current_time():
    return dict(current_time=datetime.utcnow())

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    role = SelectField(
        'Role?:', 
        choices=[('Administrator', 'Administrator'), ('Moderator', 'Moderator'), ('User', 'User')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# ... (mantenha os imports, configurações do banco, Resend e classes Role/User) ...

def send_notification_email(new_username):
    sender_email = os.environ.get('API_FROM', 'nao-responda@thiwink.tech') 
    
    html_content = f"""
    <h3>Novo Cadastro no Flasky</h3>
    <p><b>Usuário cadastrado:</b> {new_username}</p>
    <p><b>Nome do aluno:</b> [DIGITE SEU NOME AQUI]</p>
    <p><b>Prontuário:</b> [DIGITE SEU PRONTUÁRIO AQUI]</p>
    """
    
    params = {
        "from": f"Flasky Admin <{sender_email}>",
        "to": [
            "t426lolk@gmail.com", # E-mail de teste temporário
            "seu.email.institucional@aluno.ifsp.edu.br" 
        ],
        "subject": "[Flasky] Novo usuário cadastrado",
        "html": html_content,
    }
    
    try:
        resend.Emails.send(params)
        print("E-mail enviado com sucesso")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        
        if user is None:
            user_role = Role.query.filter_by(name='User').first()
            user = User(username=form.name.data, role=user_role)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            
            # Dispara o e-mail após salvar no banco
            send_notification_email(user.username)
        else:
            session['known'] = True
            
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))

    return render_template(
        'index.html', 
        form=form, 
        name=session.get('name'), 
        known=session.get('known', False)
    )