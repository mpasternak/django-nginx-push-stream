from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse


class TestAuthViewAnon(TestCase):
    def setUp(self):
        self.client = Client()

    def test_anon_allowed_to_all(self):
        """Anon wants to access 'all' queue"""

        headers = {"HTTP_X_ORIGINAL_URI": "/ws/my-app__all__"}
        res = self.client.post(reverse("auth"), **headers)
        self.assertEquals(res.status_code, 200)

    def test_anon_disallowed_to_auth(self):
        """Anon wants to access 'auth' queue"""
        headers = {"HTTP_X_ORIGINAL_URI": "/ws/my-app__all__/my-app__authorized__"}
        res = self.client.post(reverse("auth"), **headers)
        self.assertEquals(res.status_code, 403)


class TestAuthViewFuzzy(TestCase):
    def setUp(self):
        self.client = Client()

    def test_anon_allowed_to_unknown_name(self):
        """Anon wants to access 'wutlolski' queue"""
        headers = {"HTTP_X_ORIGINAL_URI": "/ws/my-app__wutlolski__"}
        res = self.client.post(reverse("auth"), **headers)
        self.assertEquals(res.status_code, 403)

    def test_anon_allowed_to_unknown_name(self):
        """Anon wants to access 'all' queue with slash"""
        headers = {"HTTP_X_ORIGINAL_URI": "/ws/my-app__all__////"}
        res = self.client.post(reverse("auth"), **headers)
        self.assertEquals(res.status_code, 200)


class TestAuthViewAuthorised(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_user(username='jacob', email='jacob@…', password='top_secret')

    def test_authorised_allowed_to_all(self):
        """Authorised wants to access 'all' queue"""
        headers = {"HTTP_X_ORIGINAL_URI": "/ws/my-app__all__"}
        self.client.force_login(self.user)
        res = self.client.post(reverse("auth"), **headers)
        self.assertEquals(res.status_code, 200)

    def test_authorised_allowed_to_auth(self):
        """Authorised user wants to access 'auth' queue"""
        headers = {"HTTP_X_ORIGINAL_URI": "/ws/my-app__all__/my-app__authorized__"}
        self.client.force_login(self.user)
        res = self.client.post(reverse("auth"), **headers)
        self.assertEquals(res.status_code, 200)

    def test_authorised_allowed_for_ones_session(self):
        """Authorised wants to access own session"""
        self.client.login(username='jacob', password='top_secret')
        cookie = self.client.cookies['sessionid'].value
        session = self.client.session
        session['session_key'] = cookie
        session.save()
        headers = {"HTTP_X_ORIGINAL_URI": "/ws/my-app__all__/my-app__session__%s" % cookie}
        res = self.client.post(reverse("auth"), **headers)
        self.assertEquals(res.status_code, 200)

    def test_authorised_disallowed_for_other_sessions(self):
        """Authorised wants to access foreing session"""
        cookie = "unknown session cookie"
        headers = {"HTTP_X_ORIGINAL_URI": "/ws/my-app__all__/my-app__session__%s" % cookie}
        self.client.force_login(self.user)
        session = self.client.session
        session['session_key'] = "some other session"
        session.save()
        res = self.client.post(reverse("auth"), **headers)
        self.assertEquals(res.status_code, 403)
