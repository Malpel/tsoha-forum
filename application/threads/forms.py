from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, validators

class ThreadForm(FlaskForm):
    title = StringField("Title", [validators.Length(min=2, max=50)])
    text = TextAreaField("Text", [validators.Length(min=2, max=2000)])

    class Meta:
        csrf = False


class CommentForm(FlaskForm):
    text = TextAreaField("Text", [validators.Length(min=2, max=2000)])

    class Meta:
        csrf = False
