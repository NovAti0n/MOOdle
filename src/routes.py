from flask import render_template
from src.db import query

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

	print(families)

	return render_template("index.html", title="Home", families=families)

def route_handler(app):
	app.add_url_rule("/", view_func=index)
	app.add_url_rule("/index", view_func=index)
