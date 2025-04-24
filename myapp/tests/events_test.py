from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import re

# Setup Chrome browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("http://localhost:8000/")
time.sleep(2)

input("✅ Loaded homepage. Press Enter to continue...")

event_boxes = driver.find_elements(By.CLASS_NAME, "event-box")

# Check number of events
if event_boxes:
    print(f"✅ {len(event_boxes)} event(s) found on the landing page.")
else:
    print("❌ No events found.")
input("Press Enter to continue...")

# Verify image presence
all_have_images = True
for i, event in enumerate(event_boxes):
    image_tags = event.find_elements(By.TAG_NAME, "img")
    if not image_tags:
        print(f"❌ Event {i + 1} does not have an image.")
        all_have_images = False
    else:
        print(f"✅ Event {i + 1} has an image.")
input("Press Enter to continue...")

# Parse and verify event dates
all_dates_valid = True
event_dates = []

for index, event in enumerate(event_boxes):
    try:
        desc_html = event.find_element(By.CLASS_NAME, "event-description").get_attribute("innerHTML")
        match = re.search(r"<strong>Date:</strong>\s*([^<]+)", desc_html)
        if match:
            date_str = match.group(1).strip()
            date_obj = datetime.strptime(date_str, "%a %b %d %Y")
            event_dates.append(date_obj)

            today = datetime.now().date()
            if date_obj.date() < today:
                print(f"❌ Event {index + 1} is in the past: {date_obj.date()}")
                all_dates_valid = False
            else:
                print(f"✅ Event {index + 1} is today or upcoming: {date_obj.date()}")
        else:
            raise Exception("Date not found in description.")
    except Exception as e:
        print(f"❌ Could not parse date for Event {index + 1}: {e}")
        all_dates_valid = False

input("Press Enter to continue...")

# Check date order
if event_dates == sorted(event_dates):
    print("✅ Events are in correct chronological order.")
else:
    print("❌ Events are not in the correct order (earliest should be first).")

# Ensure max 4 events are shown
if len(event_boxes) > 4:
    print(f"❌ Too many events shown: {len(event_boxes)} (expected 4 max).")
else:
    print(f"✅ Event count valid: {len(event_boxes)} (expected ≤ 4).")

input("Press Enter to continue...")

# Test the "View More" button functionality
try:
    # Wait until the button is clickable
    view_more_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "viewmore_button"))
    )
    view_more_button.click()
    time.sleep(2)

    current_url = driver.current_url
    if current_url.lower().endswith("/googlecalendar/"):
        print("✅ 'View More' button successfully navigated to the Google Calendar events page.")
    else:
        print(f"❌ 'View More' button did not navigate correctly. Current URL: {current_url}")
except Exception as e:
    print(f"❌ Error testing 'View More' button: {e}")
    
input("Press Enter to continue...")

# Test the "Back" button functionality
try:
    # Wait until the Back link is clickable
    back_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Back"))
    )
    back_link.click()
    time.sleep(2)

    # Verify navigation back to the homepage
    current_url = driver.current_url
    if current_url.rstrip('/') == "http://localhost:8000":
        print("✅ 'Back' button successfully returned to the homepage.")
    else:
        print(f"❌ 'Back' button did not navigate to homepage. Current URL: {current_url}")
except Exception as e:
    print(f"❌ Error testing 'Back' button: {e}")

input("Press Enter to finish...")
driver.quit()
