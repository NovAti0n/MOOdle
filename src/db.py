import psycopg
import os

def query(statement: str, *args: str) -> list:
	"""
	Queries the database

	Args:
		- statement (str): SQL query
		- *args (str): Potential arguments to prevent SQL injection

	Returns:
		- list: Results of the query
	"""

	with psycopg.connect(os.environ["DATABASE_URL"]) as db:
		with db.cursor() as cursor:
			result = list(cursor.execute(statement, args).fetchall())

	return result
