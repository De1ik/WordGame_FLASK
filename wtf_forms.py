from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired()])
    psw = PasswordField(validators=[DataRequired(), Length(min=4, max=15)])
    remember = BooleanField(default=False)
    submit = SubmitField()

class SignUpForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    psw = PasswordField(validators=[DataRequired(), Length(min=4, max=15)])
    psw_confirm = PasswordField(validators=[DataRequired(), Length(min=4, max=15)])
    submit = SubmitField()