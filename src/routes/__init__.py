from .auth import *
from .pjep import *
from .ext import *

week_days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

@app.context_processor
def inject_globals():
    return dict(
        week_days = week_days, 
        months = months,
        now = datetime.now
    )