from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=1, max=30)])
    password = PasswordField("Password",  [validators.Length(min=1)])

    class Meta:
        csrf = False