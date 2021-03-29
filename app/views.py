from flask import render_template
from app import app

@app.route('/')
def index():
    user = {'name': 'Power-Rangers'}
    return render_template('index.html',
                           title='Home',
                           user=user)