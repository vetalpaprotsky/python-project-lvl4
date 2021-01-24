from django.test import TestCase
from django.urls import reverse
from faker import Faker
from django.contrib.auth.models import User

fake = Faker()


# class UserCreateViewTests(TestCase):
#     def test_create_user_form(self):
#         response = self.client.get(reverse('users:create'))
#         self.assertContains(response, "Register")
#         self.assertEqual(response.status_code, 200)

#     def test_user_creation_with_valid_attributes(self):
#         password = fake.password()
#         attributes = {
#             'first_name': fake.first_name(),
#             'last_name': fake.last_name(),
#             'username': fake.user_name(),
#             'password1': password,
#             'password2': password,
#         }
#         response = self.client.post(reverse('users:create'), attributes)
#         self.assertEqual(response.status_code, 302)
#         user = User.objects.first()
#         self.assertEqual(user.username, attributes['username'])

#     def test_user_creation_with_invalid_attributes(self):
#         password = fake.password()
#         attributes = {
#             'last_name': fake.last_name(),
#             'username': fake.user_name(),
#             'password1': password,
#             'password2': password,
#         }
#         response = self.client.post(reverse('users:create'), attributes)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(User.objects.count(), 0)
