from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup
options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)
driver.set_window_size(1200, 900)
driver.get("http://localhost:8000/")
wait = WebDriverWait(driver, 10)

results = []

def print_result(name, passed):
    results.append((name, passed))
    symbol = "✅" if passed else "❌"
    print(f"{symbol} {name}")

def get_modal_message():
    modal = wait.until(EC.visibility_of_element_located((By.ID, "subscription-modal")))
    message = modal.find_element(By.ID, "modal-message").text.strip()
    close_btn = driver.find_element(By.ID, "close-modal")
    time.sleep(2)
    close_btn.click()
    wait.until(EC.invisibility_of_element_located((By.ID, "subscription-modal")))
    return message

try:
    # ✅ Valid email test
    try:
        email_input = wait.until(EC.presence_of_element_located((By.ID, "emailAddress")))
        email_input.clear()
        email_input.send_keys("") #place email of choice in here
        time.sleep(1)
        driver.find_element(By.ID, "subscribeButton").click()
        msg = get_modal_message()
        print_result("Valid email input test", "thank" in msg.lower() or "already subscribed" in msg.lower())
    except Exception:
        print_result("Valid email input test", False)

    # ✅ Already subscribed email test
    try:
        email_input.clear()
        email_input.send_keys("") #place email of choice in here
        time.sleep(1)
        driver.find_element(By.ID, "subscribeButton").click()
        msg = get_modal_message()
        print_result("Already subscribed email test", "already subscribed" in msg.lower())
    except Exception:
        print_result("Already subscribed email test", False)

    # ✅ Invalid email test
    try:
        email_input.clear()
        email_input.send_keys("invalid-email")
        time.sleep(1)
        driver.find_element(By.ID, "subscribeButton").click()
        msg = get_modal_message()
        print_result("Invalid email input test", "invalid email format" in msg.lower())
    except Exception:
        print_result("Invalid email input test", False)

    # ✅ Valid phone number test
    try:
        phone_input = wait.until(EC.presence_of_element_located((By.ID, "phoneNum")))
        phone_input.clear()
        phone_input.send_keys("1234567890")
        time.sleep(1)
        driver.find_element(By.ID, "subscribeButtonPhone").click()
        msg = get_modal_message()
        print_result("Valid phone number test", "saved" in msg.lower() or "already subscribed" in msg.lower())
    except Exception:
        print_result("Valid phone number test", False)

    # ✅ Already saved phone test
    try:
        phone_input.clear()
        phone_input.send_keys("1234567890")
        time.sleep(1)
        driver.find_element(By.ID, "subscribeButtonPhone").click()
        msg = get_modal_message()
        print_result("Phone number already saved test", "already subscribed" in msg.lower())
    except Exception:
        print_result("Phone number already saved test", False)

    # ✅ Invalid phone number test
    try:
        phone_input.clear()
        phone_input.send_keys("abc")
        time.sleep(1)
        driver.find_element(By.ID, "subscribeButtonPhone").click()
        msg = get_modal_message()
        print_result("Invalid phone number test", "10 digits" in msg.lower())
    except Exception:
        print_result("Invalid phone number test", False)

finally:
    time.sleep(2)
    driver.quit()

    print("\n--- Test Summary ---")
    all_passed = all(passed for _, passed in results)
    for name, passed in results:
        symbol = "✅" if passed else "❌"
        print(f"{symbol} {name}")

    if all_passed:
        print("\n🎉 All tests passed successfully!")
    else:
        print("\n⚠️ Some tests failed.")