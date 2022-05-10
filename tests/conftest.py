import pytest
from src import app

@pytest.fixture()
def client():
	return app.test_client()
