from drf_spectacular.extensions import OpenApiAuthenticationExtension


class MyAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'oauth2_provider.contrib.rest_framework.OAuth2Authentication'
    name = 'MyAuthentication'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            "scheme": "bearer",
            'name': 'Authorization',
        }
