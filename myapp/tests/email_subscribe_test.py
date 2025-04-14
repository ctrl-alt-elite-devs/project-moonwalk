from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Test emails
new_email = "testuser_selenium_001@example.com"
existing_email = "testuser_selenium_001@example.com"  # Simulate as existing by submitting twice

# Setup Firefox
options = Options()
options.headless = False  # Set to True if you want to run in headless mode
driver = webdriver.Firefox(options=options)
driver.set_window_size(1200, 900)

try:
    driver.get("http://localhost:8000/")  # Replace with your local dev URL if needed
    wait = WebDriverWait(driver, 10)

    def submit_email(email):
        print(f"📧 Submitting email: {email}")
        email_input = wait.until(EC.presence_of_element_located((By.ID, "emailAddress")))
        email_input.clear()
        email_input.send_keys(email)

        subscribe_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "subscribeButton")))
        subscribe_btn.click()

        modal = wait.until(EC.visibility_of_element_located((By.ID, "subscription-modal")))
        modal_msg = modal.find_element(By.ID, "modal-message").text.strip()

        # Close modal
        driver.find_element(By.ID, "close-modal").click()
        time.sleep(1)

        return modal_msg

    # First attempt - should be new
    first_message = submit_email(new_email)
    print("🟢 First Submission Result:", first_message)

    # Second attempt - should say already subscribed
    second_message = submit_email(existing_email)
    print("🟡 Second Submission Result:", second_message)

    # Verify behavior
    if "already subscribed" in second_message.lower():
        print("✅ Existing email test passed.")
    else:
        print("❌ Existing email test failed.")

finally:
    time.sleep(2)
    driver.quit()