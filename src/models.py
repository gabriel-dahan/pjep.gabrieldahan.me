from flask_login import UserMixin

from . import db

from datetime import datetime

###### SUBJECTS ######

class Subject(db.Model):
    __tablename__ = 'subjects'

    id: int = db.Column(db.Integer, primary_key = True)

    name: str = db.Column(db.String(15), unique = True, nullable = False)
    teacher: str = db.Column(db.String(20), nullable = False)
    color: str = db.Column(db.String(6), nullable = False) # HEX Color

    # FOREIGN KEYS
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    # RELATIONSHIPS
    actions = db.relationship('SubjectAction', backref = 'subject', lazy = True) # One-to-Many

class SubjectAction(db.Model):
    __tablename__ = 'subject_actions'

    id: int = db.Column(db.Integer, primary_key = True)

    description: str = db.Column(db.Text, nullable = False)

    # FOREIGN KEYS
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable = False)

###### JOURNAL ######

class JournalPage(db.Model):
    __tablename__ = 'journal_pages'

    id: int = db.Column(db.Integer, primary_key = True)

    date: datetime = db.Column(db.DateTime, nullable = False)
    content: str = db.Column(db.Text, nullable = False)

    # FOREIGN KEYS
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

###### HOLIDAYS PLANNING ######

class HolidaysPlanning(db.Model):
    __tablename__ = 'holidays_plannings'

    id: int = db.Column(db.Integer, primary_key = True)

    date_start: datetime = db.Column(db.DateTime, nullable = False)
    date_end: datetime = db.Column(db.DateTime, nullable = False)

    # FOREIGN KEYS
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    # Rel: HolidaysPlanningItem (OtM),

class HolidaysPlanningItem(db.Model):
    __tablename__ = 'holidays_plannings_items'

    id: int = db.Column(db.Integer, primary_key = True)

    content: str = db.Column(db.Text, nullable = False)
    time_spent: datetime = db.Column(db.DateTime, nullable = False)
    achieved: bool = db.Column(db.Boolean, nullable = False, default = False)

    # Rel: Subject (MtM), SubjectAction (MtM), 

###### WEEK PLANNING ######
    
class WeekPlanning(db.Model):
    __tablename__ = 'week_plannings'

    id: int = db.Column(db.Integer, primary_key = True)

    date_start: datetime = db.Column(db.DateTime, nullable = False)
    date_end: datetime = db.Column(db.DateTime, nullable = False)

    # FOREIGN KEYS
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

class WeekPlanningItem(db.Model):
    __tablename__ = 'week_plannings_items'

    id: int = db.Column(db.Integer, primary_key = True)

    hour_start: datetime = db.Column(db.DateTime, nullable = False)
    hour_end: datetime = db.Column(db.DateTime, nullable = False)

    content: str = db.Column(db.Text, nullable = False)

###### REPORT ######

class Report(db.Model):
    __tablename__ = 'reports'

    id: int = db.Column(db.Integer, primary_key = True)

    date_start: datetime = db.Column(db.DateTime, nullable = False)
    date_end: datetime = db.Column(db.DateTime, nullable = False)

    content: str = db.Column(db.Text, nullable = False)

    # FOREIGN KEYS
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key = True)

    name: str = db.Column(db.String(20), unique = True, nullable = False)
    passwd: str = db.Column(db.String(80), nullable = False)
    date_created: datetime = db.Column(db.DateTime, default = datetime.now(), nullable = False)

    # RELATIONSHIPS
    subjects = db.relationship('Subject', backref = 'user', lazy = True) # One-to-Many
    journal_pages = db.relationship('JournalPage', backref = 'author', lazy = True) # One-to-Many
    holidays_plannings = db.relationship('HolidayPlanning', backref = 'author', lazy = True) # One-to-Many
    week_plannings = db.relationship('WeekPlanning', backref = 'author', lazy = True) # One-to-Many
    reports = db.relationship('Report', backref = 'author', lazy = True) # One-to-Many

    def __repr__(self) -> str:
        return f'User(name: {self.name}, date_created: {self.date_created.strftime('%d-%m-%Y')})'