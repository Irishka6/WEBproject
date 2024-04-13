from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, ValidationError


class RegisterFormMaster(FlaskForm):
    foto = FileField('Выберете аватарку')
    profeshon = SelectField('Спициальность', choices=['Мастер маникюра(педикюра)', 'Парикмахер', 'Визажист'])
    adress = StringField('Адрес (где будет предоставляться услуга)', validators=[DataRequired()])
    vk = StringField('VK(необязательно)')
    telegram = StringField('Telegram(необязательно)')
    submit = SubmitField('Сохранить изменения')