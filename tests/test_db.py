from pytest import fail
from src.db import query

def test_inheritance():
	"""
	Checks if inheritance is correctly computed
	"""
	try:
		test_cases = [935, 127, 4074, 3973] # animal_id
		results = [[(50.0, 1), (50.0, 2)], [(50.0, 1), (50.0, 2)], [(75.0, 1)], [(50.0, 1), (25.0, 3)]]
		
		for i in range(len(test_cases)):
			case = test_cases[i]
			result = results[i]
			query_result = query(f"SELECT * FROM animaux_types where animal_id = {case}")
			
			for j in range(len(query_result)):
				assert not(int(query_result[j][1]) == result[j][1] and int(query_result[j][2]) == result[j][0])
					
	except IndexError as e:
		fail(e)
