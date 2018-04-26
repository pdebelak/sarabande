from flask import abort, render_template, redirect, url_for
from flask_login import login_required, current_user

from simple_site import db
from simple_site.posts import posts
from simple_site.models import Post
from .form import PostForm


@posts.route('/posts', methods=['GET'])
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)


@posts.route('/posts/<slug>', methods=['GET'])
def show(slug):
    post = Post.query.filter(Post.slug == slug).first()
    if post is None:
        abort(404)
    return render_template('posts/show.html', post=post)


@posts.route('/posts/new', methods=['GET'])
@login_required
def new():
    form = PostForm()
    return render_template('posts/new.html', form=form)


@posts.route('/posts', methods=['POST'])
@login_required
def create():
    form = PostForm()
    if form.validate():
        post = form.to_post(current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.show', slug=post.slug))
    return render_template('posts/new.html', form=form)
