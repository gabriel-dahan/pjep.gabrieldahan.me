from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

from dotenv import dotenv_values

import os

CONF = dotenv_values('.env')

app = Flask(
    __name__,
    static_url_path='', 
    static_folder='static',
    template_folder='templates'
)
app.config['SECRET_KEY'] = CONF['SECRET']

app.url_map.strict_slashes = False

__cors = CORS(app)

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = CONF['DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MIGRATE
migrate = Migrate(app, db)

# LOGIN MANAGER
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = user_id).first()

from .routes import *
from .models import *

# ADMIN PAGE 
    
from .admin import *

path = os.path.join(os.path.dirname(__file__), 'static')
admin.add_view(SecuredFileView(path, '/static/', name = 'Static Files'))

admin.add_view(SecuredModelView(User, db.session))

admin.add_view(SubjectView(Subject, db.session))
admin.add_view(SecuredModelView(SubjectAction, db.session))

admin.add_view(SecuredModelView(JournalPage, db.session))
admin.add_view(SecuredModelView(JournalPageItem, db.session))

admin.add_view(SecuredModelView(HolidaysPlanning, db.session))
admin.add_view(SecuredModelView(HolidaysPlanningItem, db.session))

admin.add_view(SecuredModelView(WeekPlanning, db.session))
admin.add_view(SecuredModelView(WeekPlanningItem, db.session))

admin.add_view(SecuredModelView(Report, db.session))