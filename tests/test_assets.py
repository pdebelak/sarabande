import unittest
from flask import Flask

from sarabande.assets import Assets


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
            '<link rel="stylesheet" type="text/css" href="http://localhost:5001/app.css" data-turbolinks-track="reload">')
        self.assertEqual(
            asset_tag('app.js'),
            '<script src="http://localhost:5001/app.js" defer data-turbolinks-track="reload"></script>')
        self.assertEqual(
            asset_tag('nested/index.js'),
            '<script src="http://localhost:5001/nested/index.js" defer data-turbolinks-track="reload"></script>')
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
            '<link rel="stylesheet" type="text/css" href="/static/app.somehash.css" data-turbolinks-track="reload">')
        self.assertEqual(
            asset_tag('app.js'),
            '<script src="/static/app.somehash.js" defer data-turbolinks-track="reload"></script>')
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

    def test_theme_asset(self):
        manifest_path = 'tests/resources/manifest.json'
        self.app.config['THEME'] = 'dark'
        self.app.config['ASSET_MANIFEST_PATH'] = manifest_path
        Assets(self.app)
        theme_asset = self.app.jinja_env.globals['theme_asset']
        self.assertEqual(
            theme_asset('css'),
            '<link rel="stylesheet" type="text/css" href="/static/dark.somehash.css" data-turbolinks-track="reload">')
        self.assertEqual(
            theme_asset('js'),
            '<script src="/static/dark.somehash.js" defer data-turbolinks-track="reload"></script>')

    def test_theme_not_specified(self):
        manifest_path = 'tests/resources/manifest.json'
        self.app.config['ASSET_MANIFEST_PATH'] = manifest_path
        Assets(self.app)
        theme_asset = self.app.jinja_env.globals['theme_asset']
        self.assertEqual(
            theme_asset('css'),
            '<link rel="stylesheet" type="text/css" href="/static/light.somehash.css" data-turbolinks-track="reload">')
        self.assertEqual(
            theme_asset('js'),
            '<script src="/static/light.somehash.js" defer data-turbolinks-track="reload"></script>')
