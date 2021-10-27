from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'hello_world'
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = '.signin'


from blogger import models
from blogger import views

