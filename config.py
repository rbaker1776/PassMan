import sys
from getpass import getpass
from rich import print
from rich.console import Console
import mysql.connector
from crypto import hashMasterPassword, generatePassword

console = Console()

def dbConfig():
	try:
		db = mysql.connector.connect(
			host = "localhost",
			user = "root",
			password = getpass("Please input MySQL credentials: "),
		)
		# print("[green][!][/green] Successfully connected to database")
	except Exception as e:
		print("[red][!][/red] Could not connect to the database")
		console.print_exception(slow_locals=True)
	return db

def checkConfig() -> bool:
	db = dbConfig()
	cursor = db.cursor()
	query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'pm'"
	cursor.execute(query)
	results = cursor.fetchall()
	db.close()
	return len(results) != 0

def make():
	if checkConfig():
		print("[red][!][/red] Already configured")
		return
	else:
		print("[green][+][/green] Creating new configuration")

	db = dbConfig()
	cursor = db.cursor()

	try:
		cursor.execute("CREATE DATABASE pm")
	except Exception as e:
		print("[red][!][/red] An error occured while creating the database. Check is database 'pm' already exists.")
		console.print_exception(show_locals=True)
		sys.exit(0)
	print("[green][+][/green] Database 'pm' created")

	try:
		query = "CREATE TABLE pm.secrets (masterkey TEXT NOT NULL, devicekey TEXT NOT NULL)"
		result = cursor.execute(query)
	except Exception as e:
		print("[red][!][/red] An error occured while creating the 'secrets' table.")
		console.print_exception(show_locals=True)
		sys.exit(0)
	print("[green][+][/green] Table 'secrets' created")

	try:
		query = "CREATE TABLE pm.entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
		result = cursor.execute(query)
	except Exception as e:
		print("[red][!][/red] An error occured while creating the 'entries' table.")
		console.print_exception(show_locals=True)
		sys.exit(0)
	print("[green][+][/green] Table 'entries' created ")

	masterkey = ""
	while True:
		masterkey = getpass("Choose a master password: ")
		if masterkey == getpass("Confirm your master password:") and masterkey != "":
			break
		print("[yellow][-][/yellow] Please try again. Make sure passwords match")

	devicekey = generatePassword(length=16)
	print("[green][+][/green] Successfully generated device secret")

	masterkey = hashMasterPassword(masterkey, devicekey)
	print("[green][+][/green] Successfully hashed master password")

	query = "INSERT INTO pm.secrets (masterkey, devicekey) values (%s, %s)"
	value = (masterkey, devicekey)
	cursor.execute(query, value)
	db.commit()

	print("[green][+][/green] Completed configuration")
	db.close()

def delete():
	print("[red][!][/red] Deleting a configuration clears the device secret and all your entries from the database. This means you will lose access to all passwords added to the database. Only do this id you want to 'destroy' all entries. This action cannot be undone.")
	while True:
		op = input("Are you sure you want to continue? (y/n): ")
		if op.upper() == 'Y':
			break
		if op.upper() == 'N' or op.upper() == '':
			print("[red][!][/red] Deletion canceled")
			sys.exit(0)
		else:
			continue

	db = dbConfig()
	cursor = db.cursor()

	if not checkConfig():
		print("[yellow][-][/yellow] No configuration exists to delete")
		return

	cursor.execute("SELECT masterkey FROM pm.secrets")
	masterkey = cursor.fetchall()[0][0]

	cursor.execute("SELECT devicekey FROM pm.secrets")
	devicekey = cursor.fetchall()[0][0]
	
	if hashMasterPassword(getpass("Please enter master password: "), devicekey) != masterkey:
		print("[red][!][/red] Incorrect master password")
		return

	query = "DROP DATABASE pm"
	cursor.execute(query)
	db.commit()
	db.close()

	print("[green][+][/green] Deleted configuration")

def remake():
	print("[green][+][/green] Remaking configuration")
	delete()
	make()

def configure(arg=""):
	if arg == "make":
		make()
	elif arg == "delete":
		delete()
	elif arg == "remake":
		remake()
	else:
		print("Usage: (c)onfig <make/delete/remake>")

def main():
	if len(sys.argv) != 2:
		print("Usage: python build.py <make/delete/remake>")
		sys.exit(0)
	if sys.argv[1] == "make":
		make()
	elif sys.argv[1] == "delete":
		delete()
	elif sys.argv[1] == "remake":
		remake()
	else:
		print("Usage: python build.py <make/delete/remake>")

if __name__ == "__main__":
	main()	
