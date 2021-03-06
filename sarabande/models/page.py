from sarabande import db
from .cms_model import CMSModel


class Page(db.Model, CMSModel):
    __tablename__ = 'pages'

    title = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False, index=True)
    body = db.Column(db.Text, nullable=False)

    def __init__(self, *args, **kwargs):
        if not kwargs.get('slug'):
            kwargs['slug'] = self.slugify(kwargs.get('title', ''))
        super(Page, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Page {title}>'.format(title=self.title)
