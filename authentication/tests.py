from django.test import TestCase, Client

# Create your tests here.

class mainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('/auth/')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('/auth/')
        self.assertTemplateUsed(response, 'login.html')