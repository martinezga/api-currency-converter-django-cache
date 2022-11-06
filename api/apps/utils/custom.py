from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone


class CustomUtil:
    def __init__(self):
        self.response = {
            'request_detail': {
                'description': '',
                'request_date_utc': timezone.now(),
            },
            'data': {
                'message': 'An error occurred'
            },
            'status_code': 400,
        }

    @staticmethod
    def send_custom_email(**kwargs):
        subject = kwargs.get('subject')
        to_email = kwargs.get('email')
        body_type = kwargs.get('body_type')
        token = kwargs.get('token')
        password = kwargs.get('password')

        if not body_type:
            # Improvement: Create default message
            message = 'Message'
        elif body_type == 'access_email':
            message = render_to_string(
                'accounts/access_email.html',
                {
                    'email': to_email,
                    'token': token,
                    'token_expiration': settings.TOKEN_EXPIRATION,
                })
        elif body_type == 'provisional_password':
            message = render_to_string(
                'accounts/provisional_password_email.html',
                {
                    'email': to_email,
                    'password': password,
                })
        # If occur an error throw 'smtplib.SMTPException'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email, ],
            fail_silently=False,
        )
