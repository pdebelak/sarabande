import json
import os

from markupsafe import Markup


def _asset_tag_with_lookup(url_for):
    def asset_tag(filename, async='async'):
        _, extension = os.path.splitext(filename)
        if extension == '.js':
            return Markup(
                '<script src="{url}" async="{async}"></script>'.format(
                    url=url_for(filename), async=async))
        elif extension == '.css':
            return Markup(
                '<link rel="stylesheet" type="text/css" href="{url}">'.format(
                    url=url_for(filename)))
        else:
            raise RuntimeError('Unknown extension {0}'.format(extension))
    return asset_tag


def _webpack_dev_url(asset_local_host):
    def url_for(filename):
        return os.path.join(asset_local_host, filename)

    return url_for


def _manifest_url(app):
    manifest_path = app.config['ASSET_MANIFEST_PATH']
    try:
        with app.open_resource(manifest_path) as manifest_file:
            manifest = json.loads(manifest_file.read().decode('utf-8'))
    except IOError:
        raise RuntimeError(
            'Could not load manifest file {0}'.format(manifest_path))

    def url_for(filename):
        try:
            return manifest[filename]
        except KeyError:
            raise RuntimeError(
                'No manifest entry for {0}'.format(filename))

    return url_for


class Assets(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if app.config.get('DEBUG', False):
            app.config.setdefault('ASSET_LOCAL_HOST', 'http://localhost:5001')
            url_for = _webpack_dev_url(app.config['ASSET_LOCAL_HOST'])
        else:
            app.config.setdefault('ASSET_MANIFEST_PATH',
                                  'static/manifest.json')
            url_for = _manifest_url(app)
        app.add_template_global(_asset_tag_with_lookup(url_for), 'asset_tag')
