import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "x1ah"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN = "x1ahgxq@gmail.com"
    ADMIN_PASSWORD = "admin"

    POSTS_PER_PAGE = 5

    @staticmethod
    def init_app(app):
        pass


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

