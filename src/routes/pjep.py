from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy.sql import func

from .. import app, db
from ..models import JournalPage, Subject
from ..forms import AddJournalPageItemForm, AddJournalPageForm

from datetime import datetime

@app.route('/')
def home():
    return render_template('pjep/home.html')

@app.route('/journal')
@login_required
def journal():
    journal_pages = JournalPage.query.filter_by(author_id = current_user.get_id())

    return render_template('pjep/journal/journal.html', 
        pages = journal_pages.all(), 
        page = journal_pages.filter(func.date(JournalPage.date) == datetime.now().date()).first()
    )

@app.route('/journal/new-page', methods=['GET', 'POST'])
@login_required
def journal_new_page():
    form = AddJournalPageForm()

    if form.validate_on_submit():
        page = JournalPage(
            date = form.date.data,
            content = form.description.data,
            author_id = current_user.id
        )
        db.session.add(page)
        db.session.commit()

        return redirect(url_for('journal_page', date = page.date.strftime('%d-%m-%Y')))

    return render_template('pjep/journal/new_page.html', form = form)

@app.route('/journal/<date>')
@login_required
def journal_page(date: str): # date format : dd-mm-yyyy
    date_obj = datetime.strptime(date, '%d-%m-%Y')
    page = JournalPage.query \
        .filter_by(author_id = current_user.get_id()) \
        .filter(func.date(JournalPage.date) == date_obj.date()) \
        .first()
    
    if page:
        return render_template('pjep/journal/page.html', page = page)
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
        return render_template('pjep/journal/page_edit.html', 
            page = page, 
            form = add_item_form
        )
    return render_template('404.html')

@app.route('/plans')
@login_required
def plannings():
    return render_template('pjep/plannings.html')

@app.route('/plans/holidays')
@login_required
def holidays_plannings():
    return render_template('pjep/holidays_plans.html')

@app.route('/reports')
@login_required
def reports():
    return render_template('pjep/reports.html')