from wrapper import Game
from model import Model
from color import get_heal
from time import sleep
from math import atan, pi
import datetime
import threading

directory = "/home/howardp/Documents/Code/moomoo"
g = Game("fatty", directory)
m = {
		"tree": Model("tree_res_s", directory),
		"food": Model("food", directory)
		}


def explore(r):
	stop_time = 1
	axis = 0
	pts = m[r].scan(str(g.screenshot()))
	flag = False
	while not pts:
		segment = round(stop_time / 2)
		for i in range(segment):
			g.move(axis)
			sleep(2)
			g.stop()
			pts = m[r].scan(str(g.screenshot()))
			if pts:
				flag = True
				break
		if flag:
			break
		stop_time *= 2
		axis += -6 if axis == 6 else 2
		pts = m[r].scan(str(g.screenshot()))


def auto(r):
	# r = resource r = command[1]
	screenshot_id = g.screenshot()
	pts = m[r].scan(str(screenshot_id))
	if len(pts) == 0:
		return
	# we don't want the point to be the upper left corner but to be in relative center
	pt = (pts[0][0] + (m[r].w / 2), pts[0][1] + (m[r].h / 2))
	origin = (g.width / 2, g.height / 2)
	axis = get_axis(pt, origin)
	r_initial = g.get_tree() if r == "tree" else (g.get_food() if r == "food" else g.get_stone())
	resource = r_initial
	g.move(axis)
	g.set_axis(axis)
	time = int(datetime.datetime.now().strftime("%s"))
	while resource == r_initial and int(datetime.datetime.now().strftime("%s")) - time < 2:
		resource = g.get_tree() if r == "tree" else (g.get_food() if r == "food" else g.get_stone())
	g.stop()


def get_axis(pt, origin):
	# We need to adjust pt such that the origin is not the top left corner but the center of the page
	adj_pt = (pt[0] - origin[0], origin[1] - pt[1])
	# Now we need to find what axial quadrant the point is located in (1..8)
	# 360 / 8 = 45 deg per quadrant, shifted (45 / 2) deg down so the sector pads the radius
	# First the quadrant:
	if adj_pt[0] > 0:
		if adj_pt[1] > 0:
			quad = 1
		else:
			quad = 4
	else:
		if adj_pt[1] > 0:
			quad = 2
		else:
			quad = 3
	# atan will give us more than one possibility, first adjust to first quadrant
	adj2_pt = (abs(adj_pt[0]), abs(adj_pt[1]))
	theta = atan(adj2_pt[1] / adj2_pt[0]) * (180 / pi)

	# Now adjust back to original quadrant
	adj_theta = theta
	if quad == 3:
		adj_theta = 180 + theta
	elif quad == 2 or quad == 4:
		adj_theta = (quad * 90) - theta

	# Now match to axial quadrant
	if (adj_theta < 360 and adj_theta >= (360 - 22.5)) or (adj_theta > 0 and adj_theta < 22.5):
		return 0
	a = 22.5
	b = a + 45
	for i in range(7):
		if adj_theta <= b and adj_theta > a:
			return i + 1
		a += 45
		b += 45


def naive_algo():
	def f():
		while True:
			if g.get_food() >= 10 and get_heal("{}/screenshots/{}.png".format(directory, str(g.screenshot()))):
				print("Healing...")
				g.heal()
	

	def upgrade():
		age_2 = False
		age_3 = False
		while True:
			age = g.get_age()
			if age == 2 and not age_2:
				age_2 = True
				g.upgrade("8")
			elif age == 3 and not age_3:
				age_3 = True
				g.upgrade("17")
			elif age == 4:
				break
			sleep(1)


	t = threading.Thread(target=f)
	t2 = threading.Thread(target=upgrade)
	t.start()
	t2.start()
	food_init = g.get_food()
	tree_init = g.get_tree()
	while True:
		food = g.get_food()
		tree = g.get_tree()
		if food < 500 and (food > food_init or tree > tree_init):
			food_init = food
			tree_init = tree
			sleep(1)
			continue
		if food < 500 and food <= food_init:
			food_init = g.get_food()
			print("Exploring food")
			explore("food")
			print("Food found")
			auto("food")
		elif tree == tree_init:
			tree_init = g.get_tree()
			print("Exploring tree")
			explore("tree")
			print("Tree found")
			auto("tree")


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
	elif command[0] =="heal":
		g.heal()
	elif command[0] == "auto":
		auto(command[1])
	elif command[0] == "explore":
		explore(command[1])
	elif command[0] == "algo":
		naive_algo()

