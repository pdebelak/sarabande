from flask_wtf import FlaskForm
from slugify import slugify
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

from sarabande.models import Post, Tag


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('Slug')
    body = TextAreaField('Body', validators=[DataRequired()])
    tag_names = StringField('Tags (comma separated)')

    def to_post(self, user=None):
        tags = self._find_or_build_tags()
        return Post(
            title=self.title.data,
            slug=self.slug.data,
            body=self.body.data,
            user=user,
            tags=tags,
        )

    def update_post(self, post):
        post.title = self.title.data
        post.slug = self.slug.data
        post.body = self.body.data
        post.tags = self._find_or_build_tags()

    def _find_or_build_tags(self):
        if not self.tag_names.data:
            return []
        requested_tags = [Tag(name=t.strip())
                          for t in self.tag_names.data.split(',')]
        tags = Tag.query.filter(
            Tag.slug.in_([tag.slug for tag in requested_tags])).all()
        found_tag_slugs = [tag.slug for tag in tags]
        for tag in requested_tags:
            if tag.slug not in found_tag_slugs:
                tags.append(tag)
        return tags
