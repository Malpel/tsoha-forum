from flask import Flask
app = Flask(__name__)

from application import views
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABSE_URI"] = "sqlite:///forum.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)
db.create_all()
