from flask import render_template, redirect, flash
from flask_login import current_user, login_user
from sqlalchemy.exc import IntegrityError

from sarabande import db, login_manager
from sarabande.users import users
from sarabande.sessions import login_required
from sarabande.models import User
from .form import UserForm


@users.route('/account/new', methods=['GET'])
def new():
    form = UserForm()
    return render_template('users_new.html', form=form)


@users.route('/account', methods=['POST'])
def create():
    form = UserForm()
    if form.validate(current_user):
        user = form.to_user()
        try:
            db.session.add(user)
            db.session.commit()
            if not current_user.is_authenticated:
                login_user(user)
            flash('Account created!', 'success')
            return redirect('/')
        except IntegrityError:
            db.session.rollback()
            form.username.errors.append('This name has been taken.')
    return render_template('users_new.html', form=form)


@users.route('/account/edit', methods=['GET'])
@login_required()
def edit_self():
    form = UserForm(obj=current_user)
    return render_template('users_edit.html', form=form, user=current_user)


@users.route('/account/<int:id>/edit', methods=['GET'])
@login_required('admin')
def edit(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    return render_template('users_edit.html', form=form, user=user)


@users.route('/account/<int:id>', methods=['POST'])
@login_required()
def update(id):
    user = User.query.get_or_404(id)
    if not user.can_edit(current_user):
        return login_manager.unauthorized()
    form = UserForm()
    if form.validate(current_user, user):
        form.update_user(user)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Account updated!', 'success')
            return redirect('/')
        except IntegrityError:
            db.session.rollback()
            form.username.errors.append('This name has been taken.')
    return render_template('users_edit.html', form=form, user=user)


@users.route('/account/<int:id>/destroy', methods=['POST'])
@login_required()
def destroy(id):
    user = User.query.get_or_404(id)
    if not user.can_edit(current_user):
        return login_manager.unauthorized()
    db.session.delete(user)
    db.session.commit()
    flash('Account deleted', 'success')
    return redirect('/')
