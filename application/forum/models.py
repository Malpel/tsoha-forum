from application import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #group = db.Column(db.Integer, db.ForeignKey('group.id'))
    #user = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(30))
    content = db.Column(db.String(1000))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_edited = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp)

    def __init__(self, name):
        self.title = "TestausTitle"
        self.content = "Quality Content"