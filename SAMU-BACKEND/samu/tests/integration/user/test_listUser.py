from samu.tests.factories.userFactory import UserFactory

def test_list_user_must_return_status_200_and_object_with_list_of_users(auth_client):
    response = auth_client.get(f'/users/')
    user_fields = [
        'id',
        'name',
        'username',
        'is_active',
        'email'
    ]
    assert all(field in user_fields for field in dict(response.data['object'][0]))
    assert response.status_code == 200

def test_list_user_must_return_object_with_list_of_users_ordered_by_id_reverse(auth_client, create_users):
    response = auth_client.get(f'/users/?ordering=-id')
    
    assert response.data['object'] == sorted(response.data['object'], key=lambda x: x['id'], reverse=True)

def test_list_user_must_return_object_with_list_of_searched_users_by_name(auth_client):
    user_created  = UserFactory.create(
        name="José Bezerra da Silva Antunes Segundo"
    )
    response = auth_client.get(f'/users/?search=José Bezerra da Silva Antunes Segundo')
    response_user_name = response.data['object'][0]['name']
    assert response_user_name == "José Bezerra da Silva Antunes Segundo"

def test_list_user_must_return_object_with_list_of_searched_users_by_username(auth_client):
    user_created = UserFactory.create(
        username="tonio_carlos_1943"
    )
    response = auth_client.get(f'/users/?search=tonio_carlos_1943')
    reponse_username = response.data['object'][0]['username']
    assert reponse_username == "tonio_carlos_1943"

def test_list_user_must_return_object_with_list_of_filtered_users_by_field_is_active(auth_client):
    UserFactory.create_batch(
        2,
        is_active=False
    )
    response = auth_client.get(f'/users/?is_active=false')
    user_list = response.data['object']
    assert all(user['is_active'] is False for user in user_list)