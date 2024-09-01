from flask import render_template, request, redirect, url_for, send_file
from flask_login import current_user, login_required
from sqlalchemy.sql import func

from .. import app, db
from ..models import JournalPage, Subject, JournalPageItem, Report
from ..forms import EditJournalPageItemForm, AddJournalPageForm

from ..utils import html_to_pdf

import io
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
    date_obj = datetime.strptime(date, '%d-%m-%Y')
    page: JournalPage = JournalPage.query \
        .filter_by(author_id = current_user.get_id()) \
        .filter(func.date(JournalPage.date) == date_obj.date()) \
        .first()
    
    choices = [
        (subject.id, subject.name) for subject in Subject.query.all()
    ]
    add_item_form = EditJournalPageItemForm()
    add_item_form.subject.choices = choices
    if page:
        if add_item_form.validate_on_submit():
            method = add_item_form.method.data or 'POST'

            hour_start = datetime.combine(page.date, add_item_form.hour_start.data)
            hour_end = datetime.combine(page.date, add_item_form.hour_end.data)
            content = add_item_form.content.data
            subject_id = int(add_item_form.subject.data)
            journal_id = page.id

            if method == 'POST':
                new_item = JournalPageItem(
                    hour_start = hour_start,
                    hour_end = hour_end,
                    content = content,
                    subject_id = subject_id,
                    journal_id = journal_id
                )
                db.session.add(new_item)
                db.session.commit()
            elif method == 'PUT':
                item = JournalPageItem.query.filter_by(id = int(add_item_form.item_id.data)).first()
                if item:
                    item.hour_start = hour_start
                    item.hour_end = hour_end
                    item.content = content
                    item.subject_id = subject_id
                    db.session.commit()
            elif method == 'DELETE':
                item = JournalPageItem.query.filter_by(id = int(add_item_form.item_id.data)).first()
                if item:
                    db.session.delete(item)
                    db.session.commit()
        return render_template('pjep/journal/page_edit.html', 
            page = page, 
            form = add_item_form
        )
    return render_template('404.html')

@app.route('/journal/<date>/delete')
@login_required
def journal_page_delete(date: str):
    date_obj = datetime.strptime(date, '%d-%m-%Y')
    page: JournalPage = JournalPage.query \
        .filter_by(author_id = current_user.get_id()) \
        .filter(func.date(JournalPage.date) == date_obj.date()) \
        .first()
    
    if page:
        db.session.delete(page)
        db.session.commit()
        return redirect(url_for('journal'))
    return render_template('404.html')

@app.route('/journal/raw')
@login_required
def journal_raw():
    pages = JournalPage.query.filter_by(author_id = current_user.get_id()).all()
    return render_template('pjep/journal/raw.html', pages = pages)

@app.route('/journal/raw/pdf')
@login_required
def journal_raw_pdf():
    pages = JournalPage.query.filter_by(author_id = current_user.get_id()).all()
    pdf = html_to_pdf('pjep/journal/raw.html', pages = pages)

    if not pdf:
        return "Erreur lors de la création du PDF", 500
    
    return send_file(
        pdf,
        mimetype = 'application/pdf',
        download_name = 'journal.pdf',
        as_attachment = False
    )

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
    reports = Report.query.filter_by(author_id = current_user.get_id()).all()
    return render_template('pjep/reports.html', reports = reports)

@app.route('/subjects')
@login_required
def subjects():
    subjects_ = Subject.query.filter_by(user = current_user).all()
    return render_template('pjep/subjects.html', subjects = subjects_)