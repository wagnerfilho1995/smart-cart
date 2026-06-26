import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append("../../app/")

from app import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
