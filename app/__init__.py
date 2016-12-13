from flask import Flask
from flask_login import LoginManager
from config import WEB_CLIENT_ID, MODE

app = Flask(__name__)
if MODE != 'deploy':
    from flask_sslify import SSLify
    sslify = SSLify(app)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)
