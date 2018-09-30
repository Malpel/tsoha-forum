from application import db
from application.models import Base
from sqlalchemy.sql import text


class User(db.Model):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())
    
    username = db.Column(db.String(144), nullable=False, unique=True)
    password = db.Column(db.String(144), nullable=False)
    role = db.relationship('Role', secondary='user_role')
    comments = db.relationship('Comment', backref='account', lazy=True)
    threads = db.relationship("Thread", backref='account', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def roles(self):
        stmt = text("SELECT role_id FROM user_role WHERE user_id = :user").params(user=self.id)
        res = db.engine.execute(stmt).first()
        role = res[0]
        return role

    def find_all_comments(self):
        stmt = text("SELECT * FROM comment WHERE user = :user GROUP BY comment.thread_id").params(user=self.id)
        res = db.engine.execute(stmt)
        return res

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
       self.name = name

class UserRole(db.Model):
    __tablename__ = "user_role"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id
