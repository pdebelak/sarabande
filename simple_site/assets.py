import json
import os

from markupsafe import Markup


class Assets(object):
    def __init__(self, app=None):
        self.app = app
        self.debug = False
        self.manifest = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if app.config.get('DEBUG', False):
            self.debug = True
            app.config.setdefault('ASSET_LOCAL_HOST', 'http://localhost:5001')
            self.asset_local_host = app.config['ASSET_LOCAL_HOST']
        else:
            app.config.setdefault('ASSET_MANIFEST_PATH',
                                  'static/manifest.json')
            self.asset_manifest_path = app.config['ASSET_MANIFEST_PATH']
            self.load_manifest(app)
        app.add_template_global(self.asset_tag)

    def asset_tag(self, filename, async='async'):
        _, extension = os.path.splitext(filename)
        if extension == '.js':
            return Markup(
                '<script src="{url}" async="{async}"></script>'.format(
                    url=self._url_for(filename), async=async))
        elif extension == '.css':
            return Markup(
                '<link rel="stylesheet" type="text/css" href="{url}">'.format(
                    url=self._url_for(filename)))
        else:
            raise RuntimeError('Unknown extension {0}'.format(extension))

    def _url_for(self, filename):
        if self.debug:
            return os.path.join(self.asset_local_host, 'static', filename)
        else:
            try:
                return os.path.join(
                    '/static', self.manifest[filename].lstrip('/'))
            except KeyError:
                raise RuntimeError(
                    'No manifest entry for {0}'.format(filename))

    def load_manifest(self, app):
        try:
            with app.open_resource(self.asset_manifest_path) as manifest_file:
                self.manifest = json.loads(
                    manifest_file.read().decode('utf-8'))
        except IOError:
            raise RuntimeError(
                'Could not load manifest file {0}'.format(
                    self.asset_manifest_path))
