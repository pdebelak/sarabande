from flask import render_template, flash, redirect
from flask_login import login_user, logout_user, login_required

from simple_site.sessions import sessions
from .form import LoginForm


@sessions.route('/sessions/new', methods=['GET'])
def login_form():
    form = LoginForm()
    return render_template('sessions/new.html', form=form)


@sessions.route('/sessions', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate():
        login_user(form.user)
        flash('You are logged in!')
        return redirect('/')
    return render_template('sessions/new.html', form=form)


@sessions.route('/sessions/destroy', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You are logged out!')
    return redirect('/')
