import os
from PIL import Image
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

#Start selenium service and chromedriver
service = Service()
driver = webdriver.Chrome(service=service)

#create a temp image to be used for testing product additions
image_path = os.path.join(os.getcwd(), "temp_test_image.jpg")
img = Image.new("RGB", (100, 100), color="blue")
img.save(image_path)

image_path2 = os.path.join(os.getcwd(), "edit_test_image.jpg")
img2 = Image.new("RGB", (100, 100), color="red")
img2.save(image_path2)
try:
    #Login to admin page
    driver.get('http://localhost:8000/admin/')
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("test123")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    sleep(2)

    #Fill in test item values
    driver.find_element(By.LINK_TEXT, "Products").click()
    sleep(2)
    driver.find_element(By.LINK_TEXT, "ADD PRODUCT").click()
    sleep(2)
    driver.find_element(By.NAME, "name").send_keys("Test Item")
    driver.find_element(By.NAME, "price").clear()
    driver.find_element(By.NAME, "price").send_keys("9.99")
    driver.find_element(By.NAME, "size").send_keys("Medium")
    driver.find_element(By.NAME, "image").send_keys(image_path)
    driver.find_element(By.NAME, "quantity").clear()
    driver.find_element(By.NAME, "quantity").send_keys("1")
    assert driver.find_element(By.NAME, "quantity").get_attribute("value") == "1"
    driver.find_element(By.NAME, "_save").click()
    sleep(2)

    #Verify products in database by navigating to shop page
    driver.get('http://localhost:8000/shop/')
    assert "Test Item" in driver.find_element(By.TAG_NAME, "body").text
    assert "9.99" in driver.find_element(By.TAG_NAME, "body").text
    assert "Medium" in driver.find_element(By.TAG_NAME, "body").text
    print("Product found on shop page!")
    sleep(3)

    #Testing editing fields in a product
    driver.get('http://localhost:8000/admin/')
    driver.find_element(By.LINK_TEXT, "Products").click()
    sleep(2)
    driver.find_element(By.LINK_TEXT, "Test Item").click()
    sleep(2)
    driver.find_element(By.NAME, "name").clear()
    driver.find_element(By.NAME, "name").send_keys("Edited Item")
    driver.find_element(By.NAME, "price").clear()
    driver.find_element(By.NAME, "price").send_keys("7.77")
    driver.find_element(By.NAME, "size").clear()
    driver.find_element(By.NAME, "size").send_keys("Large")
    driver.find_element(By.NAME, "image").send_keys(image_path2)
    driver.find_element(By.NAME, "_save").click()
    sleep(2)

    driver.get('http://localhost:8000/shop/')
    assert "Edited Item" in driver.find_element(By.TAG_NAME, "body").text
    assert "7.77" in driver.find_element(By.TAG_NAME, "body").text
    assert "Large" in driver.find_element(By.TAG_NAME, "body").text
    print("Item edited successfully!")
    sleep(3)

    #Removing item
    driver.get('http://localhost:8000/admin/')
    driver.find_element(By.LINK_TEXT, "Products").click()
    sleep(1)
    driver.find_element(By.LINK_TEXT, "Edited Item").click()
    sleep(1)
    driver.find_element(By.CLASS_NAME, "deletelink").click()
    sleep(1)
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    sleep(1)

    #Verify item was removed from database by navigating to shop
    driver.get('http://localhost:8000/shop/')
    assert "Edited Item" not in driver.find_element(By.TAG_NAME, "body").text
    print("Product removed from shop page!")
    sleep(2)

finally:
    if os.path.exists(image_path):
        os.remove(image_path)
        os.remove(image_path2)
    sleep(2)
    driver.quit()