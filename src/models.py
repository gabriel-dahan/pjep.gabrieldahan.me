from flask_login import UserMixin

from . import db

from datetime import datetime

###### SUBJECTS ######

class Subject(db.Model):
    __tablename__ = 'subjects'

    id: int = db.Column(db.Integer, primary_key = True)

    name: str = db.Column(db.String(15), unique = True, nullable = False)
    teacher: str = db.Column(db.String(20))
    color: str = db.Column(db.String(6), nullable = False) # HEX Color

    # FOREIGN KEYS
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    # RELATIONSHIPS
    actions = db.relationship('SubjectAction', backref = 'subject', lazy = True) # One-to-Many
    journal_items = db.relationship('JournalPageItem', backref = 'subject', lazy = True) # One-to-Many
    holidays_items = db.relationship('HolidaysPlanningItem', backref = 'subject', lazy = True) # One-to-Many
    week_items = db.relationship('WeekPlanningItem', backref = 'subject', lazy = True) # One-to-Many

    user = db.relationship('User', backref = 'subjects', lazy = True) # One-to-Many

    def __repr__(self) -> str:
        return f'Subject(name: {self.name}, teacher: {self.teacher})'


class SubjectAction(db.Model):
    __tablename__ = 'subject_actions'

    id: int = db.Column(db.Integer, primary_key = True)

    description: str = db.Column(db.Text, nullable = False)

    # FOREIGN KEYS
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable = False)

    def __repr__(self) -> str:
        return f'SubjectAction(description: {self.description})'

###### JOURNAL ######

class JournalPage(db.Model):
    __tablename__ = 'journal_pages'

    id: int = db.Column(db.Integer, primary_key = True)

    date: datetime = db.Column(db.DateTime, nullable = False)
    content: str = db.Column(db.Text, nullable = False)

    # FOREIGN KEYS
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    # RELATIONSHIPS
    items = db.relationship('JournalPageItem', backref = 'journal', lazy = True) # One-to-Many

    def __repr__(self) -> str:
        return f'JournalPage(date: {self.date.strftime('%d/%m/%Y')})'

class JournalPageItem(db.Model):
    __tablename__ = 'journal_pages_items'

    id: int = db.Column(db.Integer, primary_key = True)

    hour_start: datetime = db.Column(db.DateTime, nullable = False)
    hour_end: datetime = db.Column(db.DateTime, nullable = False)

    content: str = db.Column(db.Text, nullable = False)

    # FOREIGN KEYS
    journal_id = db.Column(db.Integer, db.ForeignKey('journal_pages.id'), nullable = False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable = False)

    def __repr__(self) -> str:
        return f'JournalPageItem(date: {self.journal.date.strftime('%d/%m/%Y')}, hour_start: {self.hour_start.strftime('%H:%M')}, hour_end: {self.hour_end.strftime('%H:%M')}, content: {self.content})'

###### HOLIDAYS PLANNING ######

class HolidaysPlanning(db.Model):
    __tablename__ = 'holidays_plannings'

    id: int = db.Column(db.Integer, primary_key = True)

    date_start: datetime = db.Column(db.DateTime, nullable = False)
    date_end: datetime = db.Column(db.DateTime, nullable = False)

    # FOREIGN KEYS
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    # RELATIONSHIPS
    items = db.relationship('HolidaysPlanningItem', backref = 'planning', lazy = True) # One-to-Many

    def __repr__(self) -> str:
        return f'HolidaysPlanning(date_start: {self.date_start.strftime('%d/%m/%Y')}, date_end: {self.date_end.strftime('%d/%m/%Y')})'

class HolidaysPlanningItem(db.Model):
    __tablename__ = 'holidays_plannings_items'

    id: int = db.Column(db.Integer, primary_key = True)

    content: str = db.Column(db.Text, nullable = False)
    time_spent: datetime = db.Column(db.DateTime, nullable = False)
    achieved: bool = db.Column(db.Boolean, nullable = False, default = False)

    # FOREIGN KEYS
    planning_id = db.Column(db.Integer, db.ForeignKey('holidays_plannings.id'), nullable = False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable = False)

    def __repr__(self) -> str:
        return f'HolidaysPlanningItem(time_spent: {self.time_spent.strftime('%H:%M')}, content: {self.content}, achieved: {self.achieved})'

###### WEEK PLANNING ######
    
class WeekPlanning(db.Model):
    __tablename__ = 'week_plannings'

    id: int = db.Column(db.Integer, primary_key = True)

    date_start: datetime = db.Column(db.DateTime, nullable = False)
    date_end: datetime = db.Column(db.DateTime, nullable = False)

    # FOREIGN KEYS
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    # RELATIONSHIPS
    items = db.relationship('WeekPlanningItem', backref = 'planning', lazy = True) # One-to-Many

    def __repr__(self) -> str:
        return f'WeekPlanning(date_start: {self.date_start.strftime('%d/%m/%Y')}, date_end: {self.date_end.strftime('%d/%m/%Y')})'

class WeekPlanningItem(db.Model):
    __tablename__ = 'week_plannings_items'

    id: int = db.Column(db.Integer, primary_key = True)

    hour_start: datetime = db.Column(db.DateTime, nullable = False)
    hour_end: datetime = db.Column(db.DateTime, nullable = False)

    content: str = db.Column(db.Text, nullable = False)

    # FOREIGN KEYS
    planning_id = db.Column(db.Integer, db.ForeignKey('week_plannings.id'), nullable = False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable = False)

    def __repr__(self) -> str:
        return f'WeekPlanningItem(hour_start: {self.hour_start.strftime('%H:%M')}, hour_end: {self.hour_end.strftime('%H:%M')}, content: {self.content})'

###### REPORT ######

class Report(db.Model):
    __tablename__ = 'reports'

    id: int = db.Column(db.Integer, primary_key = True)

    date_start: datetime = db.Column(db.DateTime, nullable = False)
    date_end: datetime = db.Column(db.DateTime, nullable = False)

    content: str = db.Column(db.Text, nullable = False)

    # FOREIGN KEYS
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    def __repr__(self) -> str:
        return f'Report(date_start: {self.date_start.strftime('%d/%m/%Y')}, date_end: {self.date_end.strftime('%d/%m/%Y')}, content: {self.content})'

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key = True)

    name: str = db.Column(db.String(20), unique = True, nullable = False)
    passwd: str = db.Column(db.String(80), nullable = False)
    date_created: datetime = db.Column(db.DateTime, default = datetime.now(), nullable = False)

    # RELATIONSHIPS
    journal_pages = db.relationship('JournalPage', backref = 'author', lazy = True) # One-to-Many
    holidays_plannings = db.relationship('HolidaysPlanning', backref = 'author', lazy = True) # One-to-Many
    week_plannings = db.relationship('WeekPlanning', backref = 'author', lazy = True) # One-to-Many
    reports = db.relationship('Report', backref = 'author', lazy = True) # One-to-Many

    def __repr__(self) -> str:
        return f'User(name: {self.name}, date_created: {self.date_created.strftime('%d-%m-%Y')})'