from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest

class OrderSummaryTest(unittest.TestCase):
    def setUp(self):
        options = Options()
        self.driver = webdriver.Firefox(options=options)
        self.driver.get("http://localhost:8000")  
        self.driver.maximize_window()

    def test_customer_info_and_order_id(self):
        driver = self.driver
        wait = WebDriverWait(driver, 40)

        print("🛑 Fill out the form manually and click 'Proceed to Payment' in the browser.")
        input("➡️ Press ENTER here in the terminal once you've reached the payment page...")

        # ✅ Continue test: wait for redirect to payment confirmation or summary page
        wait = WebDriverWait(driver, 20)
        wait.until(EC.url_contains("/payment"))

        print("✅ Now at payment page! Test continues...")

        # Optional: Continue to simulate payment or wait for confirmation page
        input("➡️ Press ENTER after completing payment manually...")

        # ✅ Final check
        wait.until(EC.url_contains("/orderSummary"))
        self.assertIn("orderSummary", driver.current_url)

        # ✅ Extract from localStorage (based on your payment script)
        first_name = driver.execute_script("return localStorage.getItem('customerFirstName');")
        last_name = driver.execute_script("return localStorage.getItem('customerLastName');")
        email = driver.execute_script("return localStorage.getItem('customerEmail');")
        phone = driver.execute_script("return localStorage.getItem('customerPhone');")
        order_id = driver.execute_script("return localStorage.getItem('squareOrderId');")
        email_sent = driver.execute_script("return localStorage.getItem('email_sent');")

        print("\n📦 Customer Info from localStorage:")
        print("🧍 First Name:", first_name)
        print("🧍 Last Name:", last_name)
        print("📧 Email:", email)
        print("📧 Email Sent:", email_sent)
        print("📞 Phone:", phone)
        print("🧾 Square Order ID:", order_id)

        # ✅ Optionally assert values
        self.assertIsNotNone(order_id)
        self.assertIn("@", email)
        self.assertTrue(phone.isdigit())

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()