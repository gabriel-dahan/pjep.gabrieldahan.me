from flask import render_template
from flask_login import current_user

from .. import app
from ..models import JournalPage

@app.route('/')
def home():
    return render_template('pjep/home.html')

@app.route('/journal')
def journal():
    return render_template('pjep/journal.html', 
        journal_pages = JournalPage.query.filter_by(author_id = current_user.get_id()).all()
    )