from flask import Flask

from helpers import AppTest

from sarabande.views import _home_page_data


class TestBaseViews(AppTest):
    def testLicense(self):
        resp = self.app.get('/source-license')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Sarabande is free software' in resp.data)

    def testHomePageData(self):
        app = Flask('test_app')

        @app.route('/hello/<name>')
        def hello_name(name):
            return 'Hello, {0}!'.format(name)

        app.config['HOME_PAGE'] = '/hello/World'
        _home_page_data(app)

        resp = app.test_client().get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(b'Hello, World!', resp.data)

    def testHomePageDataUnknownPath(self):
        app = Flask('test_app')
        app.config['HOME_PAGE'] = '/hello/World'
        with self.assertRaises(RuntimeError,
                               msg='Unknown home page path /hello/World'):
            _home_page_data(app)
