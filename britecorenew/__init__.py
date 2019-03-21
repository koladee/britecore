import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
SECRET_KEY = os.environ.get('SECRET_KEY', 'maikey')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from britecorenew import route