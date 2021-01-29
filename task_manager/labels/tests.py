from django.test import TestCase
from django.urls import reverse
# from faker import Faker
from django.contrib.auth.models import User
# from .models import Label

# fake = Faker()


# def generate_label_form_params():
#     return {'name': fake.word()}


class LabelsIndexViewTests(TestCase):
    fixtures = ['labels.json', 'user.json']

    def setUp(self):
        user = User.objects.first()
        self.client.force_login(user)

    def test_open_labels_page(self):
        response = self.client.get(reverse('labels:index'))

        self.assertContains(response, "test_label1")
        self.assertContains(response, "test_label2")
        self.assertEqual(response.status_code, 200)

    def test_open_labels_page_when_logged_out(self):
        self.client.logout()

        response = self.client.get(reverse('labels:index'))

        self.assertRedirects(response, '/login/?next=/labels/')
