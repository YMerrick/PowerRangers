from flask import Flask

app = Flask(__name__)
app.secret_key = "power-rangers"
from app import views