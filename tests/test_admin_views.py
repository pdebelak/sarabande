from factories import build_page, build_user, build_post, build_comment
from helpers import AppTest


class TestAdminViews(AppTest):
    def testPostsCommenter(self):
        user = build_user(user_type='commenter')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/admin')
        self.assertEqual(resp.status_code, 401)

    def testPostsUser(self):
        user = build_user(user_type='user')
        post = build_post(user=user)
        other_post = build_post()
        post_title = post.title
        other_post_title = other_post.title
        self.db.session.add(user)
        self.db.session.add(post)
        self.db.session.add(other_post)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/admin')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(post_title.encode('utf-8') in resp.data)
        self.assertFalse(other_post_title.encode('utf-8') in resp.data)

    def testPostsAdmin(self):
        user = build_user(user_type='admin')
        post = build_post(user=user)
        other_post = build_post()
        post_title = post.title
        other_post_title = other_post.title
        self.db.session.add(user)
        self.db.session.add(post)
        self.db.session.add(other_post)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/admin')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(post_title.encode('utf-8') in resp.data)
        self.assertTrue(other_post_title.encode('utf-8') in resp.data)

    def testPagesUser(self):
        user = build_user(user_type='user')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/admin/pages')
        self.assertEqual(resp.status_code, 401)

    def testPagesAdmin(self):
        user = build_user(user_type='admin')
        page = build_page()
        page_title = page.title
        self.db.session.add(user)
        self.db.session.add(page)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/admin/pages')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(page_title.encode('utf-8') in resp.data)

    def testUsersUser(self):
        user = build_user(user_type='user')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/admin/users')
        self.assertEqual(resp.status_code, 401)

    def testUsersAdmin(self):
        user = build_user(user_type='admin')
        other_user = build_user(user_type='user')
        username = user.username
        other_username = other_user.username
        self.db.session.add(user)
        self.db.session.add(other_user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/admin/users')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(username.encode('utf-8') in resp.data)
        self.assertTrue(other_username.encode('utf-8') in resp.data)

    def testCommentsCommenter(self):
        user = build_user(user_type='commenter')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/admin/comments')
        self.assertEqual(resp.status_code, 401)

    def testCommentsUser(self):
        user = build_user(user_type='user')
        comment = build_comment()
        other_comment = build_comment()
        comment_body = comment.html_body
        comment_author = comment.author_name
        other_comment_body = other_comment.html_body
        other_comment_author = other_comment.author_name
        self.db.session.add(user)
        self.db.session.add(comment)
        self.db.session.add(other_comment)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/admin/comments')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(comment_body.encode('utf-8') in resp.data)
        self.assertTrue(comment_author.encode('utf-8') in resp.data)
        self.assertTrue(other_comment_body.encode('utf-8') in resp.data)
        self.assertTrue(other_comment_author.encode('utf-8') in resp.data)
