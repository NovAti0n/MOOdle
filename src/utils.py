import math, decimal, datetime
from enum import IntEnum
from markupsafe import escape

class ChartType(IntEnum):
	CALVING   = 0
	FULL_MOON = 1
	BREED     = 2
	PASTURE   = 3
	UNDEFINED = 4

def validate_dates(first: str | None, second: str | None) -> bool:
	"""
	Checks if dates are in a valid format (first date is before second date)

	Args:
		- first (str): First date to check
		- second (str): Second date to check

	Returns:
		- bool: True if dates are correct, False otherwise
	"""

	if first is None or second is None:
		return True

	first_bits, second_bits = first.split("-"), second.split("-")

	try:
		return datetime.date(*map(int, first_bits)) <= datetime.date(*map(int, second_bits))

	except ValueError:
		return False

def gen_request(chart_type: ChartType, family: None | str = None, breed: None | list[str | None] = None, percentage: None | str | int = None, date_from: None | str = None, date_to: None | str = None) -> str:
	"""
	Generates a request based of arguments passed to the function

	Args:
		- chart_type (ChartType): Type of chart to visualize
		- family (None | str): Family to visualize. Defaults to None
		- breed (None | list[None | str]): Breeds to visualize. Defaults to None
		- percentage (None | str | int): Minimum percentage to visualize. Defaults to None
		- date_from (None | str): Minimum date from which to view. Defaults to None
		- date_to (None | str): Maximum date until which to view. Defaults to None

	Returns:
		- str: SQL query
	"""

	sql = ""
	args = []

	if family:
		args.append(f"f.nom = \"{escape(family)}\"")

	if date_from:
		args.append(f"velages.date >= \"{escape(date_from)}\"")

	if date_to:
		args.append(f"velages.date <= \"{escape(date_to)}\"")

	if breed:
		args.append(" OR ".join([f"type = \"{escape(i)}\"" for i in breed]))

	if percentage:
		args.append(f"animaux_types.pourcentage >= {escape(percentage)}")

	args = f" WHERE {' AND '.join(args)}" if args else ""

	match chart_type:
		case ChartType.CALVING:
			sql = "SELECT velages.date, COUNT(velages.date) FROM velages LEFT JOIN animaux a ON velages.mere_id = a.id LEFT JOIN familles f ON a.famille_id = f.id"
			sql += f"{args} GROUP BY velages.date"

		case ChartType.FULL_MOON:
			sql = "SELECT velages.date FROM velages LEFT JOIN animaux a ON velages.mere_id = a.id LEFT JOIN familles f ON a.famille_id = f.id"
			sql += args

		case ChartType.BREED:
			sql = "SELECT type, COUNT(animal_id) FROM animaux_types LEFT JOIN types t on animaux_types.type_id = t.id"
			sql += f"{args} GROUP BY type"

		case ChartType.PASTURE:
			sql = "SELECT type, COUNT(animal_id) FROM animaux_types LEFT JOIN types t on animaux_types.type_id = t.id LEFT JOIN animaux a on a.id = animaux_types.animal_id WHERE presence = 1 GROUP BY type"

	return sql

# Based of a script by Sean B. Palmer (inamidst.com)
# Source: https://gist.github.com/miklb/ed145757971096565723

def is_full_moon(time: str) -> bool:
	"""
	Checks if a date is during a full moon period

	Args:
		- time (str): Date to check

	Returns:
		- bool: True if full moon period, False otherwise
	"""

	year, month, day = time.split("-")
	dec = decimal.Decimal

	diff = datetime.datetime(int(year), int(month), int(day)) - datetime.datetime(2001, 1, 1)
	days = dec(diff.days) + dec(diff.seconds) / dec(86400)
	lunations = dec("0.20439731") + days * dec("0.03386319269")

	index = lunations % dec(1) * dec(8) + dec("0.5")
	index = math.floor(index)

	return int(index) & 7 == 4
