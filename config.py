import os
basedir = os.path.abspath(os.path.dirname(__file__))

try:
    from wtforms.fields import HiddenField
except ImportError:

    def is_hidden_field_filter(field):
        raise RuntimeError('WTForms is not installed.')
else:

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

class Config:
    SECRET_KEY = "x1ah"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN = "x1ahgxq@gmail.com"
    ADMIN_PASSWORD = "admin"

    POSTS_PER_PAGE = 5
    LEVMEG_PER_PAGE = 20

    @staticmethod
    def init_app(app):
        app.jinja_env.globals['material_is_hidden_field'] =\
            is_hidden_field_filter


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data-dev.sqlite3")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data-test.sqlite3")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite3")


config = {
    "devolopment": DevConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevConfig
}

