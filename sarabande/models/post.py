from bs4 import BeautifulSoup
from markupsafe import Markup
from slugify import slugify

from sarabande import db
from .posts_tags import posts_tags


class Post(db.Model):
    __tablename__ = 'posts'

    title = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False, index=True)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False,
                        index=True)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    tags = db.relationship('Tag', secondary=posts_tags,
                           back_populates='posts', lazy=True)

    def __init__(self, *args, **kwargs):
        if not kwargs.get('slug'):
            kwargs['slug'] = slugify(kwargs.get('title', ''))
        super(Post, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Post {title}>'.format(title=self.title)

    @property
    def html_body(self):
        return Markup(self.body)

    @property
    def author_name(self):
        return self.user.username

    @property
    def summary(self):
        return Markup(BeautifulSoup(self.body, 'html.parser').contents[0])

    @property
    def tag_names(self):
        return ', '.join([tag.name for tag in self.tags])

    def can_edit(self, user):
        return user.is_admin or self.user_id == user.id
