from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

from simple_site.models import Page


class PageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('Slug')
    body = TextAreaField('Body', validators=[DataRequired()])

    def to_page(self):
        return Page(
            title=self.title.data,
            slug=self.slug.data,
            body=self.body.data,
        )

    def update_page(self, page):
        page.title = self.title.data
        page.slug = self.slug.data
        page.body = self.body.data
