import click
import sqlite3
import os
import pathlib
import time

@click.command("init-db")
def init_db() -> None:
	"""
	Initializes the database by executing every file in sql/init
	"""
	start = time.time() # Get current time
	db = sqlite3.connect("db.sqlite3")
	cursor = db.cursor()

	with click.progressbar(sorted(os.listdir("./src/sql")), label="Generating database...") as files:
		# Generate the database with files in sql/init
		for i in files:
			script = pathlib.Path(f"./src/sql/{i}").read_text()
			cursor.executescript(script)
			db.commit()

	click.echo("Computing inheritance... This may take a while...")

	with click.progressbar(compute_inheritance(), label="Updating database with inheritance...") as script:
		# Insert inheritance data
		for i in script:
			for j in i:
				cursor.execute(j)
				db.commit()

	db.close()

	click.echo(f"Database generated in {round(time.time() - start, 2)}s")

def query(statement: str, *args: str) -> list:
	"""
	Queries the database

	Args:
		- statement (str): SQL query
		- *args (str): Potential arguments to prevent SQL injection

	Returns:
		- list: Results of the query
	"""
	db = sqlite3.connect("db.sqlite3")
	cursor = db.cursor()

	result = list(cursor.execute(statement, args).fetchall())
	db.close()

	return result

def compute_inheritance() -> list[str]:
	"""
	:pre: -
	:post:
		- return a list of query to insert inheritance into the data base
	"""
	parents = query("SELECT * FROM animaux_types")
	parents.sort(key=lambda a : a[0])
	ok = ~True + 2
	result = {}

	while not ok and len(parents) > 0:
		id, kind, percentage = parents.pop(0)

		#Get all velages with these parents
		calving_id = query(f"SELECT id FROM velages WHERE mere_id = {int(id)} OR  pere_id = {int(id)} ")

		if len(calving_id) > 0:
			# Get the animal id
			for calving in [*zip(*calving_id)][0]:
				animal_id = query(f"SELECT animal_id FROM animaux_velages WHERE velage_id = {calving}")

				# Get the sex
				sex = query(f"SELECT sexe FROM animaux WHERE id = {animal_id[0][0]}")

				# Divide the inheritance by 2
				new_inheritance = percentage / 2
				request = f"INSERT INTO animaux_types VALUES ({animal_id[0][0]}, {kind}, {new_inheritance});"

				# Check if both parent are same types
				if result.get(animal_id[0][0], False):
					# Compare the breed
					breed = result[animal_id[0][0]][0].split(",")[1]
					herithance = int(float(result[animal_id[0][0]][0].split(",")[2].replace(");","")))
					if int(breed) == int(kind):
						result[animal_id[0][0]] = [f"INSERT INTO animaux_types VALUES ({animal_id[0][0]}, {kind}, {new_inheritance  + herithance});"]
					else:
						result[animal_id[0][0]].append(request)

				else:
					result[animal_id[0][0]] = [request]
					parents.append([animal_id[0][0], kind, new_inheritance])

	return [i for i in result.values()]
