from flask import render_template, flash, redirect
from flask_login import login_user, logout_user, current_user

from sarabande.sessions import sessions, login_required
from .form import LoginForm


@sessions.route('/sessions/new', methods=['GET'])
def login_form():
    if current_user.is_authenticated:
        flash('You are already logged in', 'error')
        return redirect('/')
    form = LoginForm()
    return render_template('sessions_new.html', form=form)


@sessions.route('/sessions', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate():
        login_user(form.user)
        flash('You are logged in!', 'success')
        return redirect('/')
    return render_template('sessions_new.html', form=form)


@sessions.route('/sessions/destroy', methods=['POST'])
@login_required()
def logout():
    logout_user()
    flash('You are logged out!', 'success')
    return redirect('/')
