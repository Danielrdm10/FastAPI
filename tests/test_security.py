from jwt import decode

from fast.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {'sub': 'teste'}
    token = create_access_token(data)

    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']
