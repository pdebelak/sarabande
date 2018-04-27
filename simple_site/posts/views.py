from flask import render_template, redirect, url_for, flash
from flask_login import current_user

from simple_site import db, login_manager
from simple_site.posts import posts
from simple_site.models import Post
from simple_site.sessions import login_required
from .form import PostForm


@posts.route('/posts', methods=['GET'])
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)


@posts.route('/posts/<slug>', methods=['GET'])
def show(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('posts/show.html', post=post)


@posts.route('/posts/new', methods=['GET'])
@login_required('user')
def new():
    form = PostForm()
    return render_template('posts/new.html', form=form)


@posts.route('/posts', methods=['POST'])
@login_required('user')
def create():
    form = PostForm()
    if form.validate():
        post = form.to_post(user=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.show', slug=post.slug))
    return render_template('posts/new.html', form=form)


@posts.route('/posts/<slug>/edit', methods=['GET'])
@login_required('user')
def edit(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    if not post.can_edit(current_user):
        return login_manager.unauthorized()
    form = PostForm(obj=post)
    return render_template('posts/edit.html', form=form)


@posts.route('/posts/<slug>', methods=['POST'])
@login_required('user')
def update(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    if not post.can_edit(current_user):
        return login_manager.unauthorized()
    form = PostForm()
    if form.validate():
        form.update_post(post)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.show', slug=post.slug))
    return render_template('posts/edit.html', form=form)


@posts.route('/posts/<slug>/destroy', methods=['POST'])
@login_required('user')
def destroy(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    if not post.can_edit(current_user):
        return login_manager.unauthorized()
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted')
    return redirect(url_for('posts.index'))
