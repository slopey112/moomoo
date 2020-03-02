from wrapper import Game
from model import Model
from time import sleep

g = Game("fatty")
m = Model("tree")
while True:
    inn = input()
    i = g.screenshot()
    print(m.scan(str(i)))
