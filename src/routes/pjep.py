from flask import render_template
from flask_login import current_user, login_required

from .. import app
from ..models import JournalPage

import datetime

@app.route('/')
def home():
    return render_template('pjep/home.html')

@app.route('/journal')
@login_required
def journal():
    return render_template('pjep/journal.html', 
        journal_pages = JournalPage.query.filter_by(author_id = current_user.get_id()).all()
    )

@app.route('/journal/<date>')
@login_required
def journal_page(date: str):
    # date format is dd-mm-yyyy
    d, m, y = date.split('-')
    date_obj = datetime.date(year = int(y), month = int(m), day = int(d))
    page = JournalPage.query.filter_by(date = date_obj, author_id = current_user.get_id()).first()
    if page:
        return render_template('pjep/journal_page.html', journal_page = page)
    return render_template('404.html')

@app.route('/plans')
@login_required
def plannings():
    return render_template('pjep/plannings.html')

@app.route('/plans/holidays')
@login_required
def holidays_plannings():
    return render_template('pjep/holidays_plans.html')