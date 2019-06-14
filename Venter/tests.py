import os
import json
import ast

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase, override_settings
from django.test.client import Client
from django.urls import reverse

from Venter.forms import ContactForm, CSVForm, ExcelForm, ProfileForm, UserForm
from Venter.models import Category, File, Header, Organisation, Profile
from Backend.settings import MEDIA_ROOT
from Venter.wordcloud import generate_wordcloud


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

        data = open(os.path.join(MEDIA_ROOT, 'Coverage Test/responses_1.xlsx'), 'rb')
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

        data = open(os.path.join(MEDIA_ROOT, 'Coverage Test/15_rows_icmc.csv'), 'rb')
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

        data = open(os.path.join(MEDIA_ROOT, 'Coverage Test/15_rows_icmc.csv'), 'rb')
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

        data = open(os.path.join(MEDIA_ROOT, 'Coverage Test/responses_1.xlsx'), 'rb')
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
class WordCloudTestCase(TestCase):
    """
        Test case for users to view wordcloud for a set of responses per category
    """
    fixtures = ["Venter/fixtures/fixture_new_1.json"]

    def setUp(self):
        self.client = Client()

    def test_icmc_wordcloud(self):
        self.client.login(username="admin.icmc", password="pass@1234")

        pk = 207
        file = File.objects.get(pk=pk)
        
        org_name = Organisation.objects.get(organisation_name="ICMC")
        category_queryset = Category.objects.filter(organisation_name=org_name)
        category_list = []
        for element in category_queryset:
            cat = element.category
            category_list.append(cat)

        response = self.client.get(reverse('wordcloud', kwargs={"pk": file.pk}))
        
        self.assertEqual(response.context['category_list'], category_list)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './Venter/wordcloud.html')

    def test_civis_wordcloud(self):
        self.client.login(username="admin.civis", password="pass@1234")

        pk = 212
        file = File.objects.get(pk=pk)

        domain_name = "Heritage Conservation"
        wordcloud_category_list = []

        dict_data = json.load(file.output_file_json)
        print("=====================dict_data in test case: ", type(dict_data) )
        print(dict_data)
        domain_data = dict_data[domain_name]
        print("=====================domain_data in test case: ", type(domain_data))
        print(domain_data)
        for category, category_dict in domain_data.items():
            wordcloud_category_list.append(category)
        wordcloud_category_list = wordcloud_category_list[:-1]

        print("===============wordcloud category list=====")
        print(type(wordcloud_category_list))
        print(wordcloud_category_list)
        
        data = {
            "wordcloud_domain_name": domain_name
        }

        response = self.client.post(reverse('wordcloud', kwargs={"pk": file.pk}), data)
        
        self.assertEqual(response.context['category_list'], wordcloud_category_list)
        self.assertEqual(response.context['domain_name'], domain_name)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './Venter/wordcloud.html')

    def test_civis_wordcloud_content(self):
        self.client.login(username="admin.civis", password="pass@1234")

        pk = 212
        file = File.objects.get(pk=pk)

        domain_name = "Heritage Conservation"
        category_name = "set the boundaries of these heritage zones and said that these areas should be conserved, protected and highlighted by provision of transport facilities and tourist infrastructure"
        temp_cat_list = json.dumps("{'set the boundaries of these heritage zones and said that these areas should be conserved, protected and highlighted by provision of transport facilities and tourist infrastructure', 'The 12 heritage zones identified are: Central Administrative Heritage Zone, Petta and Bangalore Fort, Gavipuram, Basavanagudi and VV Puram, M.G.Road, Shivajinagar, Cleveland Town, Richards Town, Malleshwaram, Ulsoor, Whitefield Inner Circle, Begur Temple and Bangalore Palace Heritage Zone'}")
        data = {
            "category_name": category_name,
            "domain_name": domain_name,
            "category_list": temp_cat_list
        }
        response = self.client.post(reverse('wordcloud_contents', kwargs={"pk": file.pk}), data)
        output_dict = generate_wordcloud(file.output_file_json.path)
        domain_items_list = output_dict[domain_name]
        words = {}

        for domain_item in domain_items_list:
            if list(domain_item.keys())[0].split('\n')[0].strip() == category_name.strip():
                words = list(domain_item.values())[0]

        category_list = json.loads(temp_cat_list)
        self.assertEqual(response.context['category_list'], category_list)
        self.assertEqual(response.context['domain_name'], domain_name)
        self.assertEqual(response.context['words'], words)
        self.assertEqual(response.context['category_name'], category_name)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './Venter/wordcloud.html')


