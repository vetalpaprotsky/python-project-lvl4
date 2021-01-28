from django.test import TestCase
from django.urls import reverse
from faker import Faker
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from .models import Task

fake = Faker()


def generate_task_form_params(status_id, executor_id):
    return {
        'name': fake.sentence(),
        'description': fake.text(),
        'status': status_id,
        'executor': executor_id,
    }


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


class TaskCreateViewTests(TestCase):
    fixtures = ['users.json', 'status.json']

    def setUp(self):
        self.author = User.objects.get(username='test_username1')
        self.executor = User.objects.get(username='test_username2')
        self.status = Status.objects.first()
        self.client.force_login(self.author)

    def test_open_task_create_form(self):
        response = self.client.get(reverse('tasks:create'))

        self.assertContains(response, "Create task")
        self.assertEqual(response.status_code, 200)

    def test_create_task_with_valid_attributes(self):
        attributes = generate_task_form_params(self.status.id, self.executor.id)

        response = self.client.post(reverse('tasks:create'), attributes)

        task = Task.objects.first()
        self.assertRedirects(response, '/tasks/')
        self.assertEqual(task.name, attributes['name'])
        self.assertEqual(task.executor, self.executor)
        self.assertEqual(task.author, self.author)
        self.assertEqual(task.status, self.status)

    def test_create_task_with_invalid_attributes(self):
        response = self.client.post(reverse('tasks:create'), {})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_when_logged_out(self):
        self.client.logout()
        attributes = generate_task_form_params(self.status.id, self.executor.id)

        response = self.client.post(reverse('tasks:create'), attributes)

        self.assertRedirects(response, '/login/?next=/tasks/create/')
        self.assertEqual(Task.objects.count(), 0)
