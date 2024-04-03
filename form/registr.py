from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Никнейм или ФИ', validators=[DataRequired()])
    age = IntegerField('Укажите ваш возраст', validators=[DataRequired()])
    submit = SubmitField('Я мастер')
    submit2 = SubmitField('Я клиент')