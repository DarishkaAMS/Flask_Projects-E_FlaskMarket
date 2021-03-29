from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField

class RegisterForm(FlaskForm):
  username = StringField(label='User Name:')
  email_address = StringField(label='Email Address:')
  password_1 = PasswordField(label='Password:')
  password_2 = PasswordField(label='Confirm Password:')
  submit = SubmitField(label='submit')
