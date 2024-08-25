from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, TimeField, SelectField
)
from wtforms.validators import (
    DataRequired, Length, EqualTo, ValidationError, Regexp
)

from .. import CONF
from ..models import User, Subject

from . import FormErrors

USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 20

class AddJournalPageItemForm(FlaskForm):
    hour_start = TimeField(
        'Heure de début', 
        validators = [
            DataRequired(FormErrors.FIELD_REQUIRED)
        ]
    )
    hour_end = TimeField(
        'Heure de fin', 
        validators = [
            DataRequired(FormErrors.FIELD_REQUIRED)
        ]
    )
    subject = SelectField(
        'Matière', 
        validators = [
            DataRequired(FormErrors.FIELD_REQUIRED),
        ],
    )
    content = StringField(
        'Description',
        validators = [
            DataRequired(FormErrors.FIELD_REQUIRED),
        ]
    )

    submit = SubmitField('Ajouter')


class AddJournalPageForm(FlaskForm):
    username = StringField(
        'Nom d\'utilisateur', 
        validators = [
            DataRequired(FormErrors.FIELD_REQUIRED),
            Length(
                min = USERNAME_MIN_LENGTH, 
                max = USERNAME_MAX_LENGTH, 
                message = FormErrors.INVALID_LENGTH.format(
                    min = USERNAME_MIN_LENGTH, 
                    max = USERNAME_MAX_LENGTH
                )
            ),
            Regexp(
                '^([a-zA-Z0-9]|_)+$', 
                message = 'Le nom d\'utilisateur ne peut que contenir des lettres, chiffres et underscore.'
            )
        ]
    )
    password = PasswordField(
        'Mot de passe', 
        validators = [DataRequired(FormErrors.FIELD_REQUIRED),]
    )
    confirm_password = PasswordField(
        'Confirmer le mot de passe', 
        validators = [
            DataRequired(FormErrors.FIELD_REQUIRED),
            EqualTo('password', FormErrors.PASSWORD_DOESNT_MATCH),
        ]
    )

    master_pwd = PasswordField(
        'Master key',
        validators = [
            DataRequired(FormErrors.FIELD_REQUIRED),
        ]
    )

    submit = SubmitField('S\'enregistrer')

    def validate_username(self, username):
        if user := User.query.filter_by(name = username.data).first():
            raise ValidationError(FormErrors.USERNAME_ALREADY_EXISTS)
        
    def validate_master_pwd(self, master_pwd):
        if master_pwd.data != CONF['MASTER_KEY']:
            raise ValidationError('Mot de passe maître invalide... \n S\'il ne vous a pas été explicitement donné, vous n\'êtes probablement pas le/la bienvenu(e) ici :(')
        
