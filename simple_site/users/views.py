from flask import render_template, redirect, flash
from flask_login import current_user

from simple_site import db, login_manager
from simple_site.users import users
from simple_site.sessions import login_required
from simple_site.models import User
from .form import UserForm


@users.route('/account/new', methods=['GET'])
def new():
    form = UserForm()
    return render_template('users/new.html', form=form)


@users.route('/account', methods=['POST'])
def create():
    form = UserForm()
    if form.validate(current_user):
        user = form.to_user()
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect('/')
    return render_template('users/new.html', form=form)


@users.route('/account/<int:id>/edit', methods=['GET'])
@login_required()
def edit(id):
    user = User.query.filter(User.id == id).first_or_404()
    if not user.can_edit(current_user):
        return login_manager.unauthorized()
    form = UserForm(obj=user)
    return render_template('users/edit.html', form=form, user=user)


@users.route('/account/<int:id>', methods=['POST'])
@login_required()
def update(id):
    user = User.query.filter(User.id == id).first_or_404()
    if not user.can_edit(current_user):
        return login_manager.unauthorized()
    form = UserForm()
    if form.validate(current_user, user):
        form.update_user(user)
        db.session.add(user)
        db.session.commit()
        flash('Account updated!', 'success')
        return redirect('/')
    return render_template('users/edit.html', form=form, user=user)


@users.route('/account/<int:id>/destroy', methods=['POST'])
@login_required()
def destroy(id):
    user = User.query.filter(User.id == id).first_or_404()
    if not user.can_edit(current_user):
        return login_manager.unauthorized()
    db.session.delete(user)
    db.session.commit()
    flash('Account deleted', 'success')
    return redirect('/')
