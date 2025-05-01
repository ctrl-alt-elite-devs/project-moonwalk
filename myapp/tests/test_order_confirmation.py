from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import unittest

class OrderConfirmationTest(unittest.TestCase):
    def setUp(self):
        options = Options()
        self.driver = webdriver.Firefox(options=options)
        self.driver.set_window_size(1200, 900)
        self.driver.get("http://localhost:8000/shop/")
        self.wait = WebDriverWait(self.driver, 20)

    def test_full_order_flow(self):
        driver = self.driver
        wait = self.wait

        print("🛒 Adding item to cart...")
        add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-id="21"]')))
        add_btn.click()

        # 🔄 Wait for cart count to update after reload (if applicable)
        wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "cart-count"), "1"))
        time.sleep(1)

        print("🛒 Going to cart...")
        cart_icon = wait.until(EC.element_to_be_clickable((By.ID, "cart-icon")))
        cart_icon.click()

        print("📦 Proceeding to checkout...")
        driver.get("http://localhost:8000/checkout/")       

        print("🏠 Filling out delivery details...")
        driver.find_element(By.ID, "customerStreetAddress").send_keys("add test address here")
        driver.find_element(By.ID, "customerZipCode").send_keys("95823")
        driver.find_element(By.ID, "customerCity").send_keys("Sacramento")
        driver.find_element(By.ID, "customerState").send_keys("CA")
        driver.find_element(By.ID, "customerCountry").send_keys("United States")
        driver.find_element(By.ID, "customerFirstName").send_keys("J")
        driver.find_element(By.ID, "customerLastName").send_keys("B")
        driver.find_element(By.ID, "customerEmail").send_keys("add email here")
        driver.find_element(By.ID, "customerPhone").send_keys("use real phone number here")

        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "payment-proceed"))
        )
        time.sleep(0.5)  # Optional small buffer
        submit_btn.click()
        wait.until(EC.url_contains("/payment"))
        print("💳 At payment page...")

        # Wait for Square card iframe to appear and switch to it
        time.sleep(2)
        driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, 'iframe[src*="sandbox"]'))

        print("💳 Filling card info...")
        card_fields = driver.find_elements(By.TAG_NAME, "input")
        card_fields[0].send_keys("4111111111111111")
        card_fields[1].send_keys("04/44")
        card_fields[2].send_keys("411")
        time.sleep(2)
        card_fields[3].send_keys("95823")

        driver.switch_to.default_content()

        print("💸 Clicking Pay...")
        pay_btn = wait.until(EC.element_to_be_clickable((By.ID, "pay")))
        pay_btn.click()

        # Wait for redirect to order summary
        print("⏳ Waiting for confirmation...")
        wait.until(EC.url_matches(r"/order-summary/\d+/"))

        # ✅ Grab data from localStorage
        print("\n📦 Extracting localStorage data...")
        get_item = lambda key: driver.execute_script(f"return localStorage.getItem('{key}');")
        first_name = get_item("customerFirstName")
        last_name = get_item("customerLastName")
        email = get_item("customerEmail")
        phone = get_item("customerPhone")
        order_id = get_item("squareOrderId")
        email_sent = get_item("email_sent")

        # ✅ Output Results
        def print_check(name, value):
            passed = bool(value and value.strip())
            print(f"{'✅' if passed else '❌'} {name}: {value or 'Not Found'}")

        print_check("First Name", first_name)
        print_check("Last Name", last_name)
        print_check("Email", email)
        print_check("Phone", phone)
        print_check("Square Order ID", order_id)
        print_check("Email Sent", email_sent)

    def tearDown(self):
        time.sleep(3)
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()