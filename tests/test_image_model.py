import unittest

from sarabande.models import Image


class TestImageModel(unittest.TestCase):
    def testUrl(self):
        image = Image(name='Hello there.png', id=2)
        self.assertEqual(image.url, '/images/2/Hello%20there.png')

    def testRepr(self):
        image = Image(name='test.png')
        self.assertEqual(str(image), '<Image test.png>')
