
from flask import render_template, request
from application import app, db
from application.threads.models import Thread
from application.threads.forms import ThreadForm

@app.route("/")
def index():
    return render_template("index.html")