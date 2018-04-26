from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired

from simple_site.models import Post


class PostForm(FlaskForm):
    title = TextField('title', validators=[DataRequired()])
    slug = TextField('slug')
    body = TextAreaField('body', validators=[DataRequired()])

    def to_post(self, user=None):
        return Post(
            title=self.title.data,
            slug=self.slug.data,
            body=self.body.data,
            user=user,
        )
