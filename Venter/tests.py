import os

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase, override_settings
from django.test.client import Client
from django.urls import reverse

from Venter.forms import ContactForm, CSVForm, ExcelForm, ProfileForm, UserForm
from Venter.models import Category, File, Header, Organisation, Profile
from Backend.settings import MEDIA_ROOT


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class LoginTestCase(TestCase):
    """
            Test case for user to log in with valid and invalid credentials
    """
    fixtures = ["Venter/fixtures/fixture_new_1.json"]

    def setUp(self):
        self.client = Client()

    def test_login_admin_civis(self):
        response = self.client.get('/venter/login/')
        self.assertEqual(response.status_code, 200)
        self.client.login(username='admin.civis', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)

    def test_login_admin_icmc(self):
        response = self.client.get('/venter/login/')
        self.assertEqual(response.status_code, 200)
        self.client.login(username='admin.icmc', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)

    def test_login_employee_civis(self):
        response = self.client.get('/venter/login/')
        self.assertEqual(response.status_code, 200)
        self.client.login(username='user1.civis', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)

    def test_login_employee_icmc(self):
        response = self.client.get('/venter/login/')
        self.assertEqual(response.status_code, 200)
        self.client.login(username='user1.icmc', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_credentials(self):
        response = self.client.get('/venter/login/')
        self.assertEqual(response.status_code, 200)
        form = AuthenticationForm(data={'username': 'admin.civis', 'password': 'wrong'})
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class LogoutTestCase(TestCase):
    """
            Test case for user to log out
    """
    fixtures = ["Venter/fixtures/fixture_new_1.json"]

    def setUp(self):
        self.client = Client()

    def test_logout_admin_civis(self):
        self.client.login(username='admin.civis', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_admin_icmc(self):
        self.client.login(username='admin.icmc', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_employee_civis(self):
        self.client.login(username='user1.civis', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_employee_icmc(self):
        self.client.login(username='user1.icmc', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)    

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class UploadFileTestCase(TestCase):
    """
        Test case for user to upload csv/xlsx file
    """
    fixtures = ["Venter/fixtures/fixture_new_1.json"]

    def setUp(self):
        self.client = Client()

    # def test_upload_invalid_file_civis(self):
    #     self.client.login(username='admin.civis', password="pass@1234")
    #     response = self.client.get(reverse('upload_file'))
    #     self.assertEqual(response.status_code, 200)
    #     invalid_data = {
    #         "input_file": "ICMC/admin.icmc/2019-05-28/input/15_rows_icmc.csv"
    #     }
    #     factory = RequestFactory()
    #     request = factory.post('upload_file', invalid_data, enctype='multipart/form-data')
    #     form = ExcelForm(data=invalid_data, request=request)
    #     self.assertFalse(form.is_valid())
    #     self.assertTrue(form.errors)

    # def test_upload_invalid_file_icmc(self):
    #     self.client.login(username='admin.icmc', password="pass@1234")
    #     response = self.client.get(reverse('upload_file'))
    #     self.assertEqual(response.status_code, 200)
    #     invalid_data = {
    #         "input_file": "CIVIS/admin.civis/2019-05-28/input/responses_1.xlsx"
    #     }
    #     factory = RequestFactory()
    #     request = factory.post('upload_file', invalid_data, enctype='multipart/form-data')
    #     form = CSVForm(data=invalid_data, request=request)
    #     self.assertFalse(form.is_valid())
    #     self.assertTrue(form.errors)

    # def test_upload_valid_file_civis(self):
    #     self.client.login(username='admin.civis', password="pass@1234")
    #     response = self.client.get(reverse('upload_file'))
    #     self.assertEqual(response.status_code, 200)
    #     data = open(os.path.join(MEDIA_ROOT, 'CIVIS/admin.civis/2019-05-28/input/responses_1.xlsx'), 'rb')
    #     file_to_upload = SimpleUploadedFile('responses_1.xlsx', open(os.path.join(MEDIA_ROOT, 'CIVIS/admin.civis/2019-05-28/input/responses_1.xlsx'), 'r'), content_type="xlsx")
    #     valid_data = {
    #         "input_file": file_to_upload
    #     }
    #     factory = RequestFactory()

    #     request = factory.post('upload_file', valid_data, enctype='multipart/form-data')
    #     form = ExcelForm(data=valid_data, request=request)
    #     self.assertTrue(form.is_valid())
    #     self.assertFalse(form.errors)

    def test_upload_invalid_file_civis(self):
        self.client.login(username='admin.civis', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)
        data = open(os.path.join(MEDIA_ROOT, 'ICMC/admin.icmc/2019-05-28/input/15_rows_icmc.csv'), 'rb')
        file_to_upload = SimpleUploadedFile(content=data.read(), name=data.name, content_type='multipart/form-data')
        invalid_data = {
            "input_file": file_to_upload
        }
        factory = RequestFactory()

        request = factory.post('upload_file', invalid_data, enctype='multipart/form-data')
        form = ExcelForm(data=invalid_data, request=request)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    # def test_upload_valid_file_civis(self):
    #     self.client.login(username='admin.civis', password="pass@1234")
    #     response = self.client.get(reverse('upload_file'))
    #     self.assertEqual(response.status_code, 200)
    #     data = open(os.path.join(MEDIA_ROOT, 'CIVIS/admin.civis/2019-05-28/input/responses_1.xlsx'), 'rb')
    #     file_to_upload = SimpleUploadedFile(content = data.read(), name = data.name, content_type='multipart/form-data')
    #     valid_data = {
    #         "input_file": file_to_upload
    #     }
    #     factory = RequestFactory()

    #     request = factory.post('upload_file', valid_data, enctype='multipart/form-data')
    #     form = ExcelForm(data=valid_data, request=request)
    #     self.assertTrue(form.is_valid())
    #     self.assertFalse(form.errors)

    # def test_upload_valid_file_civis(self):
    #     self.client.login(username='admin.civis', password="pass@1234")
    #     response = self.client.get(reverse('upload_file'))
    #     self.assertEqual(response.status_code, 200)
    #     data = open(os.path.join(MEDIA_ROOT, 'CIVIS/admin.civis/2019-05-28/input/responses_1.xlsx'), 'rb')
    #     file_to_upload = SimpleUploadedFile(content = data.read(), name = data.name, content_type='multipart/form-data')
    #     valid_data = {
    #         "input_file": file_to_upload
    #     }
    #     factory = RequestFactory()

    #     request = factory.post('upload_file', valid_data, enctype='multipart/form-data')
    #     form = ExcelForm(data=valid_data, request=request)
    #     self.assertTrue(form.is_valid())
    #     self.assertFalse(form.errors)