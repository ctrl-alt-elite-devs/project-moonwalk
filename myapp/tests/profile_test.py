from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Step 1: Visit homepage
    driver.get("http://localhost:8000/")
    print("🔐 Visiting homepage...")

    # Step 2: Click on user icon to open login modal
    login_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "open_login"))
    )
    login_icon.click()
    print("👤 Login modal triggered.")

    # Step 3: Wait for modal and fill in login form
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "login-modal"))
    )
    print("✍️ Filling login form...")

    driver.find_element(By.NAME, "email").send_keys("yourfilter95@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("Amnk080401")
    driver.find_element(By.CSS_SELECTOR, "button.login-btn").click()

    # Step 4: Wait for login to complete (profile icon becomes link)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".profile_btn a"))
    )
    print("✅ Logged in successfully.")

    # Step 5: Go to profile page
    driver.get("http://localhost:8000/profile/")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "profile-container"))
    )
    print("📄 Profile page loaded.")

    # Step 6: Click "Edit Address" button to show form
    edit_button = WebDriverWait(driver, 10).until( 
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Edit Address')]"))
)
    
    edit_button.click()
    time.sleep(1)
    
    # Check visibility of the form
    form = driver.find_element(By.ID, "address-form")
    if form.is_displayed(): 
        print("✅ Address form is now visible.")
    else:
        print("❌ Address form is still hidden.")

    # Step 7: Fill out new address
    driver.find_element(By.NAME, "street_address").clear()
    driver.find_element(By.NAME, "street_address").send_keys("123 Moon St")

    driver.find_element(By.NAME, "street_address2").clear()
    driver.find_element(By.NAME, "street_address2").send_keys("Suite 42")

    driver.find_element(By.NAME, "city").clear()
    driver.find_element(By.NAME, "city").send_keys("Lunarville")

    driver.find_element(By.NAME, "state").clear()
    driver.find_element(By.NAME, "state").send_keys("CA")

    driver.find_element(By.NAME, "zip_code").clear()
    driver.find_element(By.NAME, "zip_code").send_keys("90001")

    # Step 8: Click Save
    driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Save')]").click()
    time.sleep(2)

    # Step 9: Verify the address update reflected on the page
    updated_address = driver.find_element(By.ID, "address-display").text
    if "123 Moon St" in updated_address and "Lunarville" in updated_address:
        print("✅ Address updated and displayed correctly.")
    else:
        print("⚠️ Address submitted but not reflected correctly.")

except Exception as e:
    print(f"❌ Test failed: {e}")

finally:
    driver.quit()
