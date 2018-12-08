from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
	#  DataRequired просто проверяет, что поле не отправлено пустым
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class SatCoord(FlaskForm):
    #  DataRequired просто проверяет, что поле не отправлено пустым
    sat_lat = FloatField('Latitude', validators=[DataRequired()])
    sat_long = FloatField('Longitude', validators=[DataRequired()])
    sat_height = FloatField('Height', validators=[DataRequired()])
    submit = SubmitField('Run')


class AntCoord(FlaskForm):
    #  DataRequired просто проверяет, что поле не отправлено пустым
    ant_lat = FloatField('Latitude', validators=[DataRequired()])
    ant_long = FloatField('Longitude', validators=[DataRequired()])
    ant_height = FloatField('Height', validators=[DataRequired()])
    submit = SubmitField('Save')


class Angels(FlaskForm):
    #  DataRequired просто проверяет, что поле не отправлено пустым
    teta = FloatField('Teta')
    fi_priv = FloatField('Fi_div')
    submit = SubmitField('Run')















