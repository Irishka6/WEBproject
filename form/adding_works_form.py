from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, StringField
from wtforms.validators import DataRequired


class AddingWorksForm(FlaskForm):
    photo = FileField('Добавить изображение', validators=[DataRequired()])
    description = StringField('Описание')
    submit = SubmitField('Добавить')
