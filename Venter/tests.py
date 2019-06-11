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

    def test_upload_valid_file_civis(self):
        self.client.login(username='admin.civis', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)

        data = open(os.path.join(MEDIA_ROOT, 'CIVIS/admin.civis/2019-05-28/input/responses_1.xlsx'), 'rb')
        file_to_upload = SimpleUploadedFile(data.name, data.read())
        valid_data = {
            "input_file": file_to_upload
        }
        response = self.client.post(reverse('upload_file'), valid_data, enctype='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './Venter/upload_file.html')

    def test_upload_invalid_file_civis(self):
        self.client.login(username='admin.civis', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)

        data = open(os.path.join(MEDIA_ROOT, 'ICMC/admin.icmc/2019-05-28/input/15_rows_icmc.csv'), 'rb')
        file_to_upload = SimpleUploadedFile(data.name, data.read())
        invalid_data = {
            "input_file": file_to_upload
        }
        response = self.client.post(reverse('upload_file'), invalid_data, enctype='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './Venter/upload_file.html')
        self.assertFormError(response, "file_form", "input_file", "File extension 'csv' is not allowed. Allowed extensions are: 'xlsx'.")

    def test_upload_no_file_civis(self):
        self.client.login(username='admin.civis', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('upload_file'), {"input_file": ''}, enctype='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './Venter/upload_file.html')
        self.assertFormError(response, "file_form", "input_file", "This field is required.")    

    def test_upload_valid_file_icmc(self):
        self.client.login(username='admin.icmc', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)

        data = open(os.path.join(MEDIA_ROOT, 'ICMC/admin.icmc/2019-05-28/input/15_rows_icmc.csv'), 'rb')
        file_to_upload = SimpleUploadedFile(data.name, data.read())
        valid_data = {
            "input_file": file_to_upload
        }
        response = self.client.post(reverse('upload_file'), valid_data, enctype='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './Venter/upload_file.html')

    def test_upload_non_csv_file_icmc(self):
        self.client.login(username='admin.icmc', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)

        data = open(os.path.join(MEDIA_ROOT, 'CIVIS/admin.civis/2019-05-28/input/responses_1.xlsx'), 'rb')
        file_to_upload = SimpleUploadedFile(data.name, data.read())
        invalid_data = {
            "input_file": file_to_upload
        }
        response = self.client.post(reverse('upload_file'), invalid_data, enctype='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './Venter/upload_file.html')
        self.assertFormError(response, "file_form", "input_file", "Please upload .csv extension files only")

    def test_upload_no_file_icmc(self):
        self.client.login(username='admin.icmc', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('upload_file'), {"input_file": ''}, enctype='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './Venter/upload_file.html')
        self.assertFormError(response, "file_form", "input_file", "This field is required.")

    def test_upload_blank_file_icmc(self):
        self.client.login(username='admin.icmc', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)

        data = open(os.path.join(MEDIA_ROOT, 'Coverage Test/blank_icmc.csv'), 'rb')
        file_to_upload = SimpleUploadedFile(data.name, data.read())
        invalid_data = {
            "input_file": file_to_upload
        }
        response = self.client.post(reverse('upload_file'), invalid_data, enctype='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './Venter/upload_file.html')
        self.assertFormError(response, "file_form", "input_file", "Incorrect headers detected, please upload correct file")

    def test_upload_incorrect_headers_file_icmc(self):
        self.client.login(username='admin.icmc', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)

        data = open(os.path.join(MEDIA_ROOT, 'Coverage Test/incorrect_headers_icmc.csv'), 'rb')
        file_to_upload = SimpleUploadedFile(data.name, data.read())
        invalid_data = {
            "input_file": file_to_upload
        }
        response = self.client.post(reverse('upload_file'), invalid_data, enctype='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './Venter/upload_file.html')
        self.assertFormError(response, "file_form", "input_file", "Incorrect headers detected, please upload correct file")

    def test_upload_max_file_icmc(self):
        self.client.login(username='admin.icmc', password="pass@1234")
        response = self.client.get(reverse('upload_file'))
        self.assertEqual(response.status_code, 200)

        data = open(os.path.join(MEDIA_ROOT, 'Coverage Test/5.3kb_icmc.csv'), 'rb')
        file_to_upload = SimpleUploadedFile(data.name, data.read())
        invalid_data = {
            "input_file": file_to_upload
        }
        response = self.client.post(reverse('upload_file'), invalid_data, enctype='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './Venter/upload_file.html')
        self.assertFormError(response, "file_form", "input_file", "File size must not exceed 5 MB")  


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class PredictionModelTestCase(TestCase):
    """
        Test case for user to upload csv/xlsx file
    """
    fixtures = ["Venter/fixtures/fixture_new_1.json"]

    def setUp(self):
        self.client = Client()
        self.client.login(username='admin.icmc', password="pass@1234")

    def file_not_predicted(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        file = open(os.path.join(MEDIA_ROOT, 'CIVIS/admin.civis/2019-06-07/input/responses_2.xlsx'), 'r', encoding='utf-8')
        uploaded_file = SimpleUploadedFile(file.name, file.read())
        filemeta = File.objects.get(input_file=uploaded_file)
        print("================filemeta")
        print(filemeta)
