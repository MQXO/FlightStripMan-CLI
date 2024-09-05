#COLORS#
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m' # orange on some systems
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
LIGHT_GRAY = '\033[37m'
DARK_GRAY = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m' # called to return to standard terminal text color

import random as r
import re 
import time 
import sys
from rich.table import Table # type: ignore
from rich.console import Console # type: ignore
from rich.markdown import Markdown # type: ignore
err = "That's not quite right, try again. "

def reset():
	global acft
	acft = {
	"No.": "",
	"Callsign": "",
	"Class": "",
	"Altitude": "",
	"Speed": "",
	"Squawk": ""
 }

def refresh():
	console = Console()
	md = Markdown(INFO)
	console.print(md)
	console.print(table) 

def gen_squawk(prefix):
	if len(prefix) < 4:
		newsqk = ""
		for i in range(4 - len(re.findall(r'\d', prefix))):
			newsqk = newsqk+str(r.randint(0,7))
		return(prefix+newsqk)


def acq_prefix():
	while True:
		global prefix
		prefix = input("Set a squawk prefix (2 digits): ")
		pattern = re.compile("[8-9]|\D+")
		if not pattern.findall(prefix):
			if len(prefix) == 2:
				return
			else:
				print(err+"You need 2 digits exactly.")
		else:
			print(err+"You can't use the numbers 8 or 9, or use letters.")

def init():
	global table
	global num
	global prefix
	global rows
	global active
	active = []
	prefix = ""
	num = 0
	table = Table(title="Aircraft", expand=True)
	rows = []
	reset()
	for k in acft.keys():
		table.add_column(k)

def newacft():
### Needs to reset the acft dict, allow input to keypair for acft thingimies and then insert that into the table
	reset()
	global num
	global rows
	rows = []
	for k in acft.keys():
		if k == "No.":
			acft[k] = str(num+1)
			num = num+1
		elif k == "Squawk":
			if prefix:
				continue
			else:
				acq_prefix()
			resp = input("Press enter for automatic squawk or type a squawk to manually enter.\n")
			if not resp:
				acft[k] = gen_squawk(prefix)
		else:
			acft[k] = input(f"{k}:")
	for k in acft.keys():
		rows.append(acft.get(k))
		print(f"rows={rows}")
	active.append(rows)
	print(f"active={active}")
	for i in active:
		print(f"i={i}")
		print(f"i[0]={i[0]}")
		print(num)
		if str(i[0]) == str(num):
			table.add_row(*rows)
	refresh()

def remacft():
	ac = input("Input the queue number of the aircraft you wish to delete.")




INFO = """
# FlightStripManager CLI

**A few important keybinds\n**
*Type the number in the command line to activate*says

"""

init()
newacft()

while True:
	ins = input()
	try:
		menu = int(ins)
	except:
		print(err+"That's not a number.")
	if menu == 1:
		newacft()
	elif menu == 2:
		break
	elif menu == 3:
		break
	elif menu == 4:
		acq_prefix()