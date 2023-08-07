# This Source Form is subject to the terms of the MOOdle OOpen Dairy LicensE, v. 1.0.
# Copyright (c) 2022 Alexis Englebert
# Copyright (c) 2022 Noa Quenon
# Copyright (c) 2022 Aymeric Wibo

import click
import sqlite3
import os
import pathlib
import time

@click.command("init-db")
def init_db() -> None:
	"""
	Initializes the database by executing every file in /sql
	"""

	start = time.time() # Get current time
	db = sqlite3.connect("db.sqlite3")
	cursor = db.cursor()

	with click.progressbar(sorted(os.listdir("./src/sql")), label="Generating database...") as files:
		# Generate the database with files in /sql

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

	statement = statement.replace('⭐', '*')

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

	parents = query("SELECT ⭐ FROM animaux_types")
	parents.sort(key=lambda a: a[0])

	animals = {}

	# Add all parent in map

	while parents:
		animal_id, type_id, pourcentage = parents.pop(0)
		animals[animal_id] = [(type_id, pourcentage)]

	to_process = [tuple(map(int, calving)) for calving in query("SELECT id, mere_id, pere_id FROM velages")]

	# Loop until all is processed

	while to_process:
		for velage_id, mere_id, pere_id in to_process:
			# Check if both parents are here for this calving

			if not animals.get(mere_id, False) or not animals.get(pere_id, False):
				continue

			# Get the animal ID

			animal_id = query(f"SELECT animal_id FROM animaux_velages where velage_id = {velage_id}")

			for calving in [*zip(*animal_id)][0]:
				distrib = {1: 0, 2: 0, 3: 0}

				# Compute the percentage

				mother = animals.get(mere_id)
				father = animals.get(pere_id)

				if mother is None or father is None:
					# Mother or father are unlikely to be None, but let's make sure that nothing terrible happens
					raise ValueError("Missing data in map")

				for breed in mother:
					type_id, pourcentage = breed
					distrib[type_id] += pourcentage / 2

				for breed in father:
					type_id, pourcentage = breed
					distrib[type_id] += pourcentage / 2

				# Add the animal as a parent

				animals[calving] = [(key, value) for key, value in distrib.items() if value > 0]

			to_process.remove((velage_id, mere_id, pere_id))

	result = ["DELETE FROM animaux_types"]

	for key, values in animals.items():
		result.extend(f"INSERT INTO animaux_types VALUES ({key}, {value[0]}, {value[1]});\n" for value in values)

	return result
