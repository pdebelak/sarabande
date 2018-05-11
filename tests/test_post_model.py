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

    def testDescription(self):
        post = Post(body='<p>First paragraph!</p><p>Second!</p>')
        self.assertEqual(post.description, 'First paragraph!')

    def testImageURL(self):
        post = Post(body='<p>First paragraph!</p><p><img src="/images/wat"></p>')
        self.assertEqual(post.image_url, '/images/wat')

    def testImageURLNoImage(self):
        post = Post(body='<p>First paragraph!</p><p>Second!</p>')
        self.assertIsNone(post.image_url)

    def testHTMLBodyWithRawHTMLMarker(self):
        post = Post(body='<p>First paragraph!</p><p>===</p>&lt;iframe src="wat"&gt;&lt;/iframe&gt;<p>===</p><p>Second!</p>')
        self.assertEqual(
            post.html_body,
            '<p>First paragraph!</p><iframe src="wat"></iframe><p>Second!</p>')

    def testHTMLBodyWithTwoRawHTMLMarkers(self):
        post = Post(body='<p>First paragraph!</p><p> ===</p>&lt;iframe src="wat"&gt;&lt;/iframe&gt;<p>===\t</p><p>Second!</p><p>===</p>&lt;strong&gt;test&lt;/strong&gt;<p>===</p><p>Third!</p>')
        self.assertEqual(
            post.html_body,
            '<p>First paragraph!</p><iframe src="wat"></iframe><p>Second!</p><strong>test</strong><p>Third!</p>')
