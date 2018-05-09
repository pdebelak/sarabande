from autolink import linkify
from markupsafe import Markup, escape

from sarabande import db


class Comment(db.Model):
    __tablename__ = 'comments'

    body = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False,
                        index=True)
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False,
                        index=True)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return '<Comment {body}>'.format(body=self.body[:20])

    @property
    def author_name(self):
        return self.user.username

    @property
    def html_body(self):
        return Markup(linkify(escape(self.body)))
