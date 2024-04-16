from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class RegisterFormMaster(FlaskForm):
    photo = FileField('Выберете аватарку')
    category = SelectField('Специальность', choices=['Мастер маникюра(педикюра)', 'Парикмахер', 'Визажист'])
    address = StringField('Адрес (где будет предоставляться услуга)', validators=[DataRequired()])
    telegram = StringField('Telegram(необязательно)')
    description = TextAreaField('Описание')
    submit = SubmitField('Сохранить')
