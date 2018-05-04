from sarabande.models import Post, Tag

from factories import build_post, build_user
from helpers import AppTest


class TestPostViews(AppTest):
    def testPostIndex(self):
        post1 = build_post()
        post2 = build_post()
        self.db.session.add(post1)
        self.db.session.add(post2)
        self.db.session.commit()
        resp = self.app.get('/posts')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(post1.title.encode('utf-8') in resp.data)
        self.assertTrue(post2.title.encode('utf-8') in resp.data)
        self.assertTrue(b'/posts/' + post1.slug.encode('utf-8') in resp.data)
        self.assertTrue(b'/posts/' + post2.slug.encode('utf-8') in resp.data)

    def testPostShowNotFound(self):
        resp = self.app.get('/posts/not-found')
        self.assertEqual(resp.status_code, 404)

    def testPostShowFound(self):
        post = build_post()
        self.db.session.add(post)
        self.db.session.commit()
        resp = self.app.get('/posts/' + post.slug)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(post.title.encode('utf-8') in resp.data)
        self.assertTrue(post.body.encode('utf-8') in resp.data)
        self.assertTrue(post.user.username.encode('utf-8') in resp.data)

    def testPostShowFoundHTMLBody(self):
        post = build_post(body='<p>Some html</p><p>In here</p>')
        self.db.session.add(post)
        self.db.session.commit()
        resp = self.app.get('/posts/' + post.slug)
        self.assertTrue(post.body.encode('utf-8') in resp.data)

    def testPostNewNotLoggedIn(self):
        resp = self.app.get('/posts/new')
        self.assertEqual(resp.status_code, 401)

    def testPostNewLoggedInCommenter(self):
        user = build_user(user_type='commenter')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/posts/new')
        self.assertEqual(resp.status_code, 401)

    def testPostNewLoggedInUser(self):
        user = build_user(user_type='user')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/posts/new')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Create Post' in resp.data)

    def testPostNewLoggedInAdmin(self):
        user = build_user(user_type='admin')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/posts/new')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Create Post' in resp.data)

    def testPostCreateAsCommenter(self):
        user = build_user(user_type='commenter')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post('/posts',
                             data={'title': 'My post', 'body': 'Posting it'})
        self.assertEqual(resp.status_code, 401)

    def testPostCreateAsUser(self):
        user = build_user(user_type='user')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post('/posts',
                             data={'title': 'My post', 'body': 'Posting it'})
        self.assert_redirected(resp, '/posts/my-post')
        post = Post.query.filter(Post.slug == 'my-post').first()
        self.assertEqual(post.title, 'My post')
        self.assertEqual(post.body, 'Posting it')
        self.assertEqual(post.user_id, user.id)

    def testPostCreateDuplicateSlug(self):
        user = build_user(user_type='user')
        post = build_post()
        slug = post.slug
        self.db.session.add(user)
        self.db.session.add(post)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post(
            '/posts',
            data={'title': 'My post', 'body': 'Posting it', 'slug': slug})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'This slug is taken.' in resp.data)

    def testPostCreateMissingData(self):
        user = build_user(user_type='user')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post('/posts',
                             data={'title': 'My post', 'body': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'This field is required' in resp.data)
        post = Post.query.filter(Post.slug == 'my-post').first()
        self.assertIsNone(post)

    def testPostCreateWithNewTags(self):
        user = build_user(user_type='user')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post(
            '/posts',
            data={'title': 'My post', 'body': 'Posting it',
                  'tag_names': 'Great, Post'})
        self.assert_redirected(resp, '/posts/my-post')
        post = Post.query.filter(Post.slug == 'my-post').first()
        tags = Tag.query.filter(Tag.slug.in_(['great', 'post'])).all()
        self.assertEqual(len(tags), 2)
        for tag in tags:
            self.assertEqual(tag.posts[0].id, post.id)

    def testPostCreateMixOfNewAndExistingTags(self):
        user = build_user(user_type='user')
        existing_tag = Tag(name='My Tag!!!')
        self.db.session.add(user)
        self.db.session.add(existing_tag)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post(
            '/posts',
            data={'title': 'My post', 'body': 'Posting it',
                  'tag_names': 'My tag, New tag'})
        self.assert_redirected(resp, '/posts/my-post')
        post = Post.query.filter(Post.slug == 'my-post').first()
        tags = Tag.query.all()
        self.assertEqual(len(tags), 2)
        for tag in tags:
            self.assertEqual(tag.posts[0].id, post.id)

    def testPostEditAsCommenter(self):
        user = build_user(user_type='commenter')
        post = build_post()
        slug = post.slug
        self.db.session.add(user)
        self.db.session.add(post)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/posts/' + slug + '/edit')
        self.assertEqual(resp.status_code, 401)

    def testPostEditAsAdmin(self):
        user = build_user(user_type='admin')
        post = build_post()
        slug = post.slug
        self.db.session.add(user)
        self.db.session.add(post)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/posts/' + slug + '/edit')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(slug.encode('utf-8') in resp.data)

    def testPostEditAsUserNotAuthor(self):
        user = build_user(user_type='user')
        post = build_post()
        slug = post.slug
        self.db.session.add(user)
        self.db.session.add(post)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/posts/' + slug + '/edit')
        self.assertEqual(resp.status_code, 401)

    def testPostEditAsAuthor(self):
        user = build_user(user_type='user')
        post = build_post(user=user)
        slug = post.slug
        self.db.session.add(post)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/posts/' + slug + '/edit')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(slug.encode('utf-8') in resp.data)

    def testPostEditWithTags(self):
        user = build_user(user_type='user')
        tags = [Tag(name='First tag'), Tag(name='Second tag')]
        post = build_post(user=user, tags=tags)
        slug = post.slug
        self.db.session.add(post)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/posts/' + slug + '/edit')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'First tag' in resp.data)
        self.assertTrue(b'Second tag' in resp.data)

    def testPostUpdate(self):
        user = build_user(user_type='user')
        post = build_post(user=user)
        slug = post.slug
        self.db.session.add(user)
        self.db.session.add(post)
        self.db.session.commit()
        self.login_user(user)
        post = Post.query.filter(Post.slug == slug).first()
        resp = self.app.post(
            '/posts/' + slug,
            data={'title': 'New title', 'body': post.body, 'slug': post.slug})
        self.assert_redirected(resp, '/posts/' + post.slug)
        new_post = Post.query.filter(Post.slug == slug).first()
        self.assertEqual(new_post.title, 'New title')
        self.assertEqual(new_post.slug, post.slug)
        self.assertEqual(new_post.body, post.body)

    def testPostUpdateDuplicateSlug(self):
        user = build_user(user_type='user')
        post = build_post(user=user)
        other_post = build_post()
        slug = post.slug
        other_slug = other_post.slug
        self.db.session.add(user)
        self.db.session.add(post)
        self.db.session.add(other_post)
        self.db.session.commit()
        self.login_user(user)
        post = Post.query.filter(Post.slug == slug).first()
        resp = self.app.post(
            '/posts/' + slug,
            data={'title': 'New title', 'body': post.body, 'slug': other_slug})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'This slug is taken.' in resp.data)

    def testPostUpdateMissingData(self):
        user = build_user(user_type='user')
        post = build_post(user=user)
        slug = post.slug
        old_title = post.title
        self.db.session.add(user)
        self.db.session.add(post)
        self.db.session.commit()
        self.login_user(user)
        post = Post.query.filter(Post.slug == slug).first()
        resp = self.app.post(
            '/posts/' + slug,
            data={'title': '', 'body': post.body, 'slug': post.slug})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'This field is required' in resp.data)
        post = Post.query.filter(Post.slug == slug).first()
        self.assertEqual(post.title, old_title)

    def testPostUpdateWrongUser(self):
        user = build_user(user_type='user')
        post = build_post()
        slug = post.slug
        self.db.session.add(user)
        self.db.session.add(post)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post(
            '/posts/' + slug,
            data={'title': 'New title', 'body': 'New body', 'slug': 'new'})
        self.assertEqual(resp.status_code, 401)

    def testPostUpdateWithTags(self):
        user = build_user(user_type='user')
        tags = [Tag(name='First tag'), Tag(name='Second tag')]
        post = build_post(user=user, tags=tags)
        slug = post.slug
        self.db.session.add(user)
        self.db.session.add(post)
        self.db.session.commit()
        self.login_user(user)
        post = Post.query.filter(Post.slug == slug).first()
        resp = self.app.post(
            '/posts/' + slug,
            data={
                'title': 'New title',
                'body': post.body,
                'slug': post.slug,
                'tag_names': 'Second tag, New tag'})
        self.assert_redirected(resp, '/posts/' + post.slug)
        new_post = Post.query.filter(Post.slug == slug).first()
        self.assertEqual(len(new_post.tags), 2)
        self.assertEqual(new_post.tag_names, 'Second tag, New tag')

    def testPostDelete(self):
        user = build_user(user_type='user')
        post = build_post(user=user)
        slug = post.slug
        self.db.session.add(user)
        self.db.session.add(post)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post('/posts/' + slug + '/destroy')
        self.assert_redirected(resp, '/admin')
        self.assert_flashes('Post deleted', 'success')
        post = Post.query.filter(Post.slug == slug).first()
        self.assertIsNone(post)

    def testPostDeleteWrongUser(self):
        user = build_user(user_type='user')
        post = build_post()
        slug = post.slug
        self.db.session.add(user)
        self.db.session.add(post)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post('/posts/' + slug + '/destroy')
        self.assertEqual(resp.status_code, 401)
