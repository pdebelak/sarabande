from flask import request


def safe_return_to():
    return_to = request.args.get('return_to')
    if return_to and return_to.startswith('/'):
        return return_to
    return '/'
