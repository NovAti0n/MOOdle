from datetime import date
from enum import Enum, auto

class ChartType(Enum):
	CALVING = auto()
	FULL_MOON = auto()
	RACE = auto()

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

	args = f" WHERE {' AND '.join(args)}" if args else ""

	match chart_type:
		case ChartType.CALVING:
			sql = f"SELECT velages.date, COUNT(velages.date) FROM velages LEFT JOIN animaux a ON velages.mere_id = a.id LEFT JOIN familles f ON a.famille_id = f.id"
			sql += args

		case ChartType.FULL_MOON:
			sql = ""

		case ChartType.RACE:
			sql = ""

	return sql

print(gen_request(ChartType.CALVING, date_from="2001-01-01"))
