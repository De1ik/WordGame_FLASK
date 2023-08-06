from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, PasswordField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo
from markupsafe import Markup

from .utilities.valid_word import word_valid


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email('Invalid email address')])
    psw = PasswordField(validators=[DataRequired(), Length(min=4, max=15)])
    remember = BooleanField(default=False)
    submit = SubmitField()



class SignUpForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField(validators=[DataRequired(), Email('Invalid email address')])
    psw = PasswordField(validators=[DataRequired(), Length(min=4, max=15)])
    psw_confirm = PasswordField(validators=[DataRequired(), Length(min=4, max=15), EqualTo('psw', 'passwords not equal')])
    submit = SubmitField()



class ReviewsForm(FlaskForm):
    review = TextAreaField(validators=[DataRequired(), Length(min=4, max=200)])
    submit = SubmitField('Send')




class UpdateInfoForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField(validators=[DataRequired(), Email('Invalid email address')])
    submit = SubmitField('Update')

def validate_word(form, field):
    """check if user word exist or it is just random word"""
    user_word = field.data.strip()
    if not word_valid(user_word):
        raise validators.ValidationError(Markup("It seems that it's a random set of letters<br>it's not an answer anyway :)"))




class GameForm(FlaskForm):
    word = StringField(validators=[DataRequired(), validate_word])
    submit = SubmitField('Send')

    
