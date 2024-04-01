import factory
from samu.models.userModel import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Faker('name')
    email = factory.Faker('email')
    username = factory.Faker('name')
    is_staff = factory.Faker('pybool')
    is_superuser = factory.Faker('pybool')
    is_active = factory.Faker('pybool')
    is_deleted = False