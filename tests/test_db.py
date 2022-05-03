from pytest import fail
from src.db import query

def test_inheritance():
	"""
	Checks if inheritance is correctly computed
	"""
	try:
		test_cases = [935, 127, 4074, 3973] # animal_id
		results = [[(50.0, 1.0), (50.0, 2.0)], [(50.0, 1.0), (50.0, 2.0)], [(75.0, 1.0)], [(50.0, 1.0), (25.0, 3.0)]]

		for i in range(len(test_cases)):
			case = test_cases[i]
			result = results[i]
			query_result = query(f"SELECT * FROM animaux_types where animal_id = {case}")

			for j in range(len(query_result)):
				assert float(query_result[j][1]) == result[j][1] and float(query_result[j][2]) == result[j][0]

	except IndexError as e:
		fail(str(e))
