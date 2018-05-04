import unittest

from sarabande.models import Post


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

    def testRepr(self):
        post = Post(title='Hello There!')
        self.assertEqual(str(post), '<Post Hello There!>')

    def testSummary(self):
        post = Post(body='<p>First paragraph!</p><p>Second!</p>')
        self.assertEqual(post.summary, '<p>First paragraph!</p>')

    def testSummaryNoPTag(self):
        post = Post(body='Just some garbage in here.')
        self.assertEqual(post.summary, post.body)
