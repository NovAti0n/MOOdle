from datetime import date
from flask import render_template, request, request_finished
from src.db import query


def index():
	if request.form.get("date", False):
		pass

	families = query("SELECT * FROM familles")
	families = filter(lambda family: family[1] != "Unknown", families)
	families = sorted(families, key=lambda family: family[1])

	dates = [_[0] for _ in query("SELECT date FROM velages")]
	min_date = "-".join(dates[0].split("/")[::-1])
	max_date = "-".join(dates[-1].split("/")[::-1])

	return render_template(
        "index.html",
        title="Home",
        families=families,
        min_date=min_date,
        max_date=max_date,
    )


def route_handler(app):
    app.add_url_rule("/", view_func=index, methods=["POST", "GET"])
    app.add_url_rule("/index", view_func=index, methods=["POST", "GET"])
