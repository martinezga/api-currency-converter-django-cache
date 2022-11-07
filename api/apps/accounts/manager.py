from django.apps import apps
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email):
        UserModel = apps.get_model('accounts.User')
        password = self.make_random_password()
        username, domain_part = UserModel.split_email(email)
        if domain_part in settings.ADMIN_DOMAIN:
            user = self.create_superuser(email, username, password)
        else:
            user = self.model(
                email=self.normalize_email(email),
                username=f'{username}#{password}',
            )
            user.set_password(password)
            user.save()

        return user

    def create_superuser(self, email, username, password):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_superuser=True,
            is_staff=True
        )
        user.set_password(password)
        user.save()
        return user
