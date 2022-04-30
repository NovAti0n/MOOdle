import math, decimal, datetime
from enum import IntEnum

from pyparsing import Char

class ChartType(IntEnum):
	CALVING = 0
	FULL_MOON = 1
	BREED = 2
	UNDEFINED = 3

def validate_dates(first: str, second: str) -> bool:
	first_bits, second_bits = first.split("-"), second.split("-")
	return datetime.date(*map(int, first_bits)) < datetime.date(*map(int, second_bits))

def gen_request(chart_type: ChartType, family=None, breed=None, forhunderedage=None, date_from=None, date_to=None):
	sql, args = None, []

	if family:
		args.append(f"f.nom = \"{family}\"")

	if date_from:
		args.append(f"velages.date >= \"{date_from}\"")

	if date_to:
		args.append(f"velages.date <= \"{date_to}\"")

	if breed:
		args.append(f"t.type = \"{breed}\"")

	if forhunderedage:
		args.append(f"at.pourcentage >= \"{forhunderedage}\"")

	args = f" WHERE {' AND '.join(args)}" if args else ""

	if chart_type == ChartType.CALVING:
		sql = "SELECT velages.date, COUNT(velages.date) FROM velages LEFT JOIN animaux a ON velages.mere_id = a.id LEFT JOIN familles f ON a.famille_id = f.id"
		sql += f"{args} GROUP BY velages.date"

	elif chart_type == ChartType.FULL_MOON:
		sql = "SELECT velages.date FROM velages LEFT JOIN animaux a ON velages.mere_id = a.id LEFT JOIN familles f ON a.famille_id = f.id"
		sql += args

	elif chart_type == ChartType.BREED:
		sql = "SELECT COUNT(animal_id) FROM animaux_types LEFT JOIN types t on animaux_types.type_id = t.id"
		sql += args

	return sql

# Based of a script by Sean B. Palmer (inamidst.com)
# Source: https://gist.github.com/miklb/ed145757971096565723

def is_full_moon(time):
	year, month, day = time.split("-")
	dec = decimal.Decimal

	diff = datetime.datetime(int(year), int(month), int(day)) - datetime.datetime(2001, 1, 1)
	days = dec(diff.days) + dec(diff.seconds) / dec(86400)
	lunations = dec("0.20439731") + days * dec("0.03386319269")

	index = lunations % dec(1) * dec(8) + dec("0.5")
	index = math.floor(index)

	return int(index) & 7 == 4



