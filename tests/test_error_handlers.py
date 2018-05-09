import unittest

from sarabande import app, unauthorized, forbidden, unhandled_error


class TestErrorHandlers(unittest.TestCase):
    def testUnauthorized(self):
        with app.test_request_context('/'):
            body, code = unauthorized()
        self.assertEqual(code, 401)
        self.assertTrue('Unauthorized' in body)

    def testForbidden(self):
        with app.test_request_context('/'):
            body, code = forbidden(None)
        self.assertEqual(code, 403)
        self.assertTrue('Unauthorized' in body)

    def testUnhandledError(self):
        with app.test_request_context('/'):
            body, code = unhandled_error(None)
        self.assertEqual(code, 500)
        self.assertTrue('Internal Server Error' in body)

    def testNotFound(self):
        resp = app.test_client().get('/blurgh')
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(b'404 Not Found' in resp.data)
