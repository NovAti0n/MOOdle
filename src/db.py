import click
import sqlite3
import os
import pathlib
import time

@click.command("init-db")
def init_db():
	start = time.time()
	db = sqlite3.connect("db.sqlite3")
	cursor = db.cursor()

	files = sorted(os.listdir("./src/sql/init"))

	with click.progressbar(sorted(os.listdir("./src/sql/init")), label="Generating database...") as files:
		for i in files:
			script = pathlib.Path(f"./src/sql/init/{i}").read_text()
			cursor.executescript(script)
			db.commit()

	db.close()
	click.echo(f"Database generated in {round(time.time() - start, 2)}s")

def query(statement):
	db = sqlite3.connect("db.sqlite3")
	cursor = db.cursor()

	result = list(cursor.execute(statement))

	db.close()

	return result