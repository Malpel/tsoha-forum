from flask import Flask, render_template, request, redirect, url_for
from flask_admin import Admin, BaseView, expose
#from flask_login import current_user, login_manager, login_required
from application import app, db
from application.threads.models import Thread, Comment, Category
from application.auth.models import User, UserRole 


# TODO: listaa käyttäjiä, poista ja muokkaa
# TODO: alueiden muuttaminen ja lisääminen
# TODO: viestien rajaaminen käyttäjän mukaan, poistaminen, siirtäminen
# TODO: 

class admin(BaseView):
    @app.route("/admin/dashboard")
    def dashboard():
        return render_template("admin/dashboard.html")


# def all_posts_by():
#    User.find_all_comments()

#def list_all_users();

#def find_user():

#def find_post():

#def move_post_to():

#def rename_category():


