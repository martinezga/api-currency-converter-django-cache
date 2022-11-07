import smtplib

from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from oauth2_provider.models import AccessToken
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.utils.custom import CustomUtil

UserModel = get_user_model()


class AuthView(ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def access(self, request):
        """
        Input: {"email": "my_email@email.com"}
        """
        custom_util = CustomUtil()
        response = custom_util.response
        description = 'Send access token to email informed. Previous registration not required'
        response['request_detail']['description'] = description
        email = request.data.get('email')

        if not email:
            response['data']['error'] = 'Email address is required'
        else:
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                # Create user. No need to be registered
                user = UserModel.objects.create_user(email)
            finally:
                # If exist update password to use OAuth workflow
                password = UserModel.objects.make_random_password()
                user.update_password(password)
                # Get tokens
                tokens = UserModel.get_tokens(email, password)
                # get access token and send it by email
                try:
                    custom_util.send_custom_email(
                        subject='Welcome! Here is your access code 🚀',
                        body_type='access_email',
                        email=email,
                        token=tokens.get('access_token'),
                    )
                    response['data']['message'] = 'Email sent'
                    response['status_code'] = 200
                except smtplib.SMTPException:
                    # Improvement: Implement logging to admins
                    response['data']['error'] = "Didn't send the email. Try again"
                    response['status_code'] = 404

        return Response(response, status=response['status_code'])

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Input: {"email": "my_email@email.com", "access_token": "37rgytpjVsjJ"}
        """
        response = CustomUtil().response
        description = 'Log in with access token previously sent by email'
        response['request_detail']['description'] = description
        email = request.data.get('email')
        access_token = request.data.get('access_token')

        if not email or not access_token:
            response['data']['error'] = 'Email and token are required'
        else:
            # Verify received token, revoke and create new one
            try:
                user = UserModel.objects.get(email=email)
                datetime_now = timezone.now()
                AccessToken.objects.get(
                    user_id=user.id,
                    token=access_token,
                    expires__gt=datetime_now,
                )
                # Discard all tokens requested by user before this successfully log in
                tokens_all = AccessToken.objects.filter(user_id=user.id)
                for one_item in tokens_all:
                    UserModel.revoke_tokens(one_item.token)
                # Get new tokens
                password = UserModel.objects.make_random_password()
                user.update_password(password)
                tokens = UserModel.get_tokens(email, password)
                # Update last login
                update_last_login(None, user)
                response['data']['message'] = 'Access granted'
                response['data']['tokens'] = tokens
                response['status_code'] = 200
            except UserModel.DoesNotExist:
                response['data']['error'] = 'Not authorized'
                response['status_code'] = 401
            except AccessToken.DoesNotExist:
                response['data']['error'] = 'Not authorized'
                response['status_code'] = 401

        return Response(response, status=response['status_code'])

    @action(detail=False, methods=['post'], url_path='password/provisional')
    def provisional_password(self, request):
        """
        Send provisional password to an admin.
        Password is required to access django admin and modify OAuth settings
        Input: {"email": "my_email@email.com"}
        """
        custom_util = CustomUtil()
        response = custom_util.response
        description = 'Send provisional password to email informed.'
        response['request_detail']['description'] = description
        email = request.data.get('email')
        user = None

        if not email:
            response['data']['error'] = 'Email address is required'
        else:
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                response['data']['error'] = 'Not authorized'
                response['status_code'] = 401
            # Verify user exist and is admin
            if user and user.is_superuser:
                password = UserModel.objects.make_random_password()
                user.update_password(password)
                # Send provisional password by email
                try:
                    custom_util.send_custom_email(
                        subject='Provisional password',
                        body_type='provisional_password',
                        password=password,
                        email=email,
                    )
                    response['data']['message'] = 'Email sent'
                    response['status_code'] = 200
                except smtplib.SMTPException:
                    # Improvement: Implement logging to admins
                    response['data']['error'] = "Didn't send the email. Try again"
                    response['status_code'] = 404
            else:
                response['data']['error'] = 'Not authorized'
                response['status_code'] = 401

        return Response(response, status=response['status_code'])
