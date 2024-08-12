from flask import redirect, url_for, request

from flask_login import current_user

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

from . import app

class SecuredAdminIndex(AdminIndexView):
    
    def is_accessible(self):
        return current_user.is_authenticated

class SecuredModelView(ModelView):

    column_display_pk = True
    column_hide_backrefs = False

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next = request.url))

class SecuredFileView(FileAdmin):

    def is_accessible(self):
        return current_user.is_authenticated
    
# Custom views

class SubjectView(SecuredModelView):
    form_columns = ['name', 'teacher', 'color', 'user']
    
admin = Admin(
    app, 
    name = 'PJEP - Admin Page', 
    template_mode = 'bootstrap4',
    index_view = SecuredAdminIndex()
)