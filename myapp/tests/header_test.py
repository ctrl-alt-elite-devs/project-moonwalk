# test checkout form validation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
import time


# launch Firefox browser
driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))
# load home page
driver.get('http://localhost:8000/')
# give time for browser to open
time.sleep(5)

def header_button():
    try:
        # test Home button
        home_button = driver.find_element(By.LINK_TEXT, "Home")
        home_button.click()
        time.sleep(2)
        
        expected_url = "http://localhost:8000/"  # home page URL
        current_url = driver.current_url # get the URL of current page displayed
        
        if current_url == expected_url:
            print("✅ Successfully navigated to the Home page.")
        else:
            print(f"❌ Failed to navigate to the Home page. Current URL: {current_url}")
        
        # test to see if the moonwalk threads logo is visible
        try:
            mwt_logo = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "brand-logo"))
            )
            print("✅ Moonwalk Threads logo is visible on Home Page.")
        except Exception as e:
            print(f"❌ Moonwalk Threads logo is NOT visible on Home Page.")
            
        mwt_logo.click()
        time.sleep(2)
        
        expected_url = "http://localhost:8000/"  # home page URL
        current_url = driver.current_url # get the URL of current page displayed
        
        if current_url == expected_url:
            print("✅ Successfully navigated to the Home page via Moonwalk Threads logo.")
        else:
            print(f"❌ Failed to navigate to the Home page via Moonwalk Threads logo. Current URL: {current_url}")

        # test Shop page
        shop_button = driver.find_element(By.LINK_TEXT, "Shop")
        shop_button.click()
        time.sleep(2)
        
        expected_url = "http://localhost:8000/shop/"  # shop page URL
        current_url = driver.current_url # get the URL of current page displayed
        
        if current_url == expected_url:
            print("✅ Successfully navigated to the Shop page.")
        else:
            print(f"❌ Failed to navigate to the Shop page. Current URL: {current_url}")
        
        # test to see if the moonwalk threads logo is visible
        try:
            mwt_logo = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "brand-logo"))
            )
            print("✅ Moonwalk Threads logo is visible on Home Page.")
        except Exception as e:
            print(f"❌ Moonwalk Threads logo is NOT visible on Home Page.")
            
        mwt_logo.click()
        time.sleep(2)
        
        expected_url = "http://localhost:8000/"  # home page URL
        current_url = driver.current_url # get the URL of current page displayed
        
        if current_url == expected_url:
            print("✅ Successfully navigated to the Home page via Moonwalk Threads logo.")
        else:
            print(f"❌ Failed to navigate to the Home page via Moonwalk Threads logo. Current URL: {current_url}")
            
        # test About page
        about_button = driver.find_element(By.LINK_TEXT, "About")
        about_button.click()
        time.sleep(2)
        
        expected_url = "http://localhost:8000/about/"  # about page URL
        current_url = driver.current_url # get the URL of current page displayed
        
        if current_url == expected_url:
            print("✅ Successfully navigated to the About page.")
        else:
            print(f"❌ Failed to navigate to the About page. Current URL: {current_url}")
        
        # test to see if the moonwalk threads logo is visible
        try:
            mwt_logo = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "brand-logo"))
            )
            print("✅ Moonwalk Threads logo is visible on Home Page.")
        except Exception as e:
            print(f"❌ Moonwalk Threads logo is NOT visible on Home Page.")
            
        mwt_logo.click()
        time.sleep(2)
        
        expected_url = "http://localhost:8000/"  # home page URL
        current_url = driver.current_url # get the URL of current page displayed
        
        if current_url == expected_url:
            print("✅ Successfully navigated to the Home page via Moonwalk Threads logo.")
        else:
            print(f"❌ Failed to navigate to the Home page via Moonwalk Threads logo. Current URL: {current_url}")

        # test Contact page
        contact_button = driver.find_element(By.LINK_TEXT, "Contact")
        contact_button.click()
        time.sleep(2)
        
        expected_url = "http://localhost:8000/contact/"  # contact page URL
        current_url = driver.current_url # get the URL of current page displayed
        
        if current_url == expected_url:
            print("✅ Successfully navigated to the Contact page.")
        else:
            print(f"❌ Failed to navigate to the Contact page. Current URL: {current_url}")
        
        # test to see if the moonwalk threads logo is visible
        try:
            mwt_logo = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "brand-logo"))
            )
            print("✅ Moonwalk Threads logo is visible on Home Page.")
        except Exception as e:
            print(f"❌ Moonwalk Threads logo is NOT visible on Home Page.")
            
        mwt_logo.click()
        time.sleep(2)
        
        expected_url = "http://localhost:8000/"  # home page URL
        current_url = driver.current_url # get the URL of current page displayed
        
        if current_url == expected_url:
            print("✅ Successfully navigated to the Home page via Moonwalk Threads logo.")
        else:
            print(f"❌ Failed to navigate to the Home page via Moonwalk Threads logo. Current URL: {current_url}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        
if __name__ == "__main__":
    header_button()
    driver.quit()