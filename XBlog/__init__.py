#!/usr/bin/env python
# coding:utf-8

from flask import Flask
from flask_moment import Moment
from flask_mail import Mail
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy, SignallingSession
from flask_material import Material

from config import config

class NewSQLAlchemy(SQLAlchemy):
    def create_session(self, options):
        options["autoflush"] = False
        return SignallingSession(self, **options)

mail = Mail()
moment = Moment()
material = Material()
db = NewSQLAlchemy()
login_manager = LoginManager()
pagedown = PageDown()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    material.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
