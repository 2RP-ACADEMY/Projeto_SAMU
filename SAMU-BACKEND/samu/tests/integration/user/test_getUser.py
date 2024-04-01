from samu.tests.factories.userFactory import UserFactory
from samu.serializers.userSerializer import UserSerializer

def test_get_user_must_return_status_200_and_object_with_user(auth_client):
    user_created  = UserFactory.create()
    user_id = user_created .id
    response = auth_client.get(f'/users/{user_id}/')
    response_user = response.data['object']
    assert response_user == UserSerializer(user_created ).data
    assert response.status_code == 200

def test_get_user_must_return_status_404_and_error_name(auth_client):
    response = auth_client.get('/users/92839182/')
    assert 'error_name' in response.data['detail']
    assert response.status_code == 404