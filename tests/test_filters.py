from datetime import datetime
import unittest

from sarabande.filters import publish_time


class TestFilters(unittest.TestCase):
    def testPublishTimeUnpublished(self):
        self.assertEqual(publish_time(None), 'DRAFT')

    def testPublishTimeShort(self):
        dt = datetime(2018, 3, 2, 1, 1, 1)
        self.assertEqual(publish_time(dt, 'short'), 'Mar 2, 2018')

    def testPublishTimeLong(self):
        dt = datetime(2018, 3, 2, 1, 2, 3)
        self.assertEqual(publish_time(dt, 'long'), '2018-03-02 01:02')

    def testPublishTimeUnknown(self):
        dt = datetime(2018, 3, 2, 1, 2, 3)
        with self.assertRaises(RuntimeError, msg='Unknown format very_long'):
            publish_time(dt, 'very_long')
