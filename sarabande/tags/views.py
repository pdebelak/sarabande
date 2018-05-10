from flask import render_template

from sarabande.tags import tags
from sarabande.models import Tag, Post


@tags.route('/tags/<slug>', methods=['GET'])
def show(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    title = 'Posts tagged \'{0}\''.format(tag.name)
    posts = Post.query.join(Post.tags).filter(
        Tag.id == tag.id).filter(Post.published).all()
    return render_template('posts_index.html', posts=posts, title=title)
