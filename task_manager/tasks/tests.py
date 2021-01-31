from urllib.parse import urlencode
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from .models import Task

fake = Faker()


def generate_task_form_params(status, executor, labels):
    return {
        'name': fake.sentence(),
        'description': fake.text(),
        'status': status.pk,
        'executor': executor.pk,
        'labels': [label.pk for label in labels],
    }


def create_status():
    status = Status(name=fake.word())
    status.save()
    return status


def create_user():
    user = User(username=fake.user_name())
    user.save()
    return user


def create_labels(count):
    labels = []
    for _ in range(count):
        label = Label(name=fake.word())
        label.save()
        labels.append(label)
    return labels


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


class TasksFilterTests(TestCase):
    fixtures = ['tasks_filtering.json']

    def setUp(self):
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.task3 = Task.objects.get(pk=3)
        user = User.objects.first()
        self.client.force_login(user)

    def test_filter_by_status(self):
        url = reverse('tasks:index')
        query_str = urlencode({'status': self.task1.status.pk})

        response = self.client.get(f'{url}?{query_str}')

        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)
        self.assertEqual(response.status_code, 200)

    def test_filter_by_executor(self):
        url = reverse('tasks:index')
        query_str = urlencode({'executor': self.task1.executor.pk})

        response = self.client.get(f'{url}?{query_str}')

        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)
        self.assertEqual(response.status_code, 200)

    def test_filter_by_label(self):
        url = reverse('tasks:index')
        query_str = urlencode({'label': self.task1.labels.first().pk})

        response = self.client.get(f'{url}?{query_str}')

        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)
        self.assertEqual(response.status_code, 200)

    def test_filter_by_self_tasks(self):
        url = reverse('tasks:index')
        query_str = urlencode({'self_tasks': 'on'})

        response = self.client.get(f'{url}?{query_str}')

        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)
        self.assertEqual(response.status_code, 200)

    def test_filter_by_status_executor_and_label(self):
        url = reverse('tasks:index')
        query_str = urlencode({
            'status': self.task2.status.pk,
            'executor': self.task2.executor.pk,
            'label': self.task2.labels.first().pk,
        })

        response = self.client.get(f'{url}?{query_str}')

        self.assertNotContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)
        self.assertEqual(response.status_code, 200)


class TasksDetailViewTests(TestCase):
    fixtures = ['task.json']

    def setUp(self):
        self.task = Task.objects.first()
        user = User.objects.first()
        self.client.force_login(user)

    def test_open_task_detail_page(self):
        url = reverse('tasks:detail', kwargs={'pk': self.task.pk})

        response = self.client.get(url)

        self.assertContains(response, "test_task")
        self.assertEqual(response.status_code, 200)

    def test_open_task_detail_page_when_logged_out(self):
        self.client.logout()
        pk = self.task.pk
        url = reverse('tasks:detail', kwargs={'pk': pk})

        response = self.client.get(url)

        self.assertRedirects(response, f'/login/?next=/tasks/{pk}/')


class TaskCreateViewTests(TestCase):
    fixtures = ['user.json']

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
        labels = create_labels(2)
        attributes = generate_task_form_params(status, executor, labels)

        response = self.client.post(reverse('tasks:create'), attributes)

        task = Task.objects.first()
        self.assertRedirects(response, '/tasks/')
        self.assertEqual(task.name, attributes['name'])
        self.assertEqual(task.author, self.author)
        self.assertEqual(task.executor, executor)
        self.assertEqual(task.status, status)
        self.assertEqual(list(task.labels.all()), list(labels))

    def test_create_task_with_invalid_attributes(self):
        response = self.client.post(reverse('tasks:create'), {})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_when_logged_out(self):
        self.client.logout()
        status = create_status()
        executor = create_user()
        labels = create_labels(2)
        attributes = generate_task_form_params(status, executor, labels)

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
        labels = create_labels(2)
        attributes = generate_task_form_params(status, executor, labels)

        response = self.client.post(url, attributes)

        self.task.refresh_from_db()
        self.assertRedirects(response, '/tasks/')
        self.assertEqual(self.task.name, attributes['name'])
        self.assertEqual(self.task.author, self.author)
        self.assertEqual(self.task.executor, executor)
        self.assertEqual(self.task.status, status)
        self.assertEqual(list(self.task.labels.all()), list(labels))

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
        status = create_status()
        executor = create_user()
        labels = create_labels(2)
        attributes = generate_task_form_params(status, executor, labels)

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
