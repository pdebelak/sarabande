import unittest

from sarabande.models import Page


class TestPostModel(unittest.TestCase):
    def testSlugAutoSet(self):
        page = Page(title='Hello There!')
        self.assertEqual(page.slug, 'hello-there')

    def testSlugManualSet(self):
        page = Page(title='Hello There!', slug='different')
        self.assertEqual(page.slug, 'different')

    def testSlugAutoSetBlank(self):
        page = Page(title='Hello There!', slug='')
        self.assertEqual(page.slug, 'hello-there')

    def testRepr(self):
        page = Page(title='Hello There!')
        self.assertEqual(str(page), '<Page Hello There!>')
