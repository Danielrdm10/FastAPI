import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast.app import app
from fast.database import get_session
from fast.models import User, table_registry
from fast.security import get_password_hash


@pytest.fixture()
def client(session):
    def fake_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = fake_session

        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    user = User(username='teste', email='teste@tmail.com', password=get_password_hash('testeteste'))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testeteste'  # monkey patch

    return user


@pytest.fixture()
def token(client, user):
    response = client.post('/token', data={'username': user.email, 'password': user.clean_password})

    return response.json()['access_token']
