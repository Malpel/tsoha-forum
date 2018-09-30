from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from application import app, db
from application.auth.models import User, UserRole
from application.auth.forms import LoginForm
from application.admin import admin


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    
    if not user:
        return render_template("auth/loginform.html", form=form, error="Wrong login credentials")
        
    login_user(user)
    
    if user.roles() == 1:
        return redirect(url_for("admin.index"))
        
    return redirect(url_for("index"))


@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))
    

@app.route("/register", methods=["GET", "POST"])
def register():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        u = User(form.username.data, form.password.data)
        db.session().add(u)
        db.session().commit()
        ur = UserRole(u.id, 3)
        db.session().add(ur)
        db.session().commit()
        return redirect(url_for("auth_login"))
    return render_template("auth/register.html", form=form)