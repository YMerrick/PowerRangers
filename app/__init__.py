from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = "power-rangers"
from app import views