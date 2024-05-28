from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Никнейм или ФИ', validators=[DataRequired()])
    user = SelectField('Я', choices=['Клиент', 'Мастер'])
    submit = SubmitField('Зарегистрироваться')
