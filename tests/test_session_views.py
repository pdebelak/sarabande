from factories import build_user
from helpers import AppTest


class TestSessionViews(AppTest):
    def testNewSessionNotLoggedIn(self):
        resp = self.app.get('/sessions/new')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Login' in resp.data)

    def testNewSessionLoggedIn(self):
        user = build_user()
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/sessions/new')
        self.assertEqual(resp.status_code, 302)

    def testLoginValidData(self):
        password = 'testpassword'
        user = build_user(password=password)
        self.db.session.add(user)
        self.db.session.commit()
        resp = self.app.post(
            '/sessions',
            data={'username': user.username, 'password': password})
        self.assert_redirected(resp, '/')
        self.assert_flashes('You are logged in!')
        with self.app.session_transaction() as sess:
            self.assertEqual(sess['user_id'], str(user.id))

    def testLoginBadUsername(self):
        resp = self.app.post(
            '/sessions',
            data={'username': 'something', 'password': 'password'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Unknown username' in resp.data)

    def testLoginBadPassword(self):
        password = 'testpassword'
        user = build_user(password=password)
        self.db.session.add(user)
        self.db.session.commit()
        resp = self.app.post(
            '/sessions',
            data={'username': user.username, 'password': password + '1'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Invalid password' in resp.data)

    def testLogout(self):
        user = build_user()
        self.db.session.add(user)
        self.db.session.commit()
        with self.app.session_transaction() as sess:
            sess['user_id'] = user.get_id()
        resp = self.app.post('/sessions/destroy')
        self.assert_redirected(resp, '/')
        self.assert_flashes('You are logged out!')
        with self.app.session_transaction() as sess:
            self.assertEqual(sess.get('user_id'), None)
