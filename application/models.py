from application import db

class Base(db.Model):

    __absract__ = True
    user = db.Column(db.Integer, db.ForeignKey('account.id'))
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modifed = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())