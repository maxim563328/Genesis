from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Email, DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField("email", validators=[
                        DataRequired(message='Не указана почта'), Email(message='Недействительный адрес'), Length(min=3, max=320, message='Некорректная длина почты')])
    password = PasswordField("password", validators=[
                             DataRequired(), Length(min=8, max=20)])
    remember_me = BooleanField("remember_me")


class RegisterForm(FlaskForm):
    email = StringField("email", validators=[
                        DataRequired(message='Не указана почта'), Email(message='Недействительный адрес'), Length(min=3, max=320, message='Некорректная длина почты')])
    password = PasswordField("password", validators=[
                             DataRequired(message='Не указан пароль'), Length(min=8, max=20, message='Пароль должен содержать от 8 до 20 символов')])
    repeat_password = PasswordField("repeat_password", validators=[
        DataRequired(message='Пароли не совпадают'), EqualTo("password", message='Пароли не совпадают')])
