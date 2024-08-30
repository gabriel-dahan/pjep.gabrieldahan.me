class FormErrors:

    FIELD_REQUIRED = "Ce champ est requis."
    INVALID_LENGTH = "Le nom d'utilisateur doit être compris entre {min} et {max} caractères."
    PASSWORD_DOESNT_MATCH = "Les mots de passe ne correspondent pas."
    USERNAME_ALREADY_EXISTS = "Ce nom d'utilisateur existe déjà."
    USERNAME_DOESNT_EXISTS = "Ce nom d'utilisateur n'existe pas."
    INVALID_PASSWORD = "Le mot de passe est incorrect."

render_kw = dict(
    class_ = 'form-control'
)
render_kw_submit = dict(
    class_ = 'btn btn-primary'
)

from .auth import *
from .pjep import *