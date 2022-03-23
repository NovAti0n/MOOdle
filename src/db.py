import click
import sqlite3
import os
import time

def init_db():
	db = sqlite3.connect("db.sqlite3")
	cursor = db.cursor()

	files = sorted(os.listdir("./src/sql/init"))

	for i in files:
		with open(f"./src/sql/init/{i}") as f:
			script = f.read()

		cursor.executescript(script)
		db.commit()

	db.close()

@click.command("init-db")
def init_db_command():
	click.echo("Generating database...")
	start = time.time()
	init_db()
	click.echo(f"Database initialized in {round(time.time() - start, 2)}s")

def query(statement):
	db = sqlite3.connect("db.sqlite3")
	cursor = db.cursor()

	result = [i for i in cursor.execute(statement)]

	db.close()

	return result
