from flask import abort, render_template, redirect, url_for
from flask_login import login_required

from simple_site import db
from simple_site.pages import pages
from simple_site.models import Page
from .form import PageForm


@pages.route('/<slug>')
def show(slug):
    page = Page.query.filter(Page.slug == slug).first()
    if page is None:
        abort(404)
    return render_template('pages/show.html', page=page)


@pages.route('/pages/new', methods=['GET'])
@login_required
def new():
    form = PageForm()
    return render_template('pages/new.html', form=form)


@pages.route('/pages', methods=['POST'])
@login_required
def create():
    form = PageForm()
    if form.validate():
        page = form.to_page()
        db.session.add(page)
        db.session.commit()
        return redirect(url_for('page.show', slug=page.slug))
    return render_template('posts/new.html', form=form)
