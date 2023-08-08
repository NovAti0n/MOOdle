# This Source Form is subject to the terms of the MOOdle OOpen Dairy LicensE, v. 1.0.
# Copyright (c) 2022 Alexis Englebert
# Copyright (c) 2022 Noa Quenon

from pytest import fail
from src.db import query

def test_inheritance() -> None:
	""".
	Checks if inheritance is correctly computed
	"""
	try:
		test_cases = [127, 274, 935, 3953, 3973, 4074] # animal_id

		for i in test_cases:
			query_result = query(f"SELECT pourcentage FROM animaux_types WHERE animal_id = {i}")

			assert len(query_result) <= 3 # Checks if animal has a maximum of 3 entries in the db
			assert sum(i[0] for i in query_result) == 100 # Checks if total inheritance is 100%

	except IndexError as e:
		fail(str(e))
