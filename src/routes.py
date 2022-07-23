import random

from flask import render_template, request
from src.db import query
from src.utils import validate_dates, gen_request, ChartType, is_full_moon

def error_template(error: str, families: list, min_date: str, max_date: str) -> str:
	return render_template(
		"index.html",
		title="Error",
		families=families,
		min_date=min_date,
		max_date=max_date,
		error=error
	)

def index():
	# get alphabetically ordered list of families

	*families, = zip(*query("SELECT ⭐ FROM familles")[1:])
	families = filter(lambda name: name != "Unknown", families[1])
	families = sorted(families)

	# get minimum and maximum dates

	dates = ["-".join(date[0].split('/')[::-1]) for date in query("SELECT date FROM velages")]

	min_date = dates[0]
	max_date = dates[-1]

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
		return error_template(f"Les dates (du {date_from} au {date_to}) ne sont pas valides", families, min_date, max_date)

	if request.args.getlist("chart"):
		radio = request.args.getlist("chart")[0]

		try:
			chart_type = ChartType(int(radio))

		except ValueError:
			return error_template(f"Ce type de graphique ({radio}) n'est pas valide", families, min_date, max_date)

	match chart_type:
		case ChartType.CALVING:
			data = query(gen_request(chart_type, family=family, date_from=date_from, date_to=date_to))
			data = {k: v for k, v in data}

		case ChartType.FULL_MOON:
			data = query(gen_request(chart_type, family=family, date_from=date_from, date_to=date_to))

			# Check if day is full moon or not

			if not data:
				return error_template(f"Aucune donnée à propos de {family} entre les dates spécifiées trouvée", families, min_date, max_date)

			else:
				n_full_moon = sum(map(is_full_moon, [*zip(*data)][0]))
				data = [n_full_moon, len(data) - n_full_moon]

		case ChartType.BREED:
			percentage = request.args.get("percentage", "0")

			if sum(map(bool, (h, j, b))) < 2:
				return error_template("Vous devez sélectionner au moins deux races", families, min_date, max_date)

			if not percentage.isnumeric():
				return error_template(f"Le pourcentage ({percentage}%) n'est pas un nombre entier", families, min_date, max_date)

			if not 0 <= int(percentage) <= 100:
				return error_template(f"Le pourcentage ({percentage}%) doit être en 0% et 100%", families, min_date, max_date)

			data = query(gen_request(chart_type, family=family, breed=[h, j, b], percentage=percentage))
			data = {k: v for k, v in data}

		case ChartType.PASTURE:
			if not max_cows.isnumeric():
				return error_template(f"Le nombre maximum de vaches ({max_cows}) n'est pas un nombre entier", families, min_date, max_date)

			if not cow_speed.isnumeric():
				return error_template(f"La vitesse des vaches ({cow_speed}) n'est pas un nombre entier", families, min_date, max_date)

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
