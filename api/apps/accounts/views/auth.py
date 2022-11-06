from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.utils.custom import CustomUtil

User = get_user_model()


class AuthView(ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def access(self, request):
        response = CustomUtil().response
        description = 'Send access token to email informed. Previous registration not required'
        response['request_detail']['description'] = description
        email = request.data.get('email')

        if not email:
            response['data']['error'] = 'Email not sent'
        else:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create user. No need to be registered
                user = User.objects.create_user(email)
            finally:
                # If exist update password to use OAuth workflow
                password = User.objects.make_random_password()
                user.update_password(password)
                # Get tokens
                tokens = User.get_tokens(email, password)
                # get access token and send it by email
                response['data']['message'] = 'Email sent'
                response['data']['access'] = tokens # borrar
                response['status_code'] = 200

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
