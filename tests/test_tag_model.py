import unittest

from sarabande.models import Tag


class TestTagModel(unittest.TestCase):
    def testSlugAutoSet(self):
        tag = Tag(name='Stuff')
        self.assertEqual(tag.slug, 'stuff')

    def testSlugManualSet(self):
        tag = Tag(name='Stuff', slug='other')
        self.assertEqual(tag.slug, 'other')

    def testSlugAutoSetBlank(self):
        tag = Tag(name='Stuff', slug='')
        self.assertEqual(tag.slug, 'stuff')

    def testRepr(self):
        tag = Tag(name='Stuff')
        self.assertEqual(str(tag), '<Tag Stuff>')
