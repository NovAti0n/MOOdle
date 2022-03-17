from flask import render_template
from src import app

def index():
	return render_template("index.html", title="Home")


def route_handler(app):
	app.add_url_rule("/", view_func=index)
	app.add_url_rule("/index",view_func=index)
