# test checkout form validation
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# launch Firefox browser
driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))

def find_map():
    expected_placeid = "ChIJu4AL434Fm4ARolpKDAJriwU" # Moonwalk threads place id
    try:
        driver.get('http://localhost:8000/contact/') # go to contact page
        time.sleep(10)
        
        map_iframe = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//iframe[contains(@src, 'google.com/maps')]")) #look for the iframe that contains the google map
        )
        print("✅ iframe that contains the Google Map is found and visible.")
        
        # check that the google maps is displaying the correct location using place id to verify
        map_src = map_iframe.get_attribute('src')
        if expected_placeid in map_src:
            print("✅ Google Maps is showing the correct Moonwalk Threads location.")
        else:
            print("❌ Google Maps is NOT showing the correct Moonwalk Threads location.")
            
        #switch into iframe that contains the google map
        driver.switch_to.frame(map_iframe)

        #check if map is loaded inside iframe
        map_loaded = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.gm-style-cc")) # "div.gm-style-cc" is found in Google maps and use this to test if Google Map is loaded
        )
        print("✅ Google Map is displayed inside iframe.")
        

    except Exception as e:
        print(f"❌ Test failed.")

    finally:
        driver.switch_to.default_content()
    
def find_calendar():
    try:
        driver.get('http://localhost:8000/googleCalendar/') # go to calendar page
        time.sleep(10)
        
        calendar_iframe = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//iframe[contains(@src, 'google.com/calendar')]")) #look for the iframe that contains the google calendar
        )
        print("✅ iframe that contains the Google Calendar is found and visible.")

        #switch into iframe that contains the google map
        driver.switch_to.frame(calendar_iframe)

        #check if google calendar is loaded inside iframe
        calendar_loaded = WebDriverWait(driver, 50).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "header.lDz5J")) # check if the calendar header is showing, if yes, means the calendar is showing. 
        )
        print("✅ Google Calendar is displayed inside iframe.")

    except Exception as e:
        print(f"❌ Test failed.")

    finally:
        driver.switch_to.default_content()
    
if __name__ == "__main__":
    print("Google Map Test")
    find_map()
    print("")
    print("Google Calendar Test")
    find_calendar() 
    driver.quit()
