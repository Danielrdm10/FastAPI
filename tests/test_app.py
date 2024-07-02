from http import HTTPStatus


def test_read_root_deve_retorna_ok(client):
    # lient = TestClient(app)  # arrange

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


def test_get_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'x',
                'id': 1,
                'email': 'qualquercoisa@gmail.com',
            }
        ]
    }


def test_put(client):
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


def test_delete(client):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'deletado'}
