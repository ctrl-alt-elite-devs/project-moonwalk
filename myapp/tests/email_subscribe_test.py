
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Test data
new_email = "testuser01@example.com"
existing_email = "testuser_selenium_001@example.com"
test_phone = "11111111111"

# Setup Firefox
options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)
driver.set_window_size(1200, 900)

try:
    driver.get("http://localhost:8000/")
    wait = WebDriverWait(driver, 10)

    def submit_email(email):
        print(f"📧 Submitting email: {email}")
        email_input = wait.until(EC.presence_of_element_located((By.ID, "emailAddress")))
        email_input.clear()
        email_input.send_keys(email)

        email_subscribe_btn = email_input.find_element(By.XPATH, "./following-sibling::button[@class='subscribeButton']")
        email_subscribe_btn.click()

        modal = wait.until(EC.visibility_of_element_located((By.ID, "subscription-modal")))
        modal_msg = modal.find_element(By.ID, "modal-message").text.strip()
        time.sleep(3)
        driver.find_element(By.ID, "close-modal").click()
        time.sleep(1)
        return modal_msg

    def submit_phone(phone):
        print(f"📱 Submitting phone: {phone}")
        phone_input = wait.until(EC.presence_of_element_located((By.ID, "phoneNum")))
        phone_input.clear()
        phone_input.send_keys(phone)

    # Corrected button ID based on your HTML
        phone_subscribe_btn = wait.until(EC.element_to_be_clickable((By.ID, "subscribeButtonPhone")))
        phone_subscribe_btn.click()

        modal = wait.until(EC.visibility_of_element_located((By.ID, "subscription-modal")))
        modal_msg = modal.find_element(By.ID, "modal-message").text.strip()
        time.sleep(5)
        driver.find_element(By.ID, "close-modal").click()
        time.sleep(1)
        return modal_msg
    
    def is_valid_phone(number):
        return number.isdigit() and len(number) >= 10

    # Example usag
    
    # Email flow
    first_email_msg = submit_email(new_email)
    print("🟢 Email Submission:", first_email_msg)

    second_email_msg = submit_email(existing_email)
    print("🟡 Email (again):", second_email_msg)

    # Phone flow
    # Test: Phone-only submission
    first_phone_msg = submit_phone(phone=test_phone)
    print("🔵 Phone Submission:", first_email_msg)
    
    second_phone_msg = submit_phone(phone=test_phone)
    print("🔵 Phone Submission:", second_phone_msg)
finally:
    time.sleep(4)
    driver.quit()
