import re
import unittest

from sarabande import app, db
from sarabande.models import User, Post, Page, Image, Tag, Comment
from sarabande.models.posts_tags import posts_tags


def _redirect_path(resp):
    search = re.search(r'https?://[^/]*(.*)', resp.headers['location'])
    if search:
        return search.group(1)


class AppTest(unittest.TestCase):
    def setUp(self):
        self.db = db
        self.app = app.test_client()

    def tearDown(self):
        User.query.delete()
        Page.query.delete()
        Post.query.delete()
        Image.query.delete()
        Tag.query.delete()
        Comment.query.delete()
        self.db.session.execute(posts_tags.delete())
        self.db.session.commit()

    def login_user(self, user):
        with self.app.session_transaction() as sess:
            sess['user_id'] = user.get_id()

    def assert_redirected(self, resp, path):
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(_redirect_path(resp), path)

    def assert_flashes(self, expected_message, expected_category='message'):
        with self.app.session_transaction() as session:
            try:
                category, message = session['_flashes'][0]
            except KeyError:
                raise AssertionError('nothing flashed')
            self.assertTrue(expected_message in message)
            self.assertEqual(expected_category, category)
