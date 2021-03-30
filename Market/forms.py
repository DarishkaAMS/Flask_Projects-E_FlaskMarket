from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import Length


class RegisterForm(FlaskForm):
    username = StringField(label='User Name:', validators=Length(min=2, max=30))
    email_address = StringField(label='Email Address:')
    password_1 = PasswordField(label='Password:', validators=Length(min=8))
    password_2 = PasswordField(label='Confirm Password:')
    submit = SubmitField(label='Create Account')
