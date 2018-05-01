from faker import Faker

from simple_site.models import Post, User, Page, Image


faker = Faker()


def _build_model(model, defaults, kwargs):
    defaults.update(kwargs)
    return model(**defaults)


def build_user(**kwargs):
    defaults = {
        'username': faker.name(),
        'user_type': 'user',
        'password': 'password',
    }
    return _build_model(User, defaults, kwargs)


def build_post(**kwargs):
    defaults = {
        'title': faker.sentence(),
        'body': faker.text(),
        'user': build_user(),
    }
    return _build_model(Post, defaults, kwargs)


def build_page(**kwargs):
    defaults = {
        'title': faker.sentence(),
        'body': faker.text(),
    }
    return _build_model(Page, defaults, kwargs)


def build_image(**kwargs):
    defaults = {
        'name': 'image.png',
        'mimetype': 'images/png',
        'image': b'image-data',
        'user': build_user(),
    }
    return _build_model(Image, defaults, kwargs)
