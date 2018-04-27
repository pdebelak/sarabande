from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

from simple_site.models import Post


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    slug = StringField('slug')
    body = TextAreaField('body', validators=[DataRequired()])

    def to_post(self, user=None):
        return Post(
            title=self.title.data,
            slug=self.slug.data,
            body=self.body.data,
            user=user,
        )

    def update_post(self, post):
        post.title = self.title.data
        post.slug = self.slug.data
        post.body = self.body.data
