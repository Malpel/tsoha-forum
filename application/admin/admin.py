from flask import Flask, render_template, request, redirect, url_for
from flask_admin import Admin, BaseView, expose
#from flask_login import current_user, login_manager, login_required
from application import app, db
from application.threads.models import Thread, Comment, Category
from application.auth.models import User, UserRole 


class admin(BaseView):
    @app.route("/admin/dashboard")
    def dashboard():
        return render_template("admin/dashboard.html")



