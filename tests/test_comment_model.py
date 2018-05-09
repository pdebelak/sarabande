import unittest

from sarabande.models import Comment


class TestCommentModel(unittest.TestCase):
    def testRepr(self):
        comment = Comment(body='First!')
        self.assertEqual(str(comment), '<Comment First!>')

    def testReprLong(self):
        comment = Comment(body='A very long body with a lot of content in it!')
        self.assertEqual(str(comment), '<Comment A very long body wit>')
