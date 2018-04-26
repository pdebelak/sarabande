import unittest

from simple_site.models import Post


class TestPostModel(unittest.TestCase):
    def testSlugAutoSet(self):
        post = Post(title='Hello There!')
        self.assertEqual(post.slug, 'hello-there')

    def testSlugManualSet(self):
        post = Post(title='Hello There!', slug='different')
        self.assertEqual(post.slug, 'different')

    def testSlugAutoSetBlank(self):
        post = Post(title='Hello There!', slug='')
        self.assertEqual(post.slug, 'hello-there')
