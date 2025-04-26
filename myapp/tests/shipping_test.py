# test address validation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
import time

# launch in Firefox
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
driver.get('http://localhost:8000/checkout/')
time.sleep(3)

# Helper function to submit form and detect if validation error occurred
def submit_form():
    try:
        driver.find_element(By.ID, "submitButton").click()
        WebDriverWait(driver, 3).until(EC.url_changes(driver.current_url))
        return True  # Form submitted successfully
    except TimeoutException:
        return False  # Validation error likely prevented submission

def reset_form():
    driver.refresh()
    time.sleep(2)

# Run test with missing street address
def test_missing_street_address():
    print("\nRunning: test_missing_street_address")
    driver.find_element(By.NAME, "zipCode").send_keys("95630")
    driver.find_element(By.NAME, "city").send_keys("Folsom")
    driver.find_element(By.NAME, "state").send_keys("California")
    driver.find_element(By.NAME, "country").send_keys("United States")
    fill_common_info()
    valid = submit_form()
    print("✅ Failed submission due to missing street address" if not valid else "❌ Form submitted despite missing street address")

# Run test with invalid street address
def test_invalid_street_address():
    print("\nRunning: test_invalid_street_address")
    driver.find_element(By.NAME, "streetAddress").send_keys("12$ Main St")
    driver.find_element(By.NAME, "zipCode").send_keys("95699")
    driver.find_element(By.NAME, "city").send_keys("Folsom")
    driver.find_element(By.NAME, "state").send_keys("Nevada")
    driver.find_element(By.NAME, "country").send_keys("United States")
    fill_common_info()
    valid = submit_form()
    print("✅ Failed submission due to invalid characters in street address" if not valid else "❌ Form submitted with invalid street address")

# Run test with optional address filled incorrectly
def test_invalid_optional_address():
    print("\nRunning: test_invalid_optional_address")
    driver.find_element(By.NAME, "streetAddress").send_keys("123 Main St")
    driver.find_element(By.NAME, "addressOptional").send_keys("@@@")
    driver.find_element(By.NAME, "zipCode").send_keys("10001")
    driver.find_element(By.NAME, "city").send_keys("Folsom")
    driver.find_element(By.NAME, "state").send_keys("Nevada")
    driver.find_element(By.NAME, "country").send_keys("United States")
    fill_common_info()
    valid = submit_form()
    print("✅ Failed submission due to invalid optional address" if not valid else "❌ Form submitted with invalid optional address")

# Run test with valid address fields
def test_valid_address_all_fields():
    print("\nRunning: test_valid_address_all_fields")
    driver.find_element(By.NAME, "streetAddress").send_keys("315 Leidesdorff St")
    driver.find_element(By.NAME, "addressOptional").send_keys("Apt 1")
    driver.find_element(By.NAME, "zipCode").send_keys("95630")
    driver.find_element(By.NAME, "city").send_keys("Folsom")
    driver.find_element(By.NAME, "state").send_keys("California")
    driver.find_element(By.NAME, "country").send_keys("United States")
    fill_common_info()
    valid = submit_form()
    print("✅ Form submitted successfully with all valid address fields" if valid else "❌ Form should have passed but failed")

# Common personal info for all tests
def fill_common_info():
    driver.find_element(By.NAME, "customerFirstName").send_keys("Greg")
    driver.find_element(By.NAME, "customerLastName").send_keys("Smith")
    driver.find_element(By.ID, "customerEmail").send_keys("Gsmith@example.com")
    driver.find_element(By.ID, "customerPhone").send_keys("9162786011")

# Run address validation tests
test_missing_street_address()
reset_form()

test_invalid_street_address()
reset_form()

test_invalid_optional_address()
reset_form()

test_valid_address_all_fields()
reset_form()

driver.quit()