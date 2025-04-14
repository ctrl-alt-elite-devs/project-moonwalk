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

#add an item
driver.find_element(By.NAME, "ADD").click()
print("added product")
input("Press any key to continue...")

#go to cart
driver.find_element(By.CLASS_NAME, "cart-count").click()
print("clicked to cart")
input("Press any key to continue...")

#add and decrease quantity
driver.find_element(By.NAME, "increment").click()
print("incremented")
input("Press any key to continue...")
driver.find_element(By.NAME, "decrement").click()
print("decremented")
input("Press any key to continue...")

#remove item
driver.find_element(By.CLASS_NAME, "remove-btn").click()
print("removed item from cart")
input("Press any key to continue...")

#try checking out with no items
driver.find_element(By.CLASS_NAME, "checkout-button").click()
print("clicked checkout with no items in cart")
input("Press any key to continue...")

#add an item and proceed to checkout
driver.find_element(by=By.LINK_TEXT, value='Shop').click()
driver.find_element(By.NAME, "ADD").click()
driver.find_element(By.CLASS_NAME, "cart-count").click()
print("added item and proceeded to checkout")
input("Press any key to continue...")

driver.quit()