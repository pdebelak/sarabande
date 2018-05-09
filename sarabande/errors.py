from flask import render_template

from sarabande import app, login_manager


@app.errorhandler(401)
@login_manager.unauthorized_handler
def unauthorized(e=None):
    return render_template('forbidden.html'), 401


@app.errorhandler(403)
def forbidden(e):
    return render_template('forbidden.html'), 403


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def unhandled_error(e):
    return render_template('500.html'), 500
