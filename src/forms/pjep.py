from flask_wtf import FlaskForm
from wtforms import (
    StringField, DateField, SubmitField, TimeField, SelectField, HiddenField
)
from wtforms.validators import (
    DataRequired
)

from datetime import datetime

from . import FormErrors, render_kw, render_kw_submit

now = datetime.now

USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 20

class EditJournalPageItemForm(FlaskForm):

    item_id = HiddenField('ItemID') # Used for PUT and DELETE methods.
    method = HiddenField('Method') # Used to deal with PUT and DELETE methods.

    hour_start = TimeField(
        'Heure de début', 
        validators = [
            DataRequired(FormErrors.FIELD_REQUIRED)
        ],
        render_kw = render_kw
    )
    hour_end = TimeField(
        'Heure de fin', 
        validators = [
            DataRequired(FormErrors.FIELD_REQUIRED)
        ],
        render_kw = render_kw
    )
    subject = SelectField(
        'Matière', 
        validators = [
            DataRequired(FormErrors.FIELD_REQUIRED),
        ],
        render_kw = render_kw
    )
    content = StringField(
        'Description',
        validators = [
            DataRequired(FormErrors.FIELD_REQUIRED),
        ],
        render_kw = render_kw
    )

    submit = SubmitField('Ajouter', render_kw = render_kw_submit)


class AddJournalPageForm(FlaskForm):
    date = DateField(
        'Date', 
        validators = [
            DataRequired(FormErrors.FIELD_REQUIRED)
        ],
        render_kw = { **render_kw, 'value': now().strftime('%Y-%m-%d') }
    )
    
    description = StringField(
        'Description',
        validators = [
            DataRequired(FormErrors.FIELD_REQUIRED),
        ],
        render_kw = render_kw
    )

    submit = SubmitField('Ajouter', render_kw = render_kw_submit)