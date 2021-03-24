from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, RadioField, SelectField, StringField
from wtforms import TextAreaField
from wtforms.validators import InputRequired, Email, Optional, NumberRange, URL


class AddPetForm(FlaskForm):

    name = StringField("Pet Name", validators=[
                       InputRequired(message="REQUIRED: Pet Name cannot be blank")])
    species = SelectField("Species", coerce=int, validators=[
        InputRequired(message="REQUIRED: Species of pet cannot be blank")])
    photo_url = StringField("Photo URL", validators=[Optional(), URL(
        message="Formatting is invalid for a web address.")])
    age = IntegerField("Age", validators=[Optional(), NumberRange(
        min=0, max=30, message="Age should be a whole number (no decimals) bewteen 0 and 30.")])
    notes = TextAreaField("Notes")


class ViewEditPetForm(FlaskForm):

    name = StringField("Pet Name", validators=[
                       InputRequired(message="REQUIRED: Pet Name cannot be blank")])
    species_id = SelectField("Species", coerce=int, validators=[
        InputRequired(message="REQUIRED: Species of pet cannot be blank")])
    photo_url = StringField("Photo URL", validators=[Optional(), URL(
        message="Formatting is invalid for a web address.")])
    age = IntegerField("Age", validators=[Optional(), NumberRange(
        min=0, max=30, message="Age should be a whole number (no decimals) bewteen 0 and 30.")])
    available = BooleanField("Available?")
    notes = TextAreaField("Notes")
