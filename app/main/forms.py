from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, validators, \
IntegerField
from wtforms.validators import ValidationError, DataRequired, Length
# from flask_babel import _, lazy_gettext as _l
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class TeamForm(FlaskForm):
    team = StringField('Team Name', [validators.Length(min=1, max=75)])
    abbr = StringField('Team Abbreviation', [validators.Length(min=1, max=3)])
    submit = SubmitField('Submit')

class TodoForm(FlaskForm):
    todo = StringField('Todo Name', [validators.Length(min=1, max=75)])
    desc = TextAreaField('Description', [validators.Length(min=1, max=150)])
    mc_number = IntegerField('MC Number', [validators.NumberRange(min=1, max=1000000)])
    dnc_doc = StringField('Delmia', [validators.Length(max=50)])
    prog_edit = StringField('Program Edited', [validators.Length(max=50)])
    status = StringField('Status', [validators.Length(max=50)])
    fal = StringField('FAL', [validators.Length(max=50)])
    submit = SubmitField('Submit')
