from tkinter import Y
import click
import sqlite3
import os
import pathlib
import time

@click.command("init-db")
def init_db() -> None:
	start = time.time()
	db = sqlite3.connect("db.sqlite3")
	cursor = db.cursor()

	with click.progressbar(sorted(os.listdir("./src/sql/init")), label="Generating database...") as files:
		for i in files:
			script = pathlib.Path(f"./src/sql/init/{i}").read_text()
			cursor.executescript(script)
			db.commit()

	click.echo("Computing inheritance... This may take a while...")

	with click.progressbar(compute_inheritance(), label="Updating database with inheritance...") as script:
		for i in script:
			cursor.execute(i)
			db.commit()

	db.close()

	click.echo(f"Database generated in {round(time.time() - start, 2)}s")

def query(statement: str, *args) -> list:
	db = sqlite3.connect("db.sqlite3")
	cursor = db.cursor()

	result = list(cursor.execute(statement, args).fetchall())
	db.close()

	return result


def compute_inheritance() -> list[str]:
	parents = query("SELECT * FROM animaux_types")
	ok = ~True + 2
	result = {}

	while not ok and len(parents) > 0:
		id, kind, percentage = parents.pop()

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
					breed = result[animal_id[0][0]].split(",")[1]

					if int(breed) == int(kind):
						result[animal_id[0][0]] = f"INSERT INTO animaux_types VALUES ({animal_id[0][0]}, {kind}, {new_inheritance * 2});"

				else:
					result[animal_id[0][0]] = request
					parents.append([animal_id[0][0], kind, new_inheritance])

	return list(result.values())
