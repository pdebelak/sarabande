from operator import attrgetter

from flask import render_template, redirect, url_for, flash, abort
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from sarabande import db, login_manager
from sarabande.posts import posts
from sarabande.models import Post, Comment
from sarabande.sessions import login_required
from .form import PostForm, CommentForm


@posts.route('/posts', methods=['GET'])
def index():
    posts = Post.query.filter(Post.published).order_by(
        Post.published_at.desc()).all()
    return render_template('posts_index.html', posts=posts)


@posts.route('/posts/<slug>', methods=['GET'])
def show(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    if post.published or post.can_edit(current_user):
        return render_template('posts_show.html', post=post)
    abort(404)


@posts.route('/posts/new', methods=['GET'])
@login_required('user')
def new():
    form = PostForm()
    return render_template('posts_new.html', form=form)


@posts.route('/posts', methods=['POST'])
@login_required('user')
def create():
    form = PostForm()
    if form.validate():
        try:
            post = form.to_post(user=current_user)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('posts.show', slug=post.slug))
        except IntegrityError:
            db.session.rollback()
            form.slug.errors.append('This slug is taken.')
    return render_template('posts_new.html', form=form)


@posts.route('/posts/<slug>/edit', methods=['GET'])
@login_required('user')
def edit(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    if not post.can_edit(current_user):
        return login_manager.unauthorized()
    form = PostForm(obj=post)
    form.tag_names.data = post.tag_names
    return render_template('posts_edit.html', form=form)


@posts.route('/posts/<slug>', methods=['POST'])
@login_required('user')
def update(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    if not post.can_edit(current_user):
        return login_manager.unauthorized()
    form = PostForm()
    if form.validate():
        try:
            form.update_post(post)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('posts.show', slug=post.slug))
        except IntegrityError:
            db.session.rollback()
            form.slug.errors.append('This slug is taken.')
    return render_template('posts_edit.html', form=form)


@posts.route('/posts/<slug>/destroy', methods=['POST'])
@login_required('user')
def destroy(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    if not post.can_edit(current_user):
        return login_manager.unauthorized()
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted', 'success')
    return redirect(url_for('admin.posts'))


@posts.route('/posts/<slug>/comments', methods=['GET'])
def comments_index(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    comments = sorted(post.comments, key=attrgetter('updated_at'))
    return render_template('comments_index.html', post=post, comments=comments)


@posts.route('/posts/<slug>/comments/new', methods=['GET'])
@login_required()
def comments_new(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    form = CommentForm()
    return render_template('comments_new.html', form=form, post=post)


@posts.route('/posts/<slug>/comments', methods=['POST'])
@login_required()
def comments_create(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    form = CommentForm()
    if form.validate():
        comment = form.to_comment(user=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('posts.comments_index', slug=slug))
    return render_template('comments_new.html', form=form, post=post)


@posts.route('/comments/<int:id>/destroy', methods=['POST'])
@login_required('user')
def comments_destroy(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted', 'success')
    return redirect(url_for('admin.comments'))
