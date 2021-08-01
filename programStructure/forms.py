from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, IntegerField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import Student
from .functions import Validate_account, Validate_password , Validate_if_waiting


class SignUp(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(message="Please Enter Your First Name"),
                                                       Length(max=15, min=2)])
    last_name = StringField('Last Name', validators=[DataRequired(message="Please Enter Your Last Name"),
                                                     Length(max=15, min=2)])
    email = StringField('Enter your email', validators=[DataRequired(message="Please Enter Your Email"),
                                             Email(message="Not An Email") , Validate_if_waiting])
    password = PasswordField('Password', validators=[DataRequired(message="Please Determine Your Password"),
                                                     Length(min=8, max=50, message='The password must be greater '
                                                                                   'than 8 characters')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(message='This Field Is Required')
        , EqualTo('password', message='the confirmation did not equal the password')])
    gender = SelectField('Gender', choices=['Male', 'Female'], validators=[DataRequired()], default='Male')
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        email = Student.find_one({'email': email.data})
        if email:
            raise ValidationError('This email existed , please use another')



class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(message="Please Enter Your Email"),
                                             Email(message="Not An Email"), Validate_account , Validate_if_waiting])
    password = PasswordField('Password',
                             validators=[DataRequired(message="Please Determine Your Password"), Validate_password])
    submit = SubmitField('Log in')


