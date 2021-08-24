from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import Student
from .functions import Validate_account, Validate_password, Validate_if_waiting \
    , Validate_account_Arabic, Validate_if_waiting_Arabic, Validate_password_Arabic


class SignUp(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(message="Please Enter Your First Name"),
                                                       Length(max=15, min=2)])
    last_name = StringField('Last Name', validators=[DataRequired(message="Please Enter Your Last Name"),
                                                     Length(max=15, min=2)])
    email = StringField('Enter your email', validators=[DataRequired(message="Please Enter Your number"),
                                                         Validate_if_waiting])
    password = PasswordField('Password', validators=[DataRequired(message="Please Determine Your Password"),
                                                     Length(min=8, max=50, message='The password must be greater '
                                                                                   'than 8 characters')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(message='This Field Is Required')
        , EqualTo('password', message='the confirmation did not equal the password')])
    gender = SelectField('Gender', choices=['Male', 'Female'], validators=[DataRequired()], default='Male')
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        email = Student.find_one({'phone_number': email.data})
        if email:
            raise ValidationError('This phone existed , please use another')


class LoginForm(FlaskForm):
    email = StringField('number', validators=[DataRequired(message="Please Enter Your number"),
                                              Validate_account, Validate_if_waiting])
    password = PasswordField('Password',
                             validators=[DataRequired(message="Please Determine Your Password"), Validate_password])
    submit = SubmitField('Log in')


class SignUpInArabic(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(message="من فضلك ادخل اسمك الاول"),
                                                       Length(max=15, min=2)])
    last_name = StringField('Last Name', validators=[DataRequired(message="من فضلك ادخل اسمك الاخير"),
                                                     Length(max=15, min=2)])
    email = StringField('Enter your number', validators=[DataRequired(message="من فضلك ادخل الرقم"),
                                                        Validate_if_waiting_Arabic])
    password = PasswordField('Password', validators=[DataRequired(message="من فضلك حدد كلمة مرور"),
                                                     Length(min=8, max=50, message='كلمة مرور قصيرة')])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(message='من فضلك أكد علي كلمة المرور')
        , EqualTo('password', message='كلمتان مرور غير متطابقتان')])
    gender = SelectField('Gender', choices=['Male', 'Female'], validators=[DataRequired()], default='Male')
    submit = SubmitField('سجل الان')

    def validate_email(self, email):
        email = Student.find_one({'phone_number': email.data})
        if email:
            raise ValidationError('هذا الرقم مستخدم من فضلك استخدم رقم اخر')


class LoginFormInArabic(FlaskForm):
    email = StringField('الرقم', validators=[DataRequired(message="من فضلك ادخل رقمك"),
                                                         Validate_account_Arabic,Validate_if_waiting_Arabic])
    password = PasswordField('كلمة المرور',
                             validators=[DataRequired(message="من فضلك ادخل كلمة المرور"), Validate_password_Arabic])
    submit = SubmitField('تسجيل الدخول')
