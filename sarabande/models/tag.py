from slugify import slugify

from sarabande import db
from .posts_tags import posts_tags


class Tag(db.Model):
    __tablename__ = 'tags'

    name = db.Column(db.String, nullable=False, index=True, unique=True)
    slug = db.Column(db.String, nullable=False, index=True, unique=True)
    posts = db.relationship('Post', secondary=posts_tags,
                            back_populates='tags', lazy=True)

    def __init__(self, *args, **kwargs):
        if not kwargs.get('slug'):
            kwargs['slug'] = slugify(kwargs.get('name', ''))
        super(Tag, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Tag {name}>'.format(name=self.name)
