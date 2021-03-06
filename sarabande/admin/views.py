from flask import render_template
from flask_login import current_user

from sarabande.admin import admin
from sarabande.sessions import login_required
from sarabande.models import Post, Page, User, Comment


@admin.route('/admin')
@login_required('user')
def posts():
    if current_user.is_admin:
        posts = Post.query.all()
    else:
        posts = current_user.posts
    return render_template('admin_posts.html', posts=posts)


@admin.route('/admin/comments')
@login_required('user')
def comments():
    comments = Comment.query.all()
    return render_template('admin_comments.html', comments=comments)


@admin.route('/admin/pages')
@login_required('admin')
def pages():
    pages = Page.query.all()
    return render_template('admin_pages.html', pages=pages)


@admin.route('/admin/users')
@login_required('admin')
def users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)
