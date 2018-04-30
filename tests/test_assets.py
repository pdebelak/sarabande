import unittest
from flask import Flask

from simple_site.assets import Assets


class TestAssets(unittest.TestCase):
    def setUp(self):
        self.app = Flask('test_app')

    def test_asset_tag_when_debug(self):
        self.assertIsNone(self.app.jinja_env.globals.get('asset_tag'))
        self.app.config['DEBUG'] = True
        Assets(self.app)
        asset_tag = self.app.jinja_env.globals['asset_tag']
        self.assertEqual(
            asset_tag('app.css'),
            '<link rel="stylesheet" type="text/css" href="http://localhost:5001/app.css">')
        self.assertEqual(
            asset_tag('app.js'),
            '<script src="http://localhost:5001/app.js" async="async"></script>')
        self.assertEqual(
            asset_tag('nested/index.js', async=False),
            '<script src="http://localhost:5001/nested/index.js" async="False"></script>')
        with self.assertRaises(
                RuntimeError, msg='Unknown extension .png'):
            asset_tag('image.png')

    def test_asset_tag_not_debug(self):
        manifest_path = 'tests/resources/manifest.json'
        self.app.config['ASSET_MANIFEST_PATH'] = manifest_path
        Assets(self.app)
        asset_tag = self.app.jinja_env.globals['asset_tag']
        self.assertEqual(
            asset_tag('app.css'),
            '<link rel="stylesheet" type="text/css" href="/static/app.somehash.css">')
        self.assertEqual(
            asset_tag('app.js'),
            '<script src="/static/app.somehash.js" async="async"></script>')
        with self.assertRaises(
                RuntimeError, msg='No manifest entry for nested/index.js'):
            asset_tag('nested/index.js')

    def test_assets_no_manifest_file(self):
        manifest_path = 'tests/resources/badmanifest.json'
        self.app.config['ASSET_MANIFEST_PATH'] = manifest_path
        with self.assertRaises(
                RuntimeError,
                msg='Could not load manifest file tests/resources/badmanifest.json'):
            Assets(self.app)
