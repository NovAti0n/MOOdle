from flask import render_template, request
from src.db import query
from src.utils import validate_dates

from collections import defaultdict, OrderedDict

class Family:
	def __init__(self, name):
		self.name = name

		# how many animals of which breed?
		# unknown breed is represented by '-1'
		# some animals may be half of one breed, half of another

		self.breeds = defaultdict(float)

	@property
	def count(self):
		return int(sum(self.breeds.values()))

def index():
	error = data = None

	if request.args:
		if not validate_dates(request.args.get("date_from", "1990-01-01"), request.args.get("date_to",  "1990-01-02")) :
			error = "Les dates ne sont pas valides (Date de fin inférieure à la date de début)"

	families_sql = query("SELECT * FROM familles")
	families_sql = filter(lambda family: family[1] != "Unknown", families_sql)
	families_sql = sorted(families_sql, key = lambda family: family[1])

	# ordered (alphabetically) dictionary of families with their id as key and a 'Family' object as value

	families = OrderedDict()

	for family_id, name in families_sql:
		family = Family(name)

		animals = query(f"SELECT id FROM animaux WHERE famille_id = {family_id}")

		if animals:
			for animal, in animals:
				type_ids = query(f"SELECT type_id FROM animaux_types WHERE animal_id = {animal}")

				if not type_ids:
					family.breeds[-1] += 1
					break

				for type_id, in type_ids:
					family.breeds[type_id] += 1 / len(type_ids)

		families[family_id] = family

	dates = [_[0] for _ in query("SELECT date FROM velages")]
	min_date = "-".join(dates[0].split("/")[::-1])
	max_date = "-".join(dates[-1].split("/")[::-1])

	return render_template(
		"index.html",
		title="Home",
		families=families,
		min_date=min_date,
		max_date=max_date,
		data=data,
		error=error
	)

def route_handler(app):
	app.add_url_rule("/", view_func=index, methods=["POST", "GET"])
	app.add_url_rule("/index", view_func=index, methods=["POST", "GET"])
