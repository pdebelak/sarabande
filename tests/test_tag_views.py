from sarabande.models import Tag

from factories import build_post
from helpers import AppTest


class TestTagViews(AppTest):
    def testTagShow(self):
        tag1 = Tag(name='First tag')
        tag2 = Tag(name='Second tag')
        post1 = build_post(tags=[tag1, tag2])
        post2 = build_post(tags=[tag1])
        post3 = build_post(tags=[tag2])
        post4 = build_post(published_at=None, tags=[tag1, tag2])
        post1_title = post1.title
        post2_title = post2.title
        post3_title = post3.title
        post4_title = post4.title
        self.db.session.add(post1)
        self.db.session.add(post2)
        self.db.session.add(post3)
        self.db.session.add(post4)
        self.db.session.commit()
        resp = self.app.get('/tags/first-tag')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(post1_title.encode('utf-8') in resp.data)
        self.assertTrue(post2_title.encode('utf-8') in resp.data)
        self.assertFalse(post3_title.encode('utf-8') in resp.data)
        self.assertFalse(post4_title.encode('utf-8') in resp.data)
        resp = self.app.get('/tags/second-tag')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(post1_title.encode('utf-8') in resp.data)
        self.assertFalse(post2_title.encode('utf-8') in resp.data)
        self.assertTrue(post3_title.encode('utf-8') in resp.data)
        self.assertFalse(post4_title.encode('utf-8') in resp.data)
