from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, IntegerField
from wtforms.validators import DataRequired


class AddingServiceForm(FlaskForm):
    name = StringField('Название услуги', validators=[DataRequired()])
    price = IntegerField('Стоймость', validators=[DataRequired()])
    time = TimeField("Длительность")
    submit = SubmitField('Сохранить')
