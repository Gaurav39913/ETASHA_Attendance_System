from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Admin, Center

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        admin = Admin.query.filter_by(email=email.data).first()
        if admin:
            raise ValidationError('Email already exists. Please use a different email.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CenterForm(FlaskForm):
    name = StringField('Center Name', validators=[DataRequired()])
    coordinator = StringField('Coordinator', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Add Center')

class StaffForm(FlaskForm):
    name = StringField('Staff Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    center = SelectField('Center', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Staff')

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.center.choices = [(c.id, c.name) for c in Center.query.all()]

class AttendanceForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    center = SelectField('Center', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Filter')

    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.center.choices = [(c.id, c.name) for c in Center.query.all()]
