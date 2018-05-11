import re

from bs4 import BeautifulSoup
from markupsafe import Markup
from slugify import slugify


def _replace_magic_text(text):
    return re.sub(
        r'<p>\s*===\s*</p>(.+?)<p>\s*===\s*</p>',
        lambda match: Markup(match.group(1)).unescape(),
        text)


class CMSModel(object):
    def slugify(self, item):
        return slugify(item or '')

    @property
    def html_body(self):
        return Markup(_replace_magic_text(self.body))

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
