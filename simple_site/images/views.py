from flask import jsonify, Response
from flask_login import current_user

from simple_site import csrf, db
from simple_site.images import images
from simple_site.models import Image
from simple_site.sessions import login_required
from .form import ImageForm


@images.route('/images', methods=['POST'])
@csrf.exempt
@login_required('user')
def create():
    form = ImageForm()
    if form.validate():
        image = form.to_image(current_user)
        db.session.add(image)
        db.session.commit()
        return jsonify({'uploaded': True, 'url': image.url})
    return jsonify({'error': form.errors['upload'][0]})


@images.route('/images/<int:id>/<name>', methods=['GET'])
def show(id, name):
    image = Image.query.filter(
        Image.id == id).filter(Image.name == name).first_or_404()
    response = Response(image.image, mimetype=image.mimetype)
    response.cache_control.max_age = 2000000
    return response
