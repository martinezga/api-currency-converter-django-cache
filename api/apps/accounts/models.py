import requests
from decouple import config
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.accounts.manager import UserManager


class User(AbstractUser):
    """
    Email, username and password are required. Other fields are optional.
    """
    email = models.EmailField(
        max_length=120, verbose_name='Email', unique=True)

    objects = UserManager()

    # Allow log in by email and password in Django admin
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

    def update_password(self, password):
        self.set_password(password)
        self.save()

    @staticmethod
    def split_email(email):
        email_name, domain_part = email.strip().rsplit('@', 1)
        return email_name, domain_part

    @staticmethod
    def get_tokens(email, password):
        # AUTH_URL must be included on ALLOWED_HOSTS
        r = requests.post(
            f'{config("AUTH_URL")}/o/token/',
            data={
                'grant_type': 'password',
                'username': email,
                'password': password,
                'client_id': config('CLIENT_ID'),
                'client_secret': config('CLIENT_SECRET'),
            },
        )

        return r.json()

    @staticmethod
    def revoke_tokens(access_token):
        """
        Method to revoke tokens.
        {"token": "<token>"}
        """
        _ = requests.post(
            f'{config("AUTH_URL")}/o/revoke_token/',
            data={
                'token': access_token,
                'client_id': config('CLIENT_ID'),
                'client_secret': config('CLIENT_SECRET'),
            },
        )
