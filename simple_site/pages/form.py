from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

from simple_site.models import Page


class PageForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    slug = StringField('slug')
    body = TextAreaField('body', validators=[DataRequired()])

    def to_page(self):
        return Page(
            title=self.title.data,
            slug=self.slug.data,
            body=self.body.data,
        )
