from flask import render_template
from flask_login import current_user

from sarabande.admin import admin
from sarabande.sessions import login_required
from sarabande.models import Post, Page, User


@admin.route('/admin')
@login_required('user')
def posts():
    if current_user.is_admin:
        posts = Post.query.all()
    else:
        posts = Post.query.filter(Post.user_id == current_user.id).all()
    return render_template('admin_posts.html', posts=posts, active='posts')


@admin.route('/admin/pages')
@login_required('admin')
def pages():
    pages = Page.query.all()
    return render_template('admin_pages.html', pages=pages, active='pages')


@admin.route('/admin/users')
@login_required('admin')
def users():
    users = User.query.all()
    return render_template('admin_users.html', users=users, active='users')
