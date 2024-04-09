from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, ValidationError


class RegisterFormMaster(FlaskForm):
    foto = FileField('Выберете аватарку')
    profeshon = SelectField('Спициальность', choices=['Мастер маникюра(педикюра)', 'парикмахер', 'визажист'])
    pris = TextAreaField('Прайс', validators=[DataRequired()])
    adress = StringField('Адрес (где будет предоставляться услуга)', validators=[DataRequired()])
    vk = StringField('VK')
    inst = StringField('Instagram')
    telegram = StringField('Telegram')
    submit = SubmitField('Создать станичку')