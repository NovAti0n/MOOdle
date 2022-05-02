from cgi import test


def test_inheritance(client):
	# Check if inheritance is correctly computed :O

	test_cases = [935, 127,4074,3973] # <- animaux
	results = [[(100,1)], [(50.0,1),(50.0,2)],[(75.0,1)],[(50.0,1),(25.0,3)]]
	for i in range(test_cases):
		case = test_cases[i]
		result = results[i]
		#COMMANDE SQL TODO

