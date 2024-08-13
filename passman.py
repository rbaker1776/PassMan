from rich import print
from rich.console import Console
from database import showAllEntries
from config import configure

VERSION = 1.0

def printHelpMessage(arg=''):
	if arg == '':
		print(''.join('=' for _ in range(120)))
		print(f"Passman {VERSION} by Ryan Baker")
		print()
		print("Commands:")
		print("\t[magenta](c)onfig[/magenta]: configure the database, needs to be done once upon setup (type 'help config' for usage")
		print("\t[magenta](s)how[/magenta]: show all entries currently in the database")
		print("\t[magenta](a)dd[/magenta]: add an entry to the database (type 'help add' for usage information)")
		print("\t[magenta](d)elete[/magenta]: delete an entry from the database (type 'help delete' for usage information)")
		print("\t[magenta](q)uit[/magenta]: quit Passman")
		print(''.join('=' for _ in range(120)))
	elif arg == "add":
		print

def main():
	while True:
		user_input = input().strip().split()
		command = user_input[0]
		if len(user_input) > 1:
			args = user_input[1:]
		else:
			args = ['']

		if command == "quit" or command == 'q':
			break
		elif command == "help" or command == 'h':
			printHelpMessage(args[0])
		elif command == "config" or command == 'c':
			configure(args[0])
		elif command == "show" or command == 's':
			showAllEntries()
		elif command == "add" or command == 'a':
			pass
		elif command == "delete" or command == 'd':
			pass
		else:
			print("Unknown command. Try 'help' for valid commands.")

if __name__ == "__main__":
	main()
