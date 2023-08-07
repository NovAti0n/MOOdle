# This Source Form is subject to the terms of the MOOdle OOpen Dairy LicensE, v. 1.0.
# Copyright (c) 2022 Noa Quenon

def test_app_main(client):
	response = client.get("/")
	assert response.status_code == 200
