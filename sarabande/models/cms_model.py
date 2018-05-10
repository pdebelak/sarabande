from bs4 import BeautifulSoup
from markupsafe import Markup
from slugify import slugify


class CMSModel(object):
    def slugify(self, item):
        return slugify(item or '')

    @property
    def html_body(self):
        return Markup(self.body)

    @property
    def summary(self):
        return Markup(BeautifulSoup(self.body, 'html.parser').contents[0])

    @property
    def description(self):
        return BeautifulSoup(self.body, 'html.parser').contents[0].text

    @property
    def image_url(self):
        image = BeautifulSoup(self.body, 'html.parser').img
        if image:
            return image.attrs['src']
