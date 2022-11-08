import factory.django
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserModel

    email = factory.Faker('free_email')
    username = factory.Faker('pystr', max_chars=10)
    password = factory.Faker('pyint', max_value=10)
