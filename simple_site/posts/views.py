from flask import abort, render_template
from simple_site.models import Post
from simple_site.posts import posts


@posts.route('/posts')
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts=posts)


@posts.route('/posts/<slug>')
def show(slug):
    post = Post.query.filter(Post.slug == slug).first()
    if post is None:
        abort(404)
    return render_template('posts/show.html', post=post)
