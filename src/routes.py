from cgitb import reset
from flask import render_template, request
from src.db import query
from src.utils import validate_dates,gen_request,ChartType,is_full_moon

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

	error = None
	data = None
	family = None
	date_from = None
	date_to = None
	pourcentage = None
	race = None
	alexis_data = None

	chart_type = ChartType.UNDEFINED

	if request.args:

		if request.args.get("date_from", None) and request.args.get("date_to", None):

			if not validate_dates(request.args.get("date_from", "1990-01-01"), request.args.get("date_to", "1990-01-02")) :

				error = "Les dates ne sont pas valides (Date de fin inférieure à la date de début)"

		if(len(request.args.getlist("chart")) > 0):
			print(request.args.getlist("chart"))
			radio = request.args.getlist("chart")[0]
			family = request.args.get("famille",None)
			date_from = request.args.get("date_from",None)
			date_to = request.args.get("date_to",None)

			if radio.isnumeric():
				chart_type = ChartType(int(radio))

				if chart_type == ChartType.CALVING:
					alexis_data = query(gen_request(chart_type, family=family, date_from=date_from, date_to=date_to))


				if chart_type == ChartType.FULL_MOON:
					alexis_data = query(gen_request(chart_type, family=family, date_from=date_from, date_to=date_to))

					n_full_moon = 0
					for i in alexis_data:
						n_full_moon += 1 if is_full_moon(i[0]) else 0

					alexis_data = [n_full_moon, len(alexis_data) - n_full_moon]

				if chart_type == ChartType.RACE:
					pourcentage = request.args.get("percentage",None)
					race = request.args.get("race",None)

					if int(pourcentage) < 0:
						error = "Le pourcentage ne peux pas être négatif !"

					alexis_data = query(gen_request(chart_type, family=family, race=race, percentage=pourcentage))

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
		data=data,
		error=error,
		my_data = alexis_data,
		chart_id = chart_type.value
	)

def route_handler(app):
	app.add_url_rule("/", view_func=index, methods=["POST", "GET"])
	app.add_url_rule("/index", view_func=index, methods=["POST", "GET"])
