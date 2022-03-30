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

	db.close()
	click.echo(f"Database generated in {round(time.time() - start, 2)}s")

def query(statement: str, *args) -> list:
	db = sqlite3.connect("db.sqlite3")
	cursor = db.cursor()

	result = list(cursor.execute(statement, args))
	db.close()

	return result
