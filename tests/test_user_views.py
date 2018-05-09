from sarabande.models import User

from factories import build_user
from helpers import AppTest


class TestUserViews(AppTest):
    def testUserNew(self):
        resp = self.app.get('/account/new')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Create Account' in resp.data)

    def testUserCreate(self):
        resp = self.app.post(
            '/account', data={'username': 'me', 'password': 'test'})
        self.assert_redirected(resp, '/')
        user = User.query.filter(User.username == 'me').first()
        self.assertTrue(user.valid_password('test'))
        self.assertEqual(user.user_type, 'commenter')
        with self.app.session_transaction() as sess:
            self.assertTrue(sess['user_id'])

    def testUserCreateDuplicateUsername(self):
        user = build_user()
        username = user.username
        self.db.session.add(user)
        self.db.session.commit()
        resp = self.app.post(
            '/account', data={'username': username, 'password': 'test'})
        self.assertEqual(resp.status_code, 200)
        user = User.query.filter(User.username == 'me').first()
        self.assertIsNone(user)
        self.assertTrue(b'This name has been taken.' in resp.data)

    def testUserCreateNoPassword(self):
        resp = self.app.post(
            '/account', data={'username': 'me', 'password': ''})
        self.assertEqual(resp.status_code, 200)
        user = User.query.filter(User.username == 'me').first()
        self.assertIsNone(user)
        self.assertTrue(b'This field is required.' in resp.data)

    def testUserCreateWithUserType(self):
        resp = self.app.post(
            '/account',
            data={'username': 'me', 'password': 'test', 'user_type': 'user'})
        self.assertEqual(resp.status_code, 200)
        user = User.query.filter(User.username == 'me').first()
        self.assertIsNone(user)

    def testUserCreateWithUserTypeUser(self):
        user = build_user(user_type='user')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post(
            '/account',
            data={'username': 'me', 'password': 'test', 'user_type': 'user'})
        self.assertEqual(resp.status_code, 200)
        user = User.query.filter(User.username == 'me').first()
        self.assertIsNone(user)

    def testUserCreateWithUserTypeAdmin(self):
        user = build_user(user_type='admin')
        self.db.session.add(user)
        self.db.session.commit()
        user_id = user.id
        self.login_user(user)
        resp = self.app.post(
            '/account',
            data={'username': 'me', 'password': 'test', 'user_type': 'user'})
        self.assert_redirected(resp, '/')
        user = User.query.filter(User.username == 'me').first()
        self.assertTrue(user.valid_password('test'))
        self.assertEqual(user.user_type, 'user')
        with self.app.session_transaction() as sess:
            self.assertEqual(sess['user_id'], str(user_id))

    def testUserEditSelf(self):
        user = build_user(user_type='commenter')
        username = user.username
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        user = User.query.filter(User.username == username).first()
        resp = self.app.get('/account/edit')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(username.encode('utf-8') in resp.data)

    def testUserEditOther(self):
        user = build_user(user_type='commenter')
        other_user = build_user(user_type='user')
        username = user.username
        self.db.session.add(user)
        self.db.session.add(other_user)
        self.db.session.commit()
        self.login_user(other_user)
        user = User.query.filter(User.username == username).first()
        resp = self.app.get('/account/' + str(user.id) + '/edit')
        self.assertEqual(resp.status_code, 401)

    def testUserEditOtherAsAdmin(self):
        user = build_user(user_type='commenter')
        other_user = build_user(user_type='admin')
        username = user.username
        self.db.session.add(user)
        self.db.session.add(other_user)
        self.db.session.commit()
        self.login_user(other_user)
        user = User.query.filter(User.username == username).first()
        resp = self.app.get('/account/' + str(user.id) + '/edit')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(username.encode('utf-8') in resp.data)

    def testUpdateSelfUsername(self):
        user = build_user(user_type='commenter')
        username = user.username
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        user = User.query.filter(User.username == username).first()
        old_id = user.id
        old_hash = user.password_hash
        resp = self.app.post(
            '/account/' + str(user.id),
            data={'username': 'new username'})
        self.assert_redirected(resp, '/')
        updated_user = User.query.filter(
            User.username == 'new username').first()
        self.assertEqual(updated_user.id, old_id)
        self.assertEqual(updated_user.password_hash, old_hash)

    def testUpdateSelfUsernameTaken(self):
        other_user = build_user()
        other_username = other_user.username
        user = build_user(user_type='commenter')
        username = user.username
        self.db.session.add(user)
        self.db.session.add(other_user)
        self.db.session.commit()
        self.login_user(user)
        user = User.query.filter(User.username == username).first()
        resp = self.app.post(
            '/account/' + str(user.id),
            data={'username': other_username})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'This name has been taken.' in resp.data)

    def testUpdateSelfNoUsername(self):
        user = build_user(user_type='commenter')
        username = user.username
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        user = User.query.filter(User.username == username).first()
        resp = self.app.post(
            '/account/' + str(user.id),
            data={'username': ''})
        self.assertEqual(resp.status_code, 200)
        user = User.query.filter(User.username == username).first()
        self.assertIsNotNone(user)

    def testUpdateSelfPassword(self):
        user = build_user(user_type='commenter')
        username = user.username
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        user = User.query.filter(User.username == username).first()
        old_id = user.id
        resp = self.app.post(
            '/account/' + str(user.id),
            data={'username': username, 'password': 'new password'})
        self.assert_redirected(resp, '/')
        updated_user = User.query.filter(User.username == username).first()
        self.assertEqual(updated_user.id, old_id)
        self.assertTrue(updated_user.valid_password('new password'))

    def testUpdateOtherUser(self):
        user = build_user(user_type='commenter')
        other_user = build_user(user_type='user')
        username = user.username
        self.db.session.add(user)
        self.db.session.add(other_user)
        self.db.session.commit()
        self.login_user(other_user)
        user = User.query.filter(User.username == username).first()
        resp = self.app.post(
            '/account/' + str(user.id),
            data={'username': username, 'password': 'new password'})
        self.assertEqual(resp.status_code, 401)

    def testUpdateOtherUserTypeAdmin(self):
        user = build_user(user_type='commenter')
        other_user = build_user(user_type='admin')
        username = user.username
        self.db.session.add(user)
        self.db.session.add(other_user)
        self.db.session.commit()
        self.login_user(other_user)
        user = User.query.filter(User.username == username).first()
        resp = self.app.post(
            '/account/' + str(user.id),
            data={'username': username, 'user_type': 'user'})
        self.assert_redirected(resp, '/')
        updated_user = User.query.filter(User.username == username).first()
        self.assertEqual(updated_user.user_type, 'user')

    def testDeleteSelf(self):
        user = build_user(user_type='commenter')
        username = user.username
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        user = User.query.filter(User.username == username).first()
        old_id = user.id
        resp = self.app.post('/account/' + str(user.id) + '/destroy')
        self.assert_redirected(resp, '/')
        deleted_user = User.query.get(old_id)
        self.assertIsNone(deleted_user)

    def testDeleteOther(self):
        user = build_user(user_type='commenter')
        other_user = build_user(user_type='user')
        username = user.username
        self.db.session.add(user)
        self.db.session.add(other_user)
        self.db.session.commit()
        self.login_user(other_user)
        user = User.query.filter(User.username == username).first()
        resp = self.app.post('/account/' + str(user.id) + '/destroy')
        self.assertEqual(resp.status_code, 401)

    def testDeleteOtherAdmin(self):
        user = build_user(user_type='commenter')
        other_user = build_user(user_type='admin')
        username = user.username
        self.db.session.add(user)
        self.db.session.add(other_user)
        self.db.session.commit()
        self.login_user(other_user)
        user = User.query.filter(User.username == username).first()
        old_id = user.id
        resp = self.app.post('/account/' + str(user.id) + '/destroy')
        self.assert_redirected(resp, '/')
        deleted_user = User.query.get(old_id)
        self.assertIsNone(deleted_user)
