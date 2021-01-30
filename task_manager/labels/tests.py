from django.test import TestCase
from django.urls import reverse
from faker import Faker
from django.contrib.auth.models import User
from .models import Label

fake = Faker()


def generate_label_form_params():
    return {'name': fake.word()}


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


class LabelCreateViewTests(TestCase):
    fixtures = ['user.json']

    def setUp(self):
        user = User.objects.first()
        self.client.force_login(user)

    def test_open_label_create_form(self):
        response = self.client.get(reverse('labels:create'))

        self.assertContains(response, "Create label")
        self.assertEqual(response.status_code, 200)

    def test_create_label_with_valid_attributes(self):
        attributes = generate_label_form_params()

        response = self.client.post(reverse('labels:create'), attributes)

        label = Label.objects.first()
        self.assertRedirects(response, '/labels/')
        self.assertEqual(label.name, attributes['name'])

    def test_create_label_with_invalid_attributes(self):
        response = self.client.post(reverse('labels:create'), {})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), 0)

    def test_create_label_when_logged_out(self):
        self.client.logout()
        attributes = generate_label_form_params()

        response = self.client.post(reverse('labels:create'), attributes)

        self.assertRedirects(response, '/login/?next=/labels/create/')
        self.assertEqual(Label.objects.count(), 0)


class LabelUpdateViewTests(TestCase):
    fixtures = ['label.json', 'user.json']

    def setUp(self):
        self.label = Label.objects.first()
        user = User.objects.first()
        self.client.force_login(user)

    def test_open_label_update_form(self):
        url = reverse('labels:update', kwargs={'pk': self.label.pk})

        response = self.client.get(url)

        self.assertContains(response, "Label update")
        self.assertEqual(response.status_code, 200)

    def test_update_label_with_valid_attributes(self):
        url = reverse('labels:update', kwargs={'pk': self.label.pk})
        attributes = generate_label_form_params()

        response = self.client.post(url, attributes)

        self.label.refresh_from_db()
        self.assertRedirects(response, '/labels/')
        self.assertEqual(self.label.name, attributes['name'])

    def test_update_label_with_invalid_attributes(self):
        url = reverse('labels:update', kwargs={'pk': self.label.pk})
        attributes = {'name': ''}

        response = self.client.post(url, attributes)

        self.label.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(self.label.name, attributes['name'])

    def test_update_label_when_logged_out(self):
        self.client.logout()
        pk = self.label.pk
        url = reverse('labels:update', kwargs={'pk': pk})
        attributes = generate_label_form_params()

        response = self.client.post(url, attributes)

        self.label.refresh_from_db()
        self.assertRedirects(response, f'/login/?next=/labels/{pk}/update/')
        self.assertNotEqual(self.label.name, attributes['name'])
