from sarabande import app


@app.template_filter('publish_time')
def publish_time(pt, format='short'):
    if not pt:
        return 'DRAFT'
    if format == 'short':
        return pt.strftime('%b %-d, %Y')
    if format == 'long':
        return pt.strftime('%Y-%m-%d %H:%M')
    raise RuntimeError('Unknown format {0}'.format(format))


@app.template_filter('comment_time')
def comment_time(ct):
    return ct.strftime('%b %-d, %Y %H:%M')
