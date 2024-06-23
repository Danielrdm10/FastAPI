import pytest
from fastapi.testclient import TestClient

from fast.app import app


@pytest.fixture()
def client():
    return TestClient(app)
