from pytest import fixture
from rest_framework.test import APIClient
from samu.tests.factories.userFactory import UserFactory

@fixture(scope="session")
def client(django_db_setup, django_db_blocker,)-> APIClient:
    with django_db_blocker.unblock():
        client = APIClient()
        yield client

@fixture(scope="session")
def auth_token(client):
    response = client.post('/auth/login/', data={
            "username": "admin",
            "password": "admin"
        }, format='json')
    yield response.data['token'].decode('utf-8')

@fixture(scope="session")
def auth_client(auth_token, client) -> APIClient:
        client.credentials(
            HTTP_AUTHORIZATION=f"Token {auth_token}"
        )
        yield client

@fixture
def create_users():
    return UserFactory.create_batch(5)