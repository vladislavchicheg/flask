from flask_wtf import FlaskForm
from wtforms import Form, PasswordField, StringField, SubmitField, validators


class UserBaseForm(FlaskForm):
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    username = StringField(
        "username",
        [validators.DataRequired()],
    )
    email = StringField(
        "Email Address",
        [
            validators.DataRequired(),
            validators.Email(),
            validators.Length(min=6, max=200),
        ],
        filters=[lambda data: data and data.lower()],
    )


class UserRegisterForm(FlaskForm):
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    email = StringField("E-mail", [validators.DataRequired(), validators.Email()])
    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm_password", message="Field must be equal to Confirm password"),
        ],
    )
    confirm_password = PasswordField("Confirm password", [validators.DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("E-mail", [validators.DataRequired(), validators.Email()])
    password = PasswordField(
        "Password",
        [validators.DataRequired()],
    )
    submit = SubmitField("Login")
