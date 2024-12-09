from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User

"""
This module contains the form classes used in the pharmacy website.
These include forms for registration, login, and product management.
"""

class RegistrationForm(FlaskForm):
    """
    Form for user registration, including fields for email, password, and password confirmation.
    """
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_email(self, email):
        """
        Validates the email to ensure it's not already registered.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is already registered.")


class LoginForm(FlaskForm):
    """
    Form for user login, including fields for email and password.
    """
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ProductForm(FlaskForm):
    """
    Form for adding a new product (medicine), including fields for name, price, and stock.
    """
    name = StringField("Medicine Name", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    stock = IntegerField("Stock", validators=[DataRequired()])
    submit = SubmitField("Add Medicine")


class UpdateProductForm(FlaskForm):
    """
    Form for updating a product (medicine), including fields for price and stock.
    """
    price = FloatField("New Price", validators=[DataRequired()])
    stock = IntegerField("New Stock", validators=[DataRequired()])
    submit = SubmitField("Update")
