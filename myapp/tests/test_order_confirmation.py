import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OrderConfirmationTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Safari()
        self.driver.get("http://localhost:8000")

    def test_full_order_flow(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # 1️⃣ Add a product to the cart
        driver.get("http://localhost:8000/shop/")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "add-to-cart-btn"))).click()
        time.sleep(1)

        # 2️⃣ Checkout
        driver.get("http://localhost:8000/checkout/")
        wait.until(EC.presence_of_element_located((By.ID, "customerFirstName"))).send_keys("Test")
        driver.find_element(By.ID, "customerLastName").send_keys("User")
        driver.find_element(By.ID, "customerEmail").send_keys("testuser@example.com")
        driver.find_element(By.ID, "customerPhone").send_keys("1234567890")

        driver.find_element(By.ID, "customerStreetAddress").send_keys("123 Main St")
        driver.find_element(By.ID, "customerCity").send_keys("Auburn")
        driver.find_element(By.ID, "customerZipCode").send_keys("11111")
        driver.find_element(By.ID, "customerState").send_keys("CA")
        driver.find_element(By.ID, "customerCountry").send_keys("USA")

        driver.find_element(By.ID, "payment-proceed").click()

        # 3️⃣ Fill Square Payment Fields
        time.sleep(3)

        card_iframe = driver.find_element(By.CSS_SELECTOR, "iframe[name^='sq-card-number']")
        driver.switch_to.frame(card_iframe)
        driver.find_element(By.NAME, "cardnumber").send_keys("4111111111111111")
        driver.switch_to.default_content()

        exp_iframe = driver.find_element(By.CSS_SELECTOR, "iframe[name^='sq-expiration-date']")
        driver.switch_to.frame(exp_iframe)
        driver.find_element(By.NAME, "exp-date").send_keys("0555")
        driver.switch_to.default_content()

        cvv_iframe = driver.find_element(By.CSS_SELECTOR, "iframe[name^='sq-cvv']")
        driver.switch_to.frame(cvv_iframe)
        driver.find_element(By.NAME, "cvv").send_keys("411")
        driver.switch_to.default_content()

        zip_iframe = driver.find_element(By.CSS_SELECTOR, "iframe[name^='sq-postal-code']")
        driver.switch_to.frame(zip_iframe)
        driver.find_element(By.NAME, "postal-code").send_keys("11111")
        driver.switch_to.default_content()

        # 4️⃣ Submit Payment
        driver.find_element(By.ID, "pay").click()

        # 5️⃣ Verify confirmation
        wait.until(EC.presence_of_element_located((By.ID, "confirmation-number")))
        self.assertIn("Confirmation Number", driver.page_source)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()