from flask import render_template
from werkzeug.exceptions import NotFound

from sarabande import app


def _home_page_data(app):
    home_path = app.config['HOME_PAGE']
    url = app.url_map.bind('sarabande', path_info=home_path)
    try:
        endpoint, defaults = url.match()
        view_func = app.view_functions[endpoint]

        @app.route('/', defaults=defaults, methods=['GET'])
        def home_page(**kwargs):
            return view_func(**kwargs)

        return home_page
    except (KeyError, NotFound):
        raise RuntimeError('Unknown home page path {0}'.format(home_path))


home_page = _home_page_data(app)


@app.route('/source-license')
def license():
    return render_template('license.html')
