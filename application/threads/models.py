from application import db
from application.models import Base

# TODO: materiaali 4.1 abstrahoi, ei toiminut odotetusti, kokeile uudestaan
class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    #group = db.Column(db.Integer, db.ForeignKey('group.id'))
    user = db.Column(db.Integer, db.ForeignKey('account.id'))
    
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modifed = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    title = db.Column(db.String(50), nullable=False)
    comments = db.relationship("Comment", backref='comment', lazy=True)

    def __init__(self, title):
        self.title = title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('account.id'))

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modifed = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    text = db.Column(db.String(1000), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    thread_id = db.Column(db.ForeignKey("thread.id"))
    children = db.relationship("Comment", backref="parent", remote_side=[id])

    def __init__(self, text):
        self.text = text


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    threads = db.relationship("Thread", backref='thread', lazy=True)