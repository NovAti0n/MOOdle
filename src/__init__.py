import os

from flask import Flask, redirect, request
from src import routes

app = Flask(
	__name__,
	template_folder="../public/templates/",
	static_folder="../public/static",
	static_url_path=""
)

@app.before_request
def redirect_from_heroku():
	if request.headers.get("Host") == "moodle-ucl.herokuapp.com/":
		return redirect("https://moodle.novation.dev", code=301)

@app.template_global()
def static_include(path: str) -> str:
	"""
	Includes file in HTML template

	Args:
		- path (str): path to file
	"""

	path = os.path.join(app.static_folder, path)

	with open(path) as f:
		return f.read()

routes.route_handler(app)
