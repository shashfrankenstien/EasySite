from flask import Flask
# from flask_sqlalchemy import SQLAlchemy # uncomment to use sqlalchemy ORM

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'very secret key with spaces'

# db = SQLAlchemy(app) # uncomment to use sqlalchemy ORM

from app import models, views