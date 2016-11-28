from flask import Flask
from flask_login import LoginManager
from config import WEB_CLIENT_ID

app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)
