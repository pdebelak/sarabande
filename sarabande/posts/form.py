from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Optional
from wtforms.ext.dateutil.fields import DateTimeField

from sarabande.models import Post, Tag, Comment


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('Slug')
    body = TextAreaField('Body', validators=[DataRequired()])
    published = BooleanField('Published')
    published_at = DateTimeField(
        'Publish time (in UTC)', display_format='%Y-%m-%dT%H:%M',
        validators=[Optional()])
    tag_names = StringField('Tags (comma separated)')

    def to_post(self, user=None):
        tags = self._find_or_build_tags()
        published_at = self._get_published_at()
        return Post(
            title=self.title.data,
            slug=self.slug.data,
            body=self.body.data,
            published_at=published_at,
            user=user,
            tags=tags,
        )

    def update_post(self, post):
        post.title = self.title.data
        post.slug = self.slug.data
        post.body = self.body.data
        post.tags = self._find_or_build_tags()
        post.published_at = self._get_published_at()

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

    def _get_published_at(self):
        if self.published_at.data:
            return self.published_at.data
        if self.published.data:
            return datetime.utcnow()
        return None


class CommentForm(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])

    def to_comment(self, user=None, post=None):
        return Comment(
            body=self.body.data,
            user=user,
            post=post,
        )
