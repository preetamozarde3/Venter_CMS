import os

from django.contrib.auth.models import Permission, User
from django.test import TestCase, override_settings
from django.test.client import Client
from django.urls import reverse

from Venter.models import Category, File, Header, Organisation, Profile


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class LoginTestCase(TestCase):
    """
            Test case for user to log in
    """
    fixtures = ["Venter/fixtures/fixture_new_1.json"]

    def setUp(self):
        self.client = Client()

    def test_login(self):
        response = self.client.get('/venter/login/')
        self.assertEqual(response.status_code, 200)
        self.client.login(username='admin.civis', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)
