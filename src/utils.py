import math, decimal, datetime
from enum import IntEnum

class ChartType(IntEnum):
	CALVING = 0
	FULL_MOON = 1
	RACE = 2

def validate_dates(date1: str, date2: str) -> bool:
	ldate1, ldate2 = date1.split("-"), date2.split("-")

	return datetime.date(int(ldate1[0]), int(ldate1[1]), int(ldate1[2])) < datetime.date(int(ldate2[0]), int(ldate2[1]), int(ldate2[2]))

def gen_request(chart_type: ChartType, family=None, race=None, percentage=None, date_from=None, date_to=None):
	args = []

	if family:
		args.append(f"f.nom = \"{family}\"")

	if date_from:
		args.append(f"velages.date >= \"{date_from}\"")

	if date_to:
		args.append(f"velages.date <= \"{date_to}\"")

	if race:
		args.append(f"t.type = \"{race}\"")

	if percentage:
		args.append(f"at.pourcentage >= \"{percentage}\"")

	args = f" WHERE {' AND '.join(args)}" if args else ""

	match chart_type:
		case ChartType.CALVING:
			sql = f"SELECT velages.date, COUNT(velages.date) FROM velages LEFT JOIN animaux a ON velages.mere_id = a.id LEFT JOIN familles f ON a.famille_id = f.id"
			sql += f"{args} GROUP BY velages.date"

		case ChartType.FULL_MOON:
			sql = "SELECT velages.date FROM velages LEFT JOIN animaux a ON velages.mere_id = a.id LEFT JOIN familles f ON a.famille_id = f.id"
			sql += args

		case ChartType.RACE:
			sql = "SELECT COUNT(animal_id) FROM animaux_types LEFT JOIN types t on animaux_types.type_id = t.id"
			sql += args

	return sql

# Based of a script by Sean B. Palmer (inamidst.com)
# Source: https://gist.github.com/miklb/ed145757971096565723

def is_full_moon(time):
	(year, month, day) = time.split("-")
	dec = decimal.Decimal

	diff = datetime.datetime(int(year), int(month), int(day)) - datetime.datetime(2001, 1, 1)
	days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
	lunations = dec("0.20439731") + (days * dec("0.03386319269"))

	index = (lunations % dec(1) * dec(8)) + dec("0.5")
	index = math.floor(index)
	return (int(index) & 7) == 4
