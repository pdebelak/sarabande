from flask import render_template

from sarabande.tags import tags
from sarabande.models import Tag, Post


@tags.route('/tags/<slug>', methods=['GET'])
def show(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    title = 'Posts tagged \'{0}\''.format(tag.name)
    pagination = Post.query.join(Post.tags).filter(
        Tag.id == tag.id).filter(Post.published).paginate(per_page=5)
    return render_template('posts_index.html', posts=pagination.items,
                           title=title, pagination=pagination)
