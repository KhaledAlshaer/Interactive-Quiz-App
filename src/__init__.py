from flask import Flask
from flask_login import LoginManager
app = Flask(__name__)
app.secret_key = "2e12d23e-783a-4430-82ad-5c2f6713b4a4"
login_manager = LoginManager()
login_manager.init_app(app)

from src import views