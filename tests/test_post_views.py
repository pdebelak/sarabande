import unittest

from simple_site import app, db
from simple_site.models import Post, User

from factories import build_post


class TestPostViews(unittest.TestCase):
    def setUp(self):
        db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        Post.query.delete()
        User.query.delete()
        db.session.commit()

    def testPostIndex(self):
        post1 = build_post()
        post2 = build_post()
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()
        resp = self.app.get('/posts')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(post1.title.encode('utf-8') in resp.data)
        self.assertTrue(post2.title.encode('utf-8') in resp.data)
        self.assertTrue(b'/posts/' + post1.slug.encode('utf-8') in resp.data)
        self.assertTrue(b'/posts/' + post2.slug.encode('utf-8') in resp.data)

    def testPostShowNotFound(self):
        resp = self.app.get('/posts/not-found')
        self.assertEqual(resp.status_code, 404)

    def testPostShowFound(self):
        post = build_post()
        db.session.add(post)
        db.session.commit()
        resp = self.app.get('/posts/' + post.slug)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(post.title.encode('utf-8') in resp.data)
        self.assertTrue(post.body.encode('utf-8') in resp.data)
        self.assertTrue(post.user.username.encode('utf-8') in resp.data)

    def testPostShowFoundHTMLBody(self):
        post = build_post(body='<p>Some html</p><p>In here</p>')
        db.session.add(post)
        db.session.commit()
        resp = self.app.get('/posts/' + post.slug)
        self.assertTrue(post.body.encode('utf-8') in resp.data)
