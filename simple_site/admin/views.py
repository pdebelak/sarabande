from flask import render_template

from simple_site.admin import admin
from simple_site.sessions import login_required
from simple_site.models import Post, Page


@admin.route('/admin')
@login_required('user')
def index():
    return render_template('admin/index.html')


@admin.route('/admin/posts')
@login_required('user')
def posts():
    posts = Post.query.all()
    return render_template('admin/posts.html', posts=posts)


@admin.route('/admin/pages')
@login_required('admin')
def pages():
    pages = Page.query.all()
    return render_template('admin/pages.html', pages=pages)
