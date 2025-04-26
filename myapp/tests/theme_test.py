from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import unittest
from time import sleep

driver = webdriver.Chrome()
a = ActionChains(driver)
driver.get("http://localhost:8000/edit-theme")

date_picker = driver.find_element(by=By.ID, value="date-drop")
date_picker.click()

date_picker.send_keys(Keys.LEFT, Keys.LEFT)
date_picker.send_keys("04302025")

color_picker = driver.find_element(by=By.ID, value="color_banner")
color_picker.click()
a.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.UP, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, "432077", Keys.ENTER)
a.perform()


img00_picker = driver.find_element(By.ID, value="img00")
img00_picker.send_keys("C:\\Users\\Valiant\\Pictures\\Saved Pictures\\WeepingRockZion.jpg")
img01_picker = driver.find_element(By.ID, value="img01")
img01_picker.send_keys("C:\\Users\\Valiant\\Pictures\\Saved Pictures\\WeepingRockZion.jpg")
img02_picker = driver.find_element(By.ID, value="img02")
img02_picker.send_keys("C:\\Users\\Valiant\\Pictures\\Saved Pictures\\WeepingRockZion.jpg")


font_picker = driver.find_element(By.ID, value="Modern Prestige Demo")
font_picker.click()

title_picker = driver.find_element(By.ID, value="title")
title_picker.click()
title_picker.send_keys("This is for the testing")

font_color_picker = driver.find_element(By.ID, value="color_font")
font_color_picker.click()
a.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.UP, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, "784013", Keys.ENTER)
a.perform()

font_weight_picker = driver.find_element(By.ID, value="bold")
font_weight_picker.click()

font_border_thickness = driver.find_element(By.ID, value="border")
font_border_thickness.click()
a.send_keys(Keys.RIGHT, Keys.RIGHT, Keys.RIGHT, Keys.RIGHT, Keys.RIGHT, Keys.RIGHT)
a.perform()

font_border_color = driver.find_element(By.ID, value="color_border")
font_border_color.click()
a.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.UP, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, "508943", Keys.ENTER)
a.perform()

submit_button = driver.find_element(By.ID, value="done")
submit_button.click()
sleep(10)

driver.get("http://localhost:8000")

assert "This is for the testing" in driver.find_element(By.ID, value="drop_title").text
print("Style successfuly changed and updated")


sleep(10)

