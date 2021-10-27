import os
from posixpath import abspath

basedir = os.path(abspath(os.path.dirname(__file__)))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'keep it secret'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_DEV_URL') or \
        f'sqlite:///{os.path.join(basedir, "data-dev.sqlite")}'

config = {'default': DevelopmentConfig}