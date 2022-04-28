from datetime import date
from enum import IntEnum, auto

class ChartType(IntEnum):
	CALVING = 0
	FULL_MOON = 1
	RACE = 2

def validate_dates(date1: str, date2: str) -> bool:
	ldate1, ldate2 = date1.split("-"), date2.split("-")
	print(ldate1, ldate2)

	return date(int(ldate1[0]), int(ldate1[1]), int(ldate1[2])) < date(int(ldate2[0]), int(ldate2[1]), int(ldate2[2]))

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

		case ChartType.FULL_MOON:
			sql = ""

		case ChartType.RACE:
			sql = "SELECT COUNT(animal_id) FROM animaux_types LEFT JOIN types t on animaux_types.type_id = t.id"

	sql += args

	return sql
