from pytest import fail
from src.db import query

def test_inheritance():
	"""
	Checks if inheritance is correctly computed
	"""
	try:
		test_cases = [935, 127, 4074, 3973] # animal_id

		for i in range(len(test_cases)):
			case = test_cases[i]
			query_result = query(f"SELECT pourcentage FROM animaux_types where animal_id = {case}")
			s = 0
			for i in query_result:
				s += i[0]

			assert s == 100

	except IndexError as e:
		fail(str(e))
