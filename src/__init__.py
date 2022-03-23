from flask import Flask
from src.db import init_db_command

app = Flask(
	__name__,
	template_folder="../public/templates/",
	static_folder="../public/static",
	static_url_path=""
)

app.cli.add_command(init_db_command)

from src import routes # Import is at the bottom because of circular imports
routes.route_handler(app)
