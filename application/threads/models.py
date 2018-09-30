from application import db
from application.models import Base
from sqlalchemy.sql import text

# TODO: materiaali 4.1 abstrahoi, ei toiminut odotetusti, kokeile uudestaan jossain välissä
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
    parent = db.relationship("Comment", backref="children", remote_side=[id])

    def __init__(self, text):
        self.text = text

    def comment_thread(thread_id):
        stmt = text("WITH RECURSIVE cte AS (SELECT comment.id, comment.parent_id, comment.user, comment.text, comment.date_created, comment.date_modifed" 
        " FROM comment WHERE comment.thread_id = :thread_id AND parent_id IS NULL UNION ALL" 
        " SELECT comment.id, comment.parent_id, comment.user, comment.text, comment.date_created, comment.date_modifed FROM comment" 
        " INNER JOIN cte ON comment.parent_id = cte.id"
        " WHERE comment.parent_id is NOT NULL ORDER BY parent_id DESC, id)"
        " SELECT * FROM cte").params(thread_id=thread_id)

        res = db.engine.execute(stmt)
        threaded = []
        for row in res:
            threaded.append(row)
            
        return threaded

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    threads = db.relationship("Thread", backref='thread', lazy=True)

    def __init__(self, name):
        self.name = name