from django.contrib.auth.models import User


def get_full_name(self):
    if self.first_name and self.last_name:
        return self.get_full_name()
    return self.username


User.add_to_class("__str__", get_full_name)
