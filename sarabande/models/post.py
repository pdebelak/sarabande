from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from sarabande import db
from .cms_model import CMSModel
from .posts_tags import posts_tags


class Post(db.Model, CMSModel):
    __tablename__ = 'posts'

    title = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False, index=True)
    body = db.Column(db.Text, nullable=False)
    published_at = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False,
                        index=True)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    tags = db.relationship('Tag', secondary=posts_tags,
                           back_populates='posts', lazy=True)

    def __init__(self, *args, **kwargs):
        if not kwargs.get('slug'):
            kwargs['slug'] = self.slugify(kwargs.get('title'))
        super(Post, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Post {title}>'.format(title=self.title)

    @property
    def author_name(self):
        return self.user.username

    @property
    def tag_names(self):
        return ', '.join([tag.name for tag in self.tags])

    @hybrid_property
    def published(self):
        return self.published_at and self.published_at <= datetime.utcnow()

    def can_edit(self, user):
        if not user.is_authenticated:
            return False
        return user.is_admin or self.user_id == user.id
