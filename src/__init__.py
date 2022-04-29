import os

from flask import Flask
from src.db import init_db

app = Flask(
	__name__,
	template_folder="../public/templates/",
	static_folder="../public/static",
	static_url_path=""
)

@app.template_global()
def static_include(path):
	path = os.path.join(app.static_folder, path)

	with open(path) as f:
		return f.read()

app.cli.add_command(init_db)

from src import routes # Import is at the bottom because of circular imports
routes.route_handler(app)
