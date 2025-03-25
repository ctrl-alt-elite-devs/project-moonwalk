# This tests the advanced search functionality in Firefox.
import sys, getopt
import time

import wait
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service


opts, args = getopt.getopt(sys.argv[1:], "d", ["debug"])

print("Running test " + sys.argv[0])

# launch
driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))

# go to shop page
driver.get('localhost:8000')
driver.find_element(by=By.LINK_TEXT, value='Shop').click()

#filter shirts
sleep(1)
driver.find_element(By.NAME, "Filter").click()
driver.find_element(By.LINK_TEXT, "Shirts").click()
print("filtered to shirts")
input("Press input to continue...")

#filter pants
driver.find_element(By.NAME, "Filter").click()
driver.find_element(By.LINK_TEXT, "Pants").click()
print("filtered to pants")
input("Press input to continue...")

#filter hats
driver.find_element(By.NAME, "Filter").click()
driver.find_element(By.LINK_TEXT, "Hats").click()
print("filtered to hats")
input("Press input to continue...")

driver.quit()
