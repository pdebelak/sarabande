from markupsafe import Markup
from slugify import slugify

from simple_site import db


class Post(db.Model):
    __tablename__ = 'posts'

    title = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False, index=True)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

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

    def can_edit(self, user):
        return user.is_admin or self.user_id == user.id
