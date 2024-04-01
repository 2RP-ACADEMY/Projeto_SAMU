def test_user_creation_must_return_status_201_and_object_with_user_data(auth_client):
    response = auth_client.post(
        '/users/',
        {
            "username": "robson",
            "email": "robsonguto1912@gmail.com",
            "name": "Robson Augusto da Silva",
            "password": "123456"
        },
        format='json'
    )
    user_object = {'name': 'Robson Augusto da Silva', 'username': 'robson', 'email': 'robsonguto1912@gmail.com', 'is_active': True}
    assert response.status_code == 201
    assert all(response.data['object'][chave] == valor for chave, valor in user_object.items())
    
def test_user_creation_must_return_status_400_and_error_message(auth_client):
    response = auth_client.post(
        '/users/',
        {
            "username": "robson",
            "email": "robsonguto1912",
            "name": "Robson Augusto da Silva",
            "password": "123456"
        },
        format='json'
    )
    assert "error_name" in response.data['detail']
    assert response.status_code == 400
