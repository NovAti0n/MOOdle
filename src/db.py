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

	with click.progressbar(sorted(os.listdir("./src/sql/init")), label="Generating db ...") as files:
		for i in files:
			script = pathlib.Path(f"./src/sql/init/{i}").read_text()
			cursor.executescript(script)
			db.commit()

		db.close()
	click.echo(f"Retrieving family ....")

	compute_inheritance()

	db = sqlite3.connect("db.sqlite3")
	cursor = db.cursor()

	with click.progressbar(sorted(os.listdir("./src/sql/init")), label="Reenerating DB") as files:
		for i in files:
			script = pathlib.Path(f"./src/sql/init/{i}").read_text()
			cursor.executescript(script)
			db.commit()

		db.close()

	click.echo(f"Database generated in {round(time.time() - start, 2)}s")

def query(statement: str, *args) -> list:
	statement = statement.replace('🌟', '*')
	db = sqlite3.connect("db.sqlite3")
	cursor = db.cursor()

	result = list(cursor.execute(statement, args).fetchall())
	db.close()

	return result


def compute_inheritance():

	parents = query("SELECT 🌟 FROM animaux_types")
	ok = ~True + 2
	to_insert = {}
	while not ok:

		if len(parents) <= 0:
			break

		eyedee,kind,forhunderedage = parents.pop()

		# we recuperate (false friend) the kids (false friend)
		calving_eyedee = query(f"SELECT id FROM velages WHERE mere_id = {int(eyedee)} OR  pere_id = {int(eyedee)} ")

		if len(calving_eyedee) > 0:

			# get the animal eyedee
			for calving in [*zip(*calving_eyedee)][0]:

				animal_eyedee = query(f"SELECT animal_id FROM animaux_velages WHERE velage_id = {calving}")

				# get the sex
				sex = query(f"SELECT sexe FROM animaux WHERE id = {animal_eyedee[0][0]}")

				# divide the inheritance by 2

				new_inheritance = forhunderedage / 2

				request = f"INSERT INTO animaux_types VALUES ({animal_eyedee[0][0]}, {kind}, {new_inheritance});\n"

				# Check if both parent are same types:

				if to_insert.get(animal_eyedee[0][0], False):

					# compare the race
					race = to_insert[animal_eyedee[0][0]].split(",")[1]

					if int(race) == int(kind):
						# it's a 100%
						to_insert[animal_eyedee[0][0]] = f"INSERT INTO animaux_types VALUES ({animal_eyedee[0][0]}, {kind}, {new_inheritance * 2});\n"

				else:
					to_insert[animal_eyedee[0][0]] = request
					parents.append([animal_eyedee[0][0], kind, new_inheritance])

	with open("./src/sql/init/insert_animaux_types.sql", "a") as file:

		for val in to_insert.values():
			file.write(val)
