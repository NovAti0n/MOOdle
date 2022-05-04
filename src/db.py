from ipaddress import v4_int_to_packed
from termios import VLNEXT
import click
import sqlite3
import os
import pathlib
import time
import copy

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
				cursor.execute(i)
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
	Computes the percentage of breed inheritance

	Returns:
		- list[str]: SQL queries to add to the database
	"""

	parents = query("SELECT * FROM animaux_types")
	parents.sort(key=lambda a : a[0])

	ok = ~True + 2
	map = {}
	to_proceed = []

	# Add all parent in map

	while(len(parents) > 0):
		animal_id, type_id, pourcentage = parents.pop(0)
		map[animal_id] = [(type_id,pourcentage)]

	# Get all animals in the farm

	with open("src/sql/insert_velages.sql","r") as file:
		for i in file:
			i = i .replace("INSERT INTO velages VALUES (","").replace("); ","").replace("\\n","").split(",")
			to_proceed.append((int(i[0]),int(i[1]),int(i[2])))

	# Loop until all is proceed

	while not ok and len(to_proceed) > 0:

		for velage_id, mere_id, pere_id in to_proceed:

			#Check if both parents are here for this velage

			if map.get(mere_id, False) and map.get(pere_id, False):

				# Get the animal id

				animal_id = query(f"SELECT animal_id FROM animaux_velages where velage_id = {velage_id}")
				for calving in [*zip(*animal_id)][0]:
					repartition = {1:0, 2:0, 3:0}

					# Calculate the percentage
					mother = map.get(mere_id, None)
					father = map.get(pere_id, None)

					for i in mother:
						type_id, pourcentage = i
						repartition[type_id] += pourcentage / 2
					for i in father:
						type_id, pourcentage = i
						repartition[type_id] += pourcentage / 2

					# Add the animal as a parent

					inheritance = []
					for key, value in repartition.items():
						if value > 0:
							inheritance.append((key, value))

					map[calving] = list(inheritance)

				to_proceed.remove((velage_id, mere_id, pere_id))


	result = ["DELETE FROM animaux_types"]
	for key, values in map.items():
		for value in values:
			req = f"INSERT INTO animaux_types VALUES ({key}, {value[0]}, {value[1]});\n"
			result.append(req)

	return list(result)
