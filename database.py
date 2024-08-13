from config import dbConfig
from rich.table import Table
from rich import print
from rich.console import Console

console = Console()

def showAllEntries():
	db = dbConfig()
	cursor = db.cursor()
	query = "SELECT * FROM pm.entries"
	table = Table()
	cursor.execute(query)

	table.add_column("Site name")
	table.add_column("Site URL")
	table.add_column("Email")
	table.add_column("Username")
	table.add_column("Password")

	results = cursor.fetchall()
	for res in results:
		table.add_row(res[0], res[1], res[2], res[3], "{hidden}")

	console.print(table)

showAllEntries()
