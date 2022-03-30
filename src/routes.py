from flask import render_template
from src.db import query

def index():
	families = query("SELECT * FROM familles")
	families = filter(lambda family: family[1] != "Unknown", families)
	families = sorted(families, key = lambda family: family[1])

	return render_template("index.html", title="Home", families=families)

def route_handler(app):
	app.add_url_rule("/", view_func=index)
	app.add_url_rule("/index", view_func=index)
