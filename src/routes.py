import random
from collections import defaultdict, OrderedDict

from flask import render_template, request
from src.db import query
from src.utils import validate_dates, gen_request, ChartType, is_full_moon

class Family:
	def __init__(self, name):
		self.name = name

		# how many animals of which breed?
		# unknown breed is represented by '-1'
		# some animals may be half of one breed, half of another

		self.breeds = defaultdict(float)

	def __repr__(self):
		return self.name

	@property
	def count(self):
		return int(sum(self.breeds.values()))

def error_template(error: str, families: dict):
	return render_template(
		"index.html",
		title="Error",
		families=families,
		error=error
	)

def index():
	# get list of families

	families_sql = query("SELECT ⭐ FROM familles")
	families_sql = filter(lambda family: family[1] != "Unknown", families_sql)
	families_sql = sorted(families_sql, key = lambda family: family[1])

	# ordered (alphabetically) dictionary of families with their id as key and a 'Family' object as value

	families = OrderedDict()

	for family_id, name in families_sql[1:]:
		family = Family(name)
		families[family_id] = family

		animals = query(f"SELECT id FROM animaux WHERE famille_id = {family_id}")

		if not animals:
			continue

		for animal, in animals:
			breed_ids = query(f"SELECT type_id FROM animaux_types WHERE animal_id = {animal}")

			if not breed_ids:
				family.breeds[-1] += 1
				break

			for breed_id, in breed_ids:
				family.breeds[breed_id] += 1 / len(breed_ids)

	# process arguments

	data = None
	percentage = 0

	chart_type = ChartType.PASTURE

	date_from = request.args.get("date_from", None)
	date_to   = request.args.get("date_to",   None)

	family = request.args.get("family")

	h = "Holstein"         if "h" in request.args else None
	j = "Jersey"           if "j" in request.args else None
	b = "Blanc Bleu Belge" if "b" in request.args else None

	max_cows = request.args.get("max_cows", "250")
	cow_speed = request.args.get("cow_speed", "1")
	invert_gravity = "true" if "invert_gravity" in request.args else "false"
	proper_cows = "proper_cows" in request.args

	if "date_from" in request.args and "date_to" in request.args and not validate_dates(date_from, date_to):
		return error_template("Les dates ne sont pas valides")

	if request.args.getlist("chart"):
		radio = request.args.getlist("chart")[0]

		try:
			chart_type = ChartType(int(radio))

		except ValueError:
			return error_template("Ce type de graphique n'est pas valide", families)

	match chart_type:
		case ChartType.CALVING:
			data = query(gen_request(chart_type, family=family, date_from=date_from, date_to=date_to))
			data = {k: v for k, v in data}

		case ChartType.FULL_MOON:
			data = query(gen_request(chart_type, family=family, date_from=date_from, date_to=date_to))

			# Check if day is full moon or not

			n_full_moon = sum(map(is_full_moon, [*zip(*data)][0]))
			data = [n_full_moon, len(data) - n_full_moon]

		case ChartType.BREED:
			percentage = request.args.get("percentage", "0")

			if not any((h, j, b)):
				return error_template("Vous devez sélectionner au moins une race", families)

			if not percentage.isnumeric():
				return error_template("Le pourcentage n'est pas un nombre entier", families)

			if not 0 <= int(percentage) <= 100:
				return error_template("Le pourcentage doit être en 0% et 100%", families)

			data = query(gen_request(chart_type, family=family, breed=[h, j, b], percentage=percentage))
			data = {k: v for k, v in data}

		case ChartType.PASTURE:
			if not max_cows.isnumeric():
				return error_template("Le nombre maximum de vaches n'est pas un nombre entier", families)

			if not cow_speed.isnumeric():
				return error_template("La vitesse des vaches n'est pas un nombre entier", families)

			if proper_cows:
				data = query(gen_request(chart_type))
				data = {k: v for k, v in data}

			else:
				# generate a random distribution of cow breeds

				data = {
					"Holstein":         random.randint(50, 100),
					"Jersey":           random.randint(50, 100),
					"Blanc Bleu Belge": random.randint(50, 100),
				}

			# normalize data and multiply it by the number of cows we want to draw

			data = {k: v / sum(data.values()) * int(max_cows) for k, v in data.items()}

	dates = ["-".join(date[0].split('/')[::-1]) for date in query("SELECT date FROM velages")]

	min_date = dates[0]
	max_date = dates[-1]

	return render_template(
		"index.html",
		title="Home",
		families=families,
		min_date=min_date,
		max_date=max_date,
		data=data,
		chart_id=chart_type.value,
		cow_speed=cow_speed,
		invert_gravity=invert_gravity,
	)

def route_handler(app):
	app.add_url_rule("/", view_func=index)
	app.add_url_rule("/index", view_func=index)
