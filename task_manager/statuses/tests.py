from django.test import TestCase
from django.urls import reverse
from faker import Faker
from django.contrib.auth.models import User
from .models import Status

fake = Faker()


def generate_status_form_params():
    return {'name': fake.pystr()}


class StatusesIndexViewTests(TestCase):
    fixtures = ['statuses.json', 'user.json']

    def setUp(self):
        user = User.objects.first()
        self.client.login(username=user.username, password='123')

    def test_open_statuses_index_page(self):
        response = self.client.get(reverse('statuses:index'))

        self.assertContains(response, "test_status1")
        self.assertContains(response, "test_status2")
        self.assertEqual(response.status_code, 200)

    def test_open_statuses_index_page_when_logged_out(self):
        self.client.logout()

        response = self.client.get(reverse('statuses:index'))

        self.assertRedirects(response, '/login/?next=/statuses/')


class StatusCreateViewTests(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        user = User.objects.first()
        self.client.login(username=user.username, password='123')

    def test_open_status_create_form(self):
        response = self.client.get(reverse('statuses:create'))

        self.assertContains(response, "Create status")
        self.assertEqual(response.status_code, 200)

    def test_create_status_with_valid_attributes(self):
        attributes = generate_status_form_params()

        response = self.client.post(reverse('statuses:create'), attributes)

        status = Status.objects.first()
        self.assertRedirects(response, '/statuses/')
        self.assertEqual(status.name, attributes['name'])

    def test_create_status_with_invalid_attributes(self):
        response = self.client.post(reverse('statuses:create'), {})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), 0)

    def test_create_status_when_logged_out(self):
        self.client.logout()
        attributes = generate_status_form_params()

        response = self.client.post(reverse('statuses:create'), attributes)

        self.assertRedirects(response, '/login/?next=/statuses/create/')
        self.assertEqual(Status.objects.count(), 0)
