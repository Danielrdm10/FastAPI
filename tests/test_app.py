from http import HTTPStatus

from fast.schemas import UserPublic


def test_read_root_deve_retorna_ok(client):
    # client = TestClient(app)  # arrange

    response = client.get('/')  # act

    assert response.status_code == HTTPStatus.OK  # assert


def test_create_user(client):
    # client = TestClient(app)  # arrange

    response = client.post(
        '/users/',
        json={
            'username': 'x',
            'password': 'i',
            'email': 'qualquercoisa@gmail.com',
        },
    )

    # validar user public
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'x',
        'id': 1,
        'email': 'qualquercoisa@gmail.com',
    }


def test_get_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()  # converter o user orm em pydentic
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_put(client, user):
    response = client.put(
        '/users/1',
        json={
            'password': '123',
            'username': 'x',
            'id': 1,
            'email': 'qualquercoisa@gmail.com',
        },
    )
    assert response.json() == {
        'username': 'x',
        'id': 1,
        'email': 'qualquercoisa@gmail.com',
    }


def test_delete(client, user):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'usuario deletado'}


def test_get_token(client, user):
    response = client.post('/token/', 
                           data={'username': user.email, 
                                 'password': user.clean_password})  # formulário não é json, é data

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
