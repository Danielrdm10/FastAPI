from sqlalchemy import select

from fast.models import User


def test_create_user(session):
    user = User(username='Daniel', email='qualquerd@gmail.com', password='123')

    session.add(user)
    session.commit()
    result = session.scalar(select(User).where(User.email == 'qualquerd@gmail.com'))

    assert result.username == 'Daniel'
