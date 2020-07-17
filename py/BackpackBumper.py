from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os

#########################
######## FILL IN ########
#########################
STEAM_ID64 = ""
#########################
#########################

def getProfile():
	if os.name == "nt":
		return "C:\\Users\\" + os.getlogin() + "\\chromeSeleniumProfile"
	elif os.name == "posix":
		return "/home/" + os.getlogin() + "/chromeSeleniumProfile"
	else:
		raise Exception("WHAT SYSTEM ARE YOU USING?!")

def saveFile(name, content):
	file = open(name, "w", encoding="utf-8")
	file.write(content)
	file.close()

def exit():
	print()
	input("Press enter to exit...")

if __name__ == "__main__":
	chromeOptions = webdriver.ChromeOptions()
	chromeOptions.add_argument("--user-data-dir=" + getProfile())
	chromeOptions.add_argument("--disable-extensions")
	chromeOptions.add_argument("--log-level=3")
	chromeOptions.add_argument("--disable-gpu")
	chromeOptions.add_argument("--headless")

	driver = webdriver.Chrome(options=chromeOptions)

	driver.get("https://backpack.tf/classifieds?steamid=" + STEAM_ID64)
	
	pages = driver.find_element_by_css_selector("#page-content > nav:nth-child(5) > ul").find_elements_by_tag_name("li")
	pageCount = len(pages) - 4

	# accept cookies if prompted to
	try:
		driver.find_element_by_css_selector("body > div.app_gdpr--2k2uB > div > div.intro_intro--Ntqks > div > div.intro_options--gTc-i > button.button_button--lgX0P.intro_acceptAll--23PPA").click()
	except NoSuchElementException:
		# nothing to do if we don't have to accept cookies
		pass

	for i in range(1, pageCount + 1):
		driver.get("https://backpack.tf/classifieds?page=" + str(i) + "&steamid=" + STEAM_ID64)

		print("[INFO]: " + "classifieds page #" + str(i))

		bpUl = driver.find_element_by_css_selector("#page-content > div:nth-child(4) > div:nth-child(1) > div > div.panel-body.padded > ul").find_elements_by_tag_name("li")

		for li in bpUl:
			id = li.get_attribute("id")

			try:
				bump = driver.find_element_by_css_selector("#" + id + " > div.listing-body > div.listing-header > div.listing-buttons > a.btn.btn-xs.btn-bottom.btn-default.listing-relist.listing-bump")
				webdriver.ActionChains(driver).context_click(bump).perform() # right-click

				print("[INFO]: " + id + " BUMPED")
			except NoSuchElementException:
				#already bumped
				print("[WARNING]: " + "cannot bump " + id + " (already bumped?)")

	#saveFile("bp.html", driver.page_source)
	#driver.get_screenshot_as_file('bp.png')

	driver.quit()
	exit()
