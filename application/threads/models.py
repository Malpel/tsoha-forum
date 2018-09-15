from application import db

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #group = db.Column(db.Integer, db.ForeignKey('group.id'))
    #user = db.Column(db.Integer, db.ForeignKey('account.id'))
    title = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_edited = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp)
    comments = db.relationship("Comment", backref='comment', lazy=True)

    def __init__(self, title):
        self.title = title
        
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #user = db.Column(db.Integer, db.ForeignKey('account.id'))
    #title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_edited = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp)
    thread_id = db.Column(db.ForeignKey("thread.id"))

    def __init__(self, text):
        self.text = text