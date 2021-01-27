from django.test import TestCase
from django.urls import reverse
from faker import Faker
from django.contrib.auth.models import User
from .models import Status

fake = Faker()


def generate_status_form_params():
    return {'name': fake.pystr(min_chars=10, max_chars=20)}


class StatusesIndexViewTests(TestCase):
    fixtures = ['statuses.json', 'user.json']

    def setUp(self):
        user = User.objects.first()
        self.client.force_login(user)

    def test_open_statuses_page(self):
        response = self.client.get(reverse('statuses:index'))

        self.assertContains(response, "test_status1")
        self.assertContains(response, "test_status2")
        self.assertEqual(response.status_code, 200)

    def test_open_statuses_page_when_logged_out(self):
        self.client.logout()

        response = self.client.get(reverse('statuses:index'))

        self.assertRedirects(response, '/login/?next=/statuses/')


class StatusCreateViewTests(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        user = User.objects.first()
        self.client.force_login(user)

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


class StatusUpdateViewTests(TestCase):
    fixtures = ['status.json', 'user.json']

    def setUp(self):
        self.status = Status.objects.first()
        user = User.objects.first()
        self.client.force_login(user)

    def test_open_status_update_form(self):
        url = reverse('statuses:update', kwargs={'pk': self.status.pk})

        response = self.client.get(url)

        self.assertContains(response, "Status update")
        self.assertEqual(response.status_code, 200)

    def test_update_status_with_valid_attributes(self):
        url = reverse('statuses:update', kwargs={'pk': self.status.pk})
        attributes = generate_status_form_params()

        response = self.client.post(url, attributes)

        self.status.refresh_from_db()
        self.assertRedirects(response, '/statuses/')
        self.assertEqual(self.status.name, attributes['name'])

    def test_update_status_with_invalid_attributes(self):
        url = reverse('statuses:update', kwargs={'pk': self.status.pk})
        attributes = {'name': ''}

        response = self.client.post(url, attributes)

        self.status.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(self.status.name, attributes['name'])

    def test_update_status_when_logged_out(self):
        self.client.logout()
        pk = self.status.pk
        url = reverse('statuses:update', kwargs={'pk': pk})
        attributes = generate_status_form_params()

        response = self.client.post(url, attributes)

        self.status.refresh_from_db()
        self.assertRedirects(response, f'/login/?next=/statuses/{pk}/update/')
        self.assertNotEqual(self.status.name, attributes['name'])


class StatusDeleteViewTests(TestCase):
    fixtures = ['status.json', 'user.json']

    def setUp(self):
        self.status = Status.objects.first()
        user = User.objects.first()
        self.client.force_login(user)

    def test_open_status_delete_form(self):
        url = reverse('statuses:delete', kwargs={'pk': self.status.pk})

        response = self.client.get(url)

        self.assertContains(response, "Status deletion")
        self.assertEqual(response.status_code, 200)

    def test_delete_status(self):
        url = reverse('statuses:delete', kwargs={'pk': self.status.pk})

        response = self.client.post(url)

        self.assertRedirects(response, '/statuses/')
        self.assertEqual(Status.objects.count(), 0)

    def test_delete_status_when_logged_out(self):
        self.client.logout()
        pk = self.status.pk
        url = reverse('statuses:delete', kwargs={'pk': pk})

        response = self.client.post(url)

        self.assertRedirects(response, f'/login/?next=/statuses/{pk}/delete/')
        self.assertEqual(Status.objects.count(), 1)
