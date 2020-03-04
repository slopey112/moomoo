from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from subprocess import run

class Game:
	screenshot_id = 0
	directory = ""

	def __init__(self, name, directory):
		# Instantiate variables
		self.name = name
		self.driver = webdriver.Firefox()
		self.height = self.driver.get_window_size()["height"]
		self.width = self.driver.get_window_size()["width"]
		Game.directory = directory

		# Instantiate game
		self.driver.get("https://www.moomoo.io")
		self.driver.find_element_by_css_selector("#consentWindow>div>div:nth-child(2)").click()
		sleep(3)
		self.driver.find_element_by_id("nameInput").send_keys(name)
		self.driver.find_element_by_id("enterGame").click()
		ActionChains(self.driver).key_down("e").perform()
	

	def set_axis(self, axis):
		ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("actionBar")).perform()
		x = 0
		y = 0
		
		# Axis 0 == 0 deg, axis 1 = 45 deg, axis 2 = 90 deg, etc.
		if axis == 0:
			x = self.width / 4
			y = - self.height / 2 + 70
		elif axis == 4:
			x = - self.width / 4
			y = - self.height / 2 + 70
		elif axis == 2:
			x = 0
			y = - self.height / 2
		elif axis == 6:
			pass
		elif axis == 1:
			x = self.width / 3 
			y = - 3 * self.height / 4
		elif axis == 3:
			x = - self.width / 3
			y = - 3 * self.height / 4
		elif axis == 5:
			x = - self.width / 3
			y = 0
		elif axis == 7:
			x = self.width / 3
			y = 0
		
		ActionChains(self.driver).move_by_offset(x, y).perform()


	def move(self, axis):
		actions = []
		if axis == 0:
			actions.append(Keys.RIGHT)
		elif axis == 2:
			actions.append(Keys.UP)
		elif axis == 4:
			actions.append(Keys.LEFT)
		elif axis == 6:
			actions.append(Keys.DOWN)
		elif axis == 1:
			actions.append(Keys.RIGHT)
			actions.append(Keys.UP)
		elif axis == 3:
			actions.append(Keys.UP)
			actions.append(Keys.LEFT)
		elif axis == 5:
			actions.append(Keys.LEFT)
			actions.append(Keys.DOWN)
		elif axis == 7:
			actions.append(Keys.DOWN)
			actions.append(Keys.RIGHT)
	
		for action in actions:
			ActionChains(self.driver).key_down(action).perform()


	def screenshot(self):
		Game.screenshot_id += 1
		self.driver.save_screenshot("{}/screenshots/{}.png".format(Game.directory, Game.screenshot_id))
		return Game.screenshot_id


	def stop(self):
		for i in [Keys.UP, Keys.RIGHT, Keys.DOWN, Keys.LEFT]:
			ActionChains(self.driver).key_up(i).perform()

	
	def close(self):
		self.driver.close()
	

	def get_food(self):
		return int(self.driver.find_element_by_id("foodDisplay").text)


	def get_tree(self):
		return int(self.driver.find_element_by_id("woodDisplay").text)


	def get_stone(self):
		return int(self.driver.find_element_by_id("stoneDisplay").text)


	def get_score(self):
		return int(self.driver.find_element_by_id("scoreDisplay").text)
	

	def heal(self):
		ActionChains(self.driver).send_keys(["q", Keys.SPACE]).send_keys("1").perform()


def main():
	g = Game("fatty")
	for i in range(8):
		g.move(i)
		sleep(3)
		g.stop()
	g.close()


if __name__ == "__main__":
	main()
