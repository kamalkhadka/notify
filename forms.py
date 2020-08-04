from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import Required, Email, ValidationError
import phonenumbers
# from wtforms.widgets import TextArea


class SignupForm(FlaskForm):
    first_name = StringField('First name', validators=[Required("First name is required")])
    last_name = StringField('Last name', validators=[Required('Last name is required')])
    email  = StringField('Email', validators=[Required('Email is required'), Email()])
    password = PasswordField('Password', validators=[Required('Password is required')])
    phone = StringField('Phone', validators=[Required()])

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse('+1'+phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required('Email is required'), Email()])
    password = PasswordField('Password', validators=[Required('Password is required')])

class ContactForm(FlaskForm):
    first_name = StringField('First name', validators=[Required()])
    last_name = StringField('Last name', validators=[Required()])
    # phone = StringField('Phone', validators=[Required()])
    email = StringField('Email', validators=[Required(), Email()])

class GroupForm(FlaskForm):
    name = StringField('Group name', validators=[Required()])

class MessageForm(FlaskForm):
    subject = StringField('Subject', validators=[Required()])
    message = TextAreaField('Message', validators=[Required()])

class VerifyUserForm(FlaskForm):
    token = StringField('Token', validators=[Required()])
    