from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flaskapp.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken')



class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RecipeForm(FlaskForm):
    name = StringField('Recipe Name', validators = [DataRequired()])
    description = StringField('Short Description', validators = [DataRequired()])

    required_ingredients = TextAreaField('Required Ingredients  ***Seperate Line by Line. If Ingredients has More than One Word, Combine with Hyphens', validators = [DataRequired()])
    additional_ingredients = TextAreaField('Optional Ingredients ***Seperate Line by Line. If Ingredients has More than One Word, Combine with Hyphens')

    cook_time = StringField('Cook Time in Minutes', validators = [DataRequired()])
    calories = StringField('Total Calories', validators = [DataRequired()])
    instructions = TextAreaField('Instructions - suggestion: seperate by lines and dashes', validators=[DataRequired()])

    image = StringField('Image URL')
    submit = SubmitField('Post')