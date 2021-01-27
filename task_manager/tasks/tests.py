from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TasksIndexViewTests(TestCase):
    fixtures = ['tasks.json']

    def setUp(self):
        user = User.objects.first()
        self.client.force_login(user)

    def test_open_tasks_page(self):
        response = self.client.get(reverse('tasks:index'))

        self.assertContains(response, "test_task1")
        self.assertContains(response, "test_task2")
        self.assertEqual(response.status_code, 200)

    def test_open_tasks_page_when_logged_out(self):
        self.client.logout()

        response = self.client.get(reverse('tasks:index'))

        self.assertRedirects(response, '/login/?next=/tasks/')
