from flask import render_template, request
from src.db import query
from src.utils import validate_dates, gen_request, ChartType, is_full_moon

from collections import defaultdict, OrderedDict

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

def index():
	error = family = date_from = date_to = data = None
	percentage = invert_gravity = 0
	cow_size = 10
	cow_speed = 1

	chart_type = ChartType.UNDEFINED

	if request.args.get("date_from", None) and request.args.get("date_to", None) and not validate_dates(request.args.get("date_from", "1990-01-01"), request.args.get("date_to", "1990-01-02")):
		# Dates are present in URL but not valid
		error = "Les dates ne sont pas valides !"

	if request.args.getlist("chart"):
		# Get all URL parameters
		radio = request.args.getlist("chart")[0]
		family = request.args.get("family", None)
		date_from = request.args.get("date_from", None)
		date_to = request.args.get("date_to", None)

		try:
			chart_type = ChartType(int(radio))

		except ValueError:
			error = "Ce type de graphique n'est pas valide !"

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
				percentage = request.args.get("percentage", 0) or 0

				h = "Holstein" if request.args.get("h", None) else None
				j = "Jersey" if request.args.get("j", None) else None
				b = "Blanc Bleu Belge" if request.args.get("b", None) else None

				if not any((h, j, b)):
					error = "Vous devez sélectionner au moins une race !"

				if not 1 <= int(percentage) <= 100:
					error = "Le pourcentage est invalide !"

				data = query(gen_request(chart_type, family=family, breed=[h, j, b], percentage=percentage))
				data = {k: v for k, v in data}

			case ChartType.PASTURE:
				data = query(gen_request(chart_type))
				data = {k: v for k, v in data}

				cow_size = request.args.get("cow_size", 10)
				cow_speed = request.args.get("cow_speed", 1)
				invert_gravity = 1 if request.args.get("invert_gravity", None) else 0

				if not 1 <= int(cow_size) <= 100 or not 1 <= int(cow_speed) <= 10:
					error = "Certains paramètres sont invalides"

	families_sql = query("SELECT * FROM familles")
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

	dates = ["-".join(date[0].split('/')[::-1]) for date in query("SELECT date FROM velages")]

	min_date = dates[0]
	max_date = dates[-1]

	return render_template(
		"index.html",
		title="Home",
		families=families,
		min_date=min_date,
		max_date=max_date,
		error=error,
		data=data,
		chart_id=chart_type.value,
		cow_size=cow_size,
		invert_gravity=invert_gravity,
		cow_speed=cow_speed
	)

def route_handler(app):
	app.add_url_rule("/", view_func=index)
	app.add_url_rule("/index", view_func=index)
