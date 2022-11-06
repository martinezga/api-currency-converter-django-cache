import smtplib

from django.contrib.auth import get_user_model
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
        custom_util = CustomUtil()
        response = custom_util.response
        description = 'Send access token to email informed. Previous registration not required'
        response['request_detail']['description'] = description
        email = request.data.get('email')

        if not email:
            response['data']['error'] = 'Email not sent'
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
                    # Improvement: Implement logging to app's admin
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

        return Response(response, status=response['status_code'])
