from flask import render_template

from .. import app

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')