import sys, os, csv

from msedge.selenium_tools import Edge, EdgeOptions

from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

def exit():
	print()
	print()

	input("Press enter...")
	driver.quit()

def getProfile():
	if os.name == "nt":
		return "C:\\Users\\" + os.getlogin() + "\\SeleniumProfile"
	elif os.name == "posix":
		return "/home/" + os.getlogin() + "/SeleniumProfile"
	else:
		raise Exception("WHAT SYSTEM ARE YOU USING?!")

def check():
	if sys.version_info[0] < 3:
		raise Exception("You must use Python 3.4 or higher.")
	elif sys.version_info[1] <  4:
		raise Exception("You must use Python 3.4 or higher.")

if __name__ == "__main__":
	check()
	
	edgeOptions = EdgeOptions()
	edgeOptions.use_chromium = True
	edgeOptions.add_argument("user-data-dir=" + getProfile())
	edgeOptions.add_argument("disable-extensions")
	edgeOptions.add_argument("disable-gpu")
	edgeOptions.add_argument("headless")
	
	driver = Edge(options=edgeOptions)
	#driver.implicitly_wait(10)

	try:
		driver.get("https://google.com")

		#TODO: YOUR CODE HERE

	except NoSuchElementException as e:
		print("ERROR: Something went wrong!")
		print(e)
	
	finally:
		exit()
