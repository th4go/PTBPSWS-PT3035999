from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import resend
from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # Inicializa a chave da API do Resend no contexto da aplicação
    resend.api_key = app.config['RESEND_API_KEY']

    # Registra o Blueprint[cite: 31]
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app