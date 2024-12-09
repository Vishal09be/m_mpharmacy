from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is already registered.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ProductForm(FlaskForm):
    name = StringField("Medicine Name", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    stock = IntegerField("Stock", validators=[DataRequired()])
    submit = SubmitField("Add Medicine")


class UpdateProductForm(FlaskForm):
    price = FloatField("New Price", validators=[DataRequired()])
    stock = IntegerField("New Stock", validators=[DataRequired()])
    submit = SubmitField("Update")
