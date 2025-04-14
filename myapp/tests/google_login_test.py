import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MyTextTestResult(unittest.TextTestResult):
    def printErrors(self):
        super().printErrors()
        if self.wasSuccessful():
            self.stream.writeln("\n🎉 ALL TESTS PASSED! 🎉\n")

class MyTextTestRunner(unittest.TextTestRunner):
    resultclass = MyTextTestResult

class GoogleSignInTest(unittest.TestCase):

    def setUp(self):
        # Create and configure Chrome options
        options = Options()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        )
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        service = Service(executable_path=r"D:\chromedriver-win64\chromedriver-win64\chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=options)

    def tearDown(self):
        self.driver.quit()

    def test_google_sign_in_creates_user(self):
        driver = self.driver
        wait = WebDriverWait(driver, 30)

        # Step 1: Open homepage
        driver.get("http://127.0.0.1:8000/") 

        # Step 2: Click the profile icon to open the login modal
        profile_icon = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "open_login")))
        profile_icon.click()

        # Step 3: Wait for the login modal to become visible
        wait.until(EC.visibility_of_element_located((By.ID, "login-modal")))

        # Step 4: Click the Google sign-in button inside the modal
        google_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "classic-google-btn")))
        google_button.click()

        # Step 5: Wait until the URL indicates Google's login page
        wait.until(EC.url_contains("accounts.google.com"))

        # Step 6: Fill in the Google login form
        email_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='email']")))
        test_email = "moonwalktester@gmail.com"  
        email_input.send_keys(test_email)

        next_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), 'Next')]/parent::button")
        ))
        next_button.click()

        # Wait for the password field to be clickable and fill it in
        password_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
        driver.execute_script("arguments[0].scrollIntoView();", password_input)
        test_password = "!test12345"  # Replace with your test password
        password_input.send_keys(test_password)

        next_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), 'Next')]/parent::button")
        ))
        next_button.click()

        # New Step: Wait for and click the "Continue" (or consent) button if it appears.
        try:
            continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Continue')]/parent::button"))
            )
            continue_button.click()
            print("Clicked on the 'Continue' button.")
        except Exception as e:
            # If the button doesn't appear, print a message and proceed.
            print("No 'Continue' button detected; proceeding without clicking it.")

        # Step 7: Wait until Google completes the login; the app should now redirect back to the home page.
        wait.until(EC.url_contains("127.0.0.1"))
        print("After login, current URL:", driver.current_url)
        print("Page snippet:", driver.page_source[:500])

        # Step 8: On the home page, click the profile link to navigate to the profile page.
        profile_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".profile_btn a")))
        profile_link.click()

        # Step 9: Wait until the profile page loads and the element with ID "user-email" is present.
        user_email_element = wait.until(EC.presence_of_element_located((By.ID, "user-email")))
        self.assertEqual(user_email_element.text.strip(), test_email)

if __name__ == '__main__':
    unittest.main(testRunner=MyTextTestRunner(), verbosity=2)
