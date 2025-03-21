# This tests the advanced search functionality in Firefox.
import sys, getopt
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

# check search page
driver.get('localhost:8000')
driver.find_element(by=By.ID, value='emailAddress').send_keys('nazapot@gmail.com' + Keys.ENTER)
#wait.pause(opts)

'''driver.find_element(by=By.NAME, value='emailAddress').clear()
driver.find_element(by=By.NAME, value='emailAddress').send_keys('Sacramento' + Keys.ENTER)
wait.pause(opts)

driver.find_element(by=By.NAME, value='emailAddress').clear()
driver.find_element(by=By.NAME, value='emailAddress').send_keys('tina delgado' + Keys.ENTER)
wait.pause(opts)

driver.find_element(by=By.NAME, value='emailAddress').clear()
driver.find_element(by=By.NAME, value='emailAddress').send_keys('' + Keys.ENTER)
wait.pause(opts)'''

driver.quit()