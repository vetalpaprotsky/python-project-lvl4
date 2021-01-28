from django.test import TestCase
from django.urls import reverse
from faker import Faker
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from .models import Task

fake = Faker()


def generate_task_form_params(status=None, executor=None):
    params = {
        'name': fake.sentence(),
        'description': fake.text(),
    }
    if status:
        params.update(status=status.pk)
    if executor:
        params.update(executor=executor.pk)
    return params


def create_status():
    status = Status(name=fake.word())
    status.save()
    return status


def create_user():
    user = User(username=fake.user_name())
    user.save()
    return user


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
    fixtures = ['user.json', 'status.json']

    def setUp(self):
        self.author = User.objects.first()
        self.client.force_login(self.author)

    def test_open_task_create_form(self):
        response = self.client.get(reverse('tasks:create'))

        self.assertContains(response, "Create task")
        self.assertEqual(response.status_code, 200)

    def test_create_task_with_valid_attributes(self):
        status = create_status()
        executor = create_user()
        attributes = generate_task_form_params(status, executor)

        response = self.client.post(reverse('tasks:create'), attributes)

        task = Task.objects.first()
        self.assertRedirects(response, '/tasks/')
        self.assertEqual(task.name, attributes['name'])
        self.assertEqual(task.author, self.author)
        self.assertEqual(task.executor, executor)
        self.assertEqual(task.status, status)

    def test_create_task_with_invalid_attributes(self):
        response = self.client.post(reverse('tasks:create'), {})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_when_logged_out(self):
        self.client.logout()
        status = create_status()
        executor = create_user()
        attributes = generate_task_form_params(status, executor)

        response = self.client.post(reverse('tasks:create'), attributes)

        self.assertRedirects(response, '/login/?next=/tasks/create/')
        self.assertEqual(Task.objects.count(), 0)


class TaskUpdateViewTests(TestCase):
    fixtures = ['task.json']

    def setUp(self):
        self.task = Task.objects.first()
        self.author = User.objects.first()
        self.client.force_login(self.author)

    def test_open_task_update_form(self):
        url = reverse('tasks:update', kwargs={'pk': self.task.pk})

        response = self.client.get(url)

        self.assertContains(response, "Task update")
        self.assertEqual(response.status_code, 200)

    def test_update_task_with_valid_attributes(self):
        url = reverse('tasks:update', kwargs={'pk': self.task.pk})
        status = create_status()
        executor = create_user()
        attributes = generate_task_form_params(status, executor)

        response = self.client.post(url, attributes)

        self.task.refresh_from_db()
        self.assertRedirects(response, '/tasks/')
        self.assertEqual(self.task.name, attributes['name'])
        self.assertEqual(self.task.author, self.author)
        self.assertEqual(self.task.executor, executor)
        self.assertEqual(self.task.status, status)

    def test_update_task_with_invalid_attributes(self):
        url = reverse('tasks:update', kwargs={'pk': self.task.pk})
        attributes = {'name': ''}

        response = self.client.post(url, attributes)

        self.task.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(self.task.name, attributes['name'])

    def test_update_task_when_logged_out(self):
        self.client.logout()
        pk = self.task.pk
        url = reverse('tasks:update', kwargs={'pk': pk})
        attributes = generate_task_form_params()

        response = self.client.post(url, attributes)

        self.task.refresh_from_db()
        self.assertRedirects(response, f'/login/?next=/tasks/{pk}/update/')
        self.assertNotEqual(self.task.name, attributes['name'])


class TaskDeleteViewTests(TestCase):
    fixtures = ['task.json']

    def setUp(self):
        self.task = Task.objects.first()
        user = User.objects.first()
        self.client.force_login(user)

    def test_open_task_delete_form(self):
        url = reverse('tasks:delete', kwargs={'pk': self.task.pk})

        response = self.client.get(url)

        self.assertContains(response, "Task deletion")
        self.assertEqual(response.status_code, 200)

    def test_delete_task(self):
        url = reverse('tasks:delete', kwargs={'pk': self.task.pk})

        response = self.client.post(url)

        self.assertRedirects(response, '/tasks/')
        self.assertEqual(Task.objects.count(), 0)

    def test_delete_task_of_other_author(self):
        other_task = Task(
            name=fake.sentence(),
            author=create_user(),
            status=Status.objects.first(),
        )
        other_task.save()
        url = reverse('tasks:delete', kwargs={'pk': other_task.pk})

        response = self.client.post(url)

        self.assertRedirects(response, '/tasks/')
        self.assertEqual(Task.objects.count(), 2)

    def test_delete_task_when_logged_out(self):
        self.client.logout()
        pk = self.task.pk
        url = reverse('tasks:delete', kwargs={'pk': pk})

        response = self.client.post(url)

        self.assertRedirects(response, f'/login/?next=/tasks/{pk}/delete/')
        self.assertEqual(Task.objects.count(), 1)
