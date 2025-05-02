from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
import time

# Launch browser
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
base_url = "http://localhost:8000"

# Helper to check if page contains 404 error or DoesNotExist
def is_404_page():
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        return "404" in driver.title or "DoesNotExist" in driver.title.lower() or "not found" in driver.page_source.lower()
    except TimeoutException:
        return False
# Test accessing existent page and item
def test_direct_link():
    print("\nRunning: direct link")
    driver.get(f"{base_url}/about/")
    time.sleep(4)
    if is_404_page():
        print("❌ 404 page shown for direct link")
    else:
        print("✅ Direct URL correctly shown ")

    print("\nRunning: direct shopping link")
    driver.get(f"{base_url}/product/20/")
    time.sleep(2)
    if is_404_page():
        print("❌ 404 page shown for direct link")
    else:
        print("✅ Direct shopping URL correctly shown ")

# Test accessing non-existent page and missing item
def test_broken_link():
    print("\nRunning: broken link")
    driver.get(f"{base_url}/shopping")
    time.sleep(4)
    if is_404_page():
        print("✅ 404 page correctly shown for broken link")
    else:
        print("❌ 404 page NOT shown for broken link")

    print("\nRunning: missing shopping link")
    driver.get(f"{base_url}/product/200/")
    time.sleep(4)
    if is_404_page():
        print("❌ Does not exist NOT shown for missing item")
    else:
        print("✅ Does not exist shown for missing item")

# Test accessing admin page without login
def test_unauthorized_admin():
    print("\nRunning: unauthorized admin access")
    driver.get(f"{base_url}/admin/socialaccount/socialtoken/")
    time.sleep(4)
    current_url = driver.current_url.lower()
    page_source = driver.page_source.lower()

    if "login" in current_url or "unauthorized" in page_source or "access denied" in page_source:
        print("✅ Admin access blocked for unauthenticated user")
    else:
        print("❌ Admin page was accessible without login")

# Run tests
test_direct_link()
test_broken_link()
test_unauthorized_admin()

# Close browser
driver.quit()