# This Source Form is subject to the terms of the MOOdle OOpen Dairy LicensE, v. 1.0.
# Copyright (c) 2022 Noa Quenon

import pytest
from src import app

@pytest.fixture()
def client():
	return app.test_client()
