from django.test import TestCase
from django.urls import reverse
from faker import Faker
from django.contrib.auth.models import User

fake = Faker()


class StatusesIndexViewTests(TestCase):
    fixtures = ['statuses.json', 'user.json']

    def setUp(self):
        user = User.objects.first()
        self.client.login(username=user.username, password='123')

    def test_open_statuses_index_page(self):
        response = self.client.get(reverse('statuses:index'))

        self.assertContains(response, "finished")
        self.assertContains(response, "in progress")
        self.assertEqual(response.status_code, 200)

    def test_open_statuses_index_page_when_logged_out(self):
        self.client.logout()

        response = self.client.get(reverse('statuses:index'))

        self.assertRedirects(response, '/login/?next=/statuses/')
