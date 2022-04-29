import pytest
from src import app
from src.db import init_db

@pytest.fixture()
def client():
	return app.test_client()

@pytest.fixture()
def runner():
	return app.test_cli_runner()

@pytest.fixture()
def client_with_db():
	init_db()
	return app.test_client()
