from flask import Flask

app = Flask(
	__name__,
	template_folder="../public/templates/",
	static_folder="../public/static",
	static_url_path=""
)

from src import routes # Import is at the bottom because of circular imports
