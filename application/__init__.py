from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt

app = Flask(__name__)


from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from application.auth.models import User, UserRole, Role
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login"


from application import views
from application.threads import models
from application.threads.models import Thread, Comment, Category
from application.threads import views
from application.auth import models
from application.auth import views



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def sample_db():
    admin = User("admin", bcrypt.generate_password_hash("admin"))
    db.session().add(admin)
    monkey = User("SunWukong", bcrypt.generate_password_hash("xiyouji"))
    db.session().add(monkey)
    generic_user = User("generic_user", bcrypt.generate_password_hash("salis"))
    db.session().add(generic_user)

    role1 = Role("admin")
    db.session().add(role1)
    role2 = Role("user")
    db.session().add(role2)
    

    urole1 = UserRole(1, 1)
    db.session().add(urole1)
    urole2 = UserRole(2, 2)
    db.session().add(urole2)
    urole3 = UserRole(3, 2)
    db.session().add(urole3)

    alueet = [
        "Yleistä keskustelua musiikista", "Mainstream", "Hevimeteli", "Elektroninen musiikki", "Aito ug ja trve kvlt musa", "Bysanttilainen dädä",
        "Kitarat", "Muut soittimet", "Tietokoneet ja musaohjelmat yms", "Säveltäminen ja sovittaminen", 
        "Sekalainen"
    ]

    for i in range(len(alueet)):
        alue = Category(alueet[i])
        db.session().add(alue)

    db.session().commit()
    return

db.drop_all()

try:
    db.create_all()
except:
    pass

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Thread, db.session))
admin.add_view(ModelView(Comment, db.session))
#admin.add_view(ModelView(UserRole, db.session))
sample_db()

