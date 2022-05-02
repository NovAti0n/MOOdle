from cgi import test
from tracemalloc import reset_peak
from src.db import query

def test_inheritance(client):
	# Check if inheritance is correctly computed :O
	try:
		test_cases = [935, 127,4074,3973] # <- animaux
		results = [[(50.0,1),(50.0,2)], [(50.0,1),(50.0,2)],[(75.0,1)],[(50.0,1),(25.0,3)]]
		for i in range(len(test_cases)):
			case = test_cases[i]
			result = results[i]
			query_result = query(f"SELECT * FROM animaux_types where animal_id = {case}")
			for j in range(len(query_result)):
				print(len(query_result),len(result),case)
				if not(int(query_result[j][1]) == result[j][1] and int(query_result[j][2]) == result[j][0]):
					assert "Error while testing inheritance"
	except IndexError:
		assert "Error while testing inheritance"


