from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, SelectMultipleField, TimeField
from wtforms.validators import DataRequired


class SignUpForm(FlaskForm):
    date = DateField('Дата', validators=[DataRequired()])
    time = TimeField('Время', validators=[DataRequired()])
    choice = SelectMultipleField('Услуги', validators=[DataRequired()])
    submit = SubmitField('Ок')
