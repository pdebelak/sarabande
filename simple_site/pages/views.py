from flask import render_template, redirect, url_for, flash

from simple_site import db
from simple_site.pages import pages
from simple_site.models import Page
from simple_site.sessions import login_required
from .form import PageForm


@pages.route('/<slug>')
def show(slug):
    page = Page.query.filter(Page.slug == slug).first_or_404()
    return render_template('pages/show.html', page=page)


@pages.route('/pages/new', methods=['GET'])
@login_required('admin')
def new():
    form = PageForm()
    return render_template('pages/new.html', form=form)


@pages.route('/pages', methods=['POST'])
@login_required('admin')
def create():
    form = PageForm()
    if form.validate():
        page = form.to_page()
        db.session.add(page)
        db.session.commit()
        return redirect(url_for('page.show', slug=page.slug))
    return render_template('posts/new.html', form=form)


@pages.route('/pages/<slug>/edit', methods=['GET'])
@login_required('admin')
def edit(slug):
    page = Page.query.filter(Page.slug == slug).first_or_404()
    form = PageForm(obj=page)
    return render_template('pages/edit.html', form=form)


@pages.route('/pages/<slug>', methods=['POST'])
@login_required('admin')
def update(slug):
    page = Page.query.filter(Page.slug == slug).first_or_404()
    form = PageForm()
    if form.validate():
        form.update_page(page)
        db.session.add(page)
        db.session.commit()
        return redirect(url_for('page.show', slug=page.slug))
    return render_template('pages/edit.html', form=form)


@pages.route('/pages/<slug>/destroy', methods=['POST'])
@login_required('admin')
def destroy(slug):
    page = Page.query.filter(Page.slug == slug).first_or_404()
    db.session.delete(page)
    db.session.commit()
    flash('Page deleted', 'success')
    return redirect(url_for('admin.pages'))
