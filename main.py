from wrapper import Game
from model import Model
from time import sleep

g = Game("fatty")
m = Model("tree_res")
while True:
	command = input().split()
	if command[0] == "screenshot":
		i = g.screenshot()
		print(m.scan(str(i)))
	elif command[0] == "move":
		g.move(int(command[1]))
	elif command[0] == "stop":
		g.stop()
	elif command[0] == "axis":
		g.set_axis(int(command[1]))
	elif command[0] == "close":
		g.close()
		break
	elif command[0] == "auto":
		while True:
			screenshot_id = g.screenshot()
			pts = m.scan(str(i))
			
