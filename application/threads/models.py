from application import db
from application.models import Base
from sqlalchemy.sql import text


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
   
    def get_id(self):
        return self.id

    def comment_thread(self):
        
        stmt = text("WITH RECURSIVE cte(id, parent_id, account, text, date_created, date_modifed, root, level)" 
        " AS (SELECT comment.id, comment.parent_id, comment.user, comment.text, comment.date_created, comment.date_modifed, ARRAY[comment.id], 0"  
        " FROM comment WHERE comment.thread_id = :thread_id AND parent_id IS NULL " 
        " UNION ALL SELECT comment.id, comment.parent_id, comment.user, comment.text, comment.date_created, comment.date_modifed, root || ARRAY[comment.id], cte.level + 1" 
        " FROM cte"
        " INNER JOIN comment ON comment.parent_id = cte.id)"
        " SELECT * FROM cte ORDER BY root").params(thread_id=self.id)

        res = db.engine.execute(stmt)
        threaded = []
        for row in res:
            threaded.append(row)
            
        return threaded


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('account.id'))

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modifed = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    text = db.Column(db.String(1000), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    thread_id = db.Column(db.ForeignKey("thread.id"))
    is_deleted = db.Column(db.Boolean, default=False)
    parent = db.relationship("Comment", backref="children", remote_side=[id])

    def __init__(self, text):
        self.text = text
        
    def get_user(self):
        return self.user
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    threads = db.relationship("Thread", backref='thread', lazy=True)

    def __init__(self, name):
        self.name = name