from io import BytesIO
import json

from sarabande.models import Image, User

from factories import build_image, build_user
from helpers import AppTest


class TestImageViews(AppTest):
    def testImageShowNotFound(self):
        resp = self.app.get('images/1/not-found')
        self.assertEqual(resp.status_code, 404)

    def testImageShowFound(self):
        image = build_image()
        self.db.session.add(image)
        self.db.session.commit()
        resp = self.app.get(image.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(image.image, resp.data)
        self.assertEqual(resp.headers['cache-control'], 'max-age=2000000')
        self.assertEqual(resp.headers['content-type'], image.mimetype)

    def testImageShowFoundSpaceInName(self):
        image = build_image(name='I have space.png', image=b'space town')
        self.db.session.add(image)
        self.db.session.commit()
        resp = self.app.get(image.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(image.image, resp.data)

    def testImageCreateCommenter(self):
        user = build_user(user_type='commenter')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post(
            '/images', data={'upload': (BytesIO(b'image'), 'image.png')})
        self.assertEqual(resp.status_code, 401)

    def testImageCreateUser(self):
        user = build_user(user_type='user')
        with open('tests/resources/sample_image.jpeg', 'rb') as img:
            image_bytes = BytesIO(img.read())
            username = user.username
            self.db.session.add(user)
            self.db.session.commit()
            user = User.query.filter(User.username == username).first()
            self.login_user(user)
            resp = self.app.post(
                '/images',
                data={'upload': (image_bytes, 'image.jpeg')})
            self.assertEqual(resp.status_code, 200)
            image = Image.query.filter(Image.name == 'image.jpeg').first()
            self.assertEqual(image.mimetype, 'image/jpeg')
            self.assertEqual(image.user_id, user.id)
            body = json.loads(resp.data.decode('utf-8'))
            self.assertEqual(body['url'], image.url)
            self.assertTrue(body['uploaded'])

    def testImageCreateNoUpload(self):
        user = build_user(user_type='user')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post('/images', data={})
        self.assertEqual(resp.status_code, 200)
        body = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(body['error'], 'This field is required.')
