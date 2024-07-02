import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast.app import app
from fast.database import get_session
from fast.models import table_registry


@pytest.fixture()
def client(session):
    
    def fake_session():
        return session            
    
    with TestClient(app) as client:
        client.dependency_overrides[get_session] = fake_session
        
        yield client
        
    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine('sqlite:///:memory:',
                           connect_args={'check_same_thread' : False},
                           poolclass=StaticPool)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
