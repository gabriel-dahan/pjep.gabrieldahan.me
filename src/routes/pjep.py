from flask import render_template, request
from flask_login import current_user, login_required
from sqlalchemy.sql import func

from .. import app
from ..models import JournalPage, Subject
from ..forms import AddJournalPageItemForm

from datetime import datetime

week_days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

@app.route('/')
def home():
    return render_template('pjep/home.html')

@app.route('/journal')
@login_required
def journal():
    journal_pages = JournalPage.query.filter_by(author_id = current_user.get_id())

    return render_template('pjep/journal.html', 
        journal_pages = journal_pages.all(), 
        journal_page = journal_pages.filter(func.date(JournalPage.date) == datetime.now().date()).first(),

        week_days = week_days,
        months = months
    )

@app.route('/journal/<date>')
@login_required
def journal_page(date: str): # date format : dd-mm-yyyy
    date_obj = datetime.strptime(date, '%d-%m-%Y')
    page = JournalPage.query \
        .filter_by(author_id = current_user.get_id()) \
        .filter(func.date(JournalPage.date) == date_obj.date()) \
        .first()
    if page:
        return render_template('pjep/journal_page.html', 
            journal_page = page, 
            week_days = week_days, 
            months = months
        )
    return render_template('404.html')

@app.route('/journal/<date>/edit', methods = ['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def journal_page_edit(date: str):
    method = request.method
    date_obj = datetime.strptime(date, '%d-%m-%Y')
    page = JournalPage.query \
        .filter_by(author_id = current_user.get_id()) \
        .filter(func.date(JournalPage.date) == date_obj.date()) \
        .first()
    
    choices = [
        (subject.id, subject.name) for subject in Subject.query.all()
    ]
    add_item_form = AddJournalPageItemForm()
    add_item_form.subject.choices = choices
    if page:
        return render_template('pjep/journal_page_edit.html', journal_page = page, form = add_item_form, week_days = week_days, months = months)
    return render_template('404.html')

@app.route('/plans')
@login_required
def plannings():
    return render_template('pjep/plannings.html')

@app.route('/plans/holidays')
@login_required
def holidays_plannings():
    return render_template('pjep/holidays_plans.html')