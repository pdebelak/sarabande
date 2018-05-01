from sarabande.models import Page

from factories import build_page, build_user
from helpers import AppTest


class TestPageViews(AppTest):
    def testPageShowNotFound(self):
        resp = self.app.get('/not-found')
        self.assertEqual(resp.status_code, 404)

    def testPageShowFound(self):
        page = build_page()
        self.db.session.add(page)
        self.db.session.commit()
        resp = self.app.get('/' + page.slug)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(page.title.encode('utf-8') in resp.data)
        self.assertTrue(page.body.encode('utf-8') in resp.data)

    def testPageShowFoundHTMLBody(self):
        page = build_page(body='<p>Some html</p><p>In here</p>')
        self.db.session.add(page)
        self.db.session.commit()
        resp = self.app.get('/' + page.slug)
        self.assertTrue(page.body.encode('utf-8') in resp.data)

    def testPageNewNotLoggedIn(self):
        resp = self.app.get('/pages/new')
        self.assertEqual(resp.status_code, 401)

    def testPageNewLoggedInCommenter(self):
        user = build_user(user_type='commenter')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/pages/new')
        self.assertEqual(resp.status_code, 401)

    def testPageNewLoggedInUser(self):
        user = build_user(user_type='user')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/pages/new')
        self.assertEqual(resp.status_code, 401)

    def testPageNewLoggedInAdmin(self):
        user = build_user(user_type='admin')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/pages/new')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'Create Page' in resp.data)

    def testPageCreateAsUser(self):
        user = build_user(user_type='user')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post('/pages',
                             data={'title': 'About', 'body': 'About'})
        self.assertEqual(resp.status_code, 401)

    def testPageCreateAsAdmin(self):
        user = build_user(user_type='admin')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post('/pages',
                             data={'title': 'About', 'body': 'About the page'})
        self.assert_redirected(resp, '/about')
        page = Page.query.filter(Page.slug == 'about').first()
        self.assertEqual(page.title, 'About')
        self.assertEqual(page.body, 'About the page')

    def testPageCreateDuplicateSlug(self):
        user = build_user(user_type='admin')
        page = build_page(slug='about')
        self.db.session.add(user)
        self.db.session.add(page)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post('/pages',
                             data={'title': 'About', 'body': 'About the page'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'This slug is taken.' in resp.data)

    def testPageCreateAsAdminMissingData(self):
        user = build_user(user_type='admin')
        self.db.session.add(user)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post('/pages',
                             data={'title': 'About', 'body': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'This field is required' in resp.data)
        page = Page.query.filter(Page.slug == 'about').first()
        self.assertIsNone(page)

    def testPageEditAsUser(self):
        user = build_user(user_type='user')
        page = build_page()
        slug = page.slug
        self.db.session.add(user)
        self.db.session.add(page)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/pages/' + slug + '/edit')
        self.assertEqual(resp.status_code, 401)

    def testPageEditAsAdmin(self):
        user = build_user(user_type='admin')
        page = build_page()
        slug = page.slug
        self.db.session.add(user)
        self.db.session.add(page)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.get('/pages/' + slug + '/edit')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(slug.encode('utf-8') in resp.data)

    def testPageUpdate(self):
        user = build_user(user_type='admin')
        page = build_page()
        slug = page.slug
        self.db.session.add(user)
        self.db.session.add(page)
        self.db.session.commit()
        self.login_user(user)
        page = Page.query.filter(Page.slug == slug).first()
        resp = self.app.post(
            '/pages/' + slug,
            data={'title': 'New title', 'body': page.body, 'slug': page.slug})
        self.assert_redirected(resp, '/' + slug)
        new_page = Page.query.filter(page.slug == slug).first()
        self.assertEqual(new_page.title, 'New title')
        self.assertEqual(new_page.slug, page.slug)
        self.assertEqual(new_page.body, page.body)

    def testPageUpdateDuplicateSlug(self):
        user = build_user(user_type='admin')
        page = build_page()
        other_page = build_page()
        slug = page.slug
        other_slug = other_page.slug
        self.db.session.add(user)
        self.db.session.add(page)
        self.db.session.add(other_page)
        self.db.session.commit()
        self.login_user(user)
        page = Page.query.filter(Page.slug == slug).first()
        resp = self.app.post(
            '/pages/' + slug,
            data={'title': 'New title', 'body': page.body, 'slug': other_slug})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'This slug is taken.' in resp.data)

    def testPageUpdateMissingData(self):
        user = build_user(user_type='admin')
        page = build_page()
        slug = page.slug
        old_title = page.title
        self.db.session.add(user)
        self.db.session.add(page)
        self.db.session.commit()
        self.login_user(user)
        page = Page.query.filter(Page.slug == slug).first()
        resp = self.app.post(
            '/pages/' + slug,
            data={'title': '', 'body': page.body, 'slug': page.slug})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(b'This field is required' in resp.data)
        page = Page.query.filter(Page.slug == slug).first()
        self.assertEqual(page.title, old_title)

    def testPageUpdateNotAdmin(self):
        user = build_user(user_type='user')
        page = build_page()
        slug = page.slug
        self.db.session.add(user)
        self.db.session.add(page)
        self.db.session.commit()
        self.login_user(user)
        page = Page.query.filter(Page.slug == slug).first()
        resp = self.app.post(
            '/pages/' + slug,
            data={'title': 'New title', 'body': page.body, 'slug': page.slug})
        self.assertEqual(resp.status_code, 401)

    def testPageDelete(self):
        user = build_user(user_type='admin')
        page = build_page()
        slug = page.slug
        self.db.session.add(user)
        self.db.session.add(page)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post('/pages/' + slug + '/destroy')
        self.assert_redirected(resp, '/admin/pages')
        self.assert_flashes('Page deleted', 'success')
        page = Page.query.filter(Page.slug == slug).first()
        self.assertIsNone(page)

    def testPageDeleteNotAdmin(self):
        user = build_user(user_type='user')
        page = build_page()
        slug = page.slug
        self.db.session.add(user)
        self.db.session.add(page)
        self.db.session.commit()
        self.login_user(user)
        resp = self.app.post('/pages/' + slug + '/destroy')
        self.assertEqual(resp.status_code, 401)
