# test checkout form validation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
import time


# launch Firefox browser
driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))
# load checkout page
driver.get('http://localhost:8000/checkout/')
# give time for browser to open
time.sleep(5)


# test form with valid inputs and input in the address optional
def valid_input_optional():
    driver.find_element(By.NAME, "streetAddress").send_keys("123 Main St")
    driver.find_element(By.NAME, "addressOptional").send_keys("Apt 1") # apartment number 1
    driver.find_element(By.NAME, "zipCode").send_keys("10001")
    driver.find_element(By.NAME, "city").send_keys("Albany")
    driver.find_element(By.NAME, "state").send_keys("New York")
    driver.find_element(By.NAME, "country").send_keys("United States")
    driver.find_element(By.NAME, "firstName").send_keys("John")
    driver.find_element(By.NAME, "lastName").send_keys("Doe")
    driver.find_element(By.ID, "customerEmail").send_keys("johndoe@example.com")
    driver.find_element(By.ID, "customerPhone").send_keys("9162786011") #sac state phone number

    is_valid = submit_form()

    if is_valid != False:
        print("✅ Checkout Form passed validation because of valid input (including address optional)")
    else:
        print("❌ Checkout Form failed validation because of valid input (including address optional)")


# test form with valid inputs and NO input in the address optional
def valid_input_no_optional():
    driver.find_element(By.NAME, "streetAddress").send_keys("123 Main St")
    driver.find_element(By.NAME, "addressOptional").send_keys("") # empty
    driver.find_element(By.NAME, "zipCode").send_keys("10001")
    driver.find_element(By.NAME, "city").send_keys("Albany")
    driver.find_element(By.NAME, "state").send_keys("New York")
    driver.find_element(By.NAME, "country").send_keys("United States")
    driver.find_element(By.NAME, "firstName").send_keys("John")
    driver.find_element(By.NAME, "lastName").send_keys("Doe")
    driver.find_element(By.ID, "customerEmail").send_keys("johndoe@example.com")
    driver.find_element(By.ID, "customerPhone").send_keys("9162786011")

    is_valid = submit_form()

    if is_valid != False:
        print("✅ Checkout Form passed validation because of valid input (excluding address optional: is empty)")
    else:
        print("❌ Checkout Form failed validation because of valid input (excluding address optional: is empty)")


# test form with invalid input for street address
def invalid_input_street():
    driver.find_element(By.NAME, "streetAddress").send_keys("12$ Main St") # invalid input here $
    driver.find_element(By.NAME, "addressOptional").send_keys("") # empty
    driver.find_element(By.NAME, "zipCode").send_keys("10001")
    driver.find_element(By.NAME, "city").send_keys("Albany")
    driver.find_element(By.NAME, "state").send_keys("New York")
    driver.find_element(By.NAME, "country").send_keys("United States")
    driver.find_element(By.NAME, "firstName").send_keys("John")
    driver.find_element(By.NAME, "lastName").send_keys("Doe")
    driver.find_element(By.ID, "customerEmail").send_keys("johndoe@example.com")
    driver.find_element(By.ID, "customerPhone").send_keys("9162786011")

    is_valid = submit_form()

    if is_valid == False:
        print("✅ Checkout Form failed validation because of invalid street address: 12$ Main St")
    else:
        print("❌ Checkout Form failed validation because of invalid street address: 12$ Main St")


# test form with invalid input for optional address
def invalid_input_optional():
    driver.find_element(By.NAME, "streetAddress").send_keys("123 Main St")
    driver.find_element(By.NAME, "addressOptional").send_keys("@") # invalid input here @
    driver.find_element(By.NAME, "zipCode").send_keys("10001")
    driver.find_element(By.NAME, "city").send_keys("Albany")
    driver.find_element(By.NAME, "state").send_keys("New York")
    driver.find_element(By.NAME, "country").send_keys("United States")
    driver.find_element(By.NAME, "firstName").send_keys("John")
    driver.find_element(By.NAME, "lastName").send_keys("Doe")
    driver.find_element(By.ID, "customerEmail").send_keys("johndoe@example.com")
    driver.find_element(By.ID, "customerPhone").send_keys("9162786011")

    is_valid = submit_form()

    if is_valid == False:
        print("✅ Checkout Form failed validation because of invalid address optional: @")
    else:
        print("❌ Checkout Form failed validation because of invalid address optional: @")


# test form with invalid input for zipcode   
def invalid_input_zipcode():
    driver.find_element(By.NAME, "streetAddress").send_keys("123 Main St")
    driver.find_element(By.NAME, "addressOptional").send_keys("")
    driver.find_element(By.NAME, "zipCode").send_keys("abc") # invalid input here abc
    driver.find_element(By.NAME, "city").send_keys("Albany")
    driver.find_element(By.NAME, "state").send_keys("New York")
    driver.find_element(By.NAME, "country").send_keys("United States")
    driver.find_element(By.NAME, "firstName").send_keys("John")
    driver.find_element(By.NAME, "lastName").send_keys("Doe")
    driver.find_element(By.ID, "customerEmail").send_keys("johndoe@example.com")
    driver.find_element(By.ID, "customerPhone").send_keys("9162786011")

    is_valid = submit_form()

    if is_valid == False:
        print("✅ Checkout Form failed validation because of invalid zipcode: abc")
    else:
        print("❌ Checkout Form failed validation because of invalid zipcode: abc")


# test form with invalid input for city  
def invalid_input_city():
    driver.find_element(By.NAME, "streetAddress").send_keys("123 Main St")
    driver.find_element(By.NAME, "addressOptional").send_keys("")
    driver.find_element(By.NAME, "zipCode").send_keys("10010")
    driver.find_element(By.NAME, "city").send_keys("12345") # invalid input here 12345
    driver.find_element(By.NAME, "state").send_keys("New York")
    driver.find_element(By.NAME, "country").send_keys("United States")
    driver.find_element(By.NAME, "firstName").send_keys("John")
    driver.find_element(By.NAME, "lastName").send_keys("Doe")
    driver.find_element(By.ID, "customerEmail").send_keys("johndoe@example.com")
    driver.find_element(By.ID, "customerPhone").send_keys("9162786011")

    is_valid = submit_form()

    if is_valid == False:
        print("✅ Checkout Form failed validation because of invalid city: 12345")
    else:
        print("❌ Checkout Form failed validation because of invalid city: 12345")


# test form with invalid input for country
def invalid_input_country():
    driver.find_element(By.NAME, "streetAddress").send_keys("123 Main St")
    driver.find_element(By.NAME, "addressOptional").send_keys("")
    driver.find_element(By.NAME, "zipCode").send_keys("10010")
    driver.find_element(By.NAME, "city").send_keys("Albany")
    driver.find_element(By.NAME, "state").send_keys("New York")
    driver.find_element(By.NAME, "country").send_keys("United States1") # invalid input here United States1
    driver.find_element(By.NAME, "firstName").send_keys("John")
    driver.find_element(By.NAME, "lastName").send_keys("Doe")
    driver.find_element(By.ID, "customerEmail").send_keys("johndoe@example.com")
    driver.find_element(By.ID, "customerPhone").send_keys("9162786011")

    is_valid = submit_form()

    if is_valid == False:
        print("✅ Checkout Form failed validation because of invalid country: United States1")
    else:
        print("❌ Checkout Form failed validation because of invalid country: United States1")


# test form with invalid input for first name
def invalid_input_firstname():
    driver.find_element(By.NAME, "streetAddress").send_keys("123 Main St")
    driver.find_element(By.NAME, "addressOptional").send_keys("")
    driver.find_element(By.NAME, "zipCode").send_keys("10010")
    driver.find_element(By.NAME, "city").send_keys("Albany")
    driver.find_element(By.NAME, "state").send_keys("New York")
    driver.find_element(By.NAME, "country").send_keys("United States")
    driver.find_element(By.NAME, "firstName").send_keys("12345") # invalid input here 12345
    driver.find_element(By.NAME, "lastName").send_keys("Doe")
    driver.find_element(By.ID, "customerEmail").send_keys("johndoe@example.com")
    driver.find_element(By.ID, "customerPhone").send_keys("9162786011")

    is_valid = submit_form()

    if is_valid == False:
        print("✅ Checkout Form failed validation because of invalid first name: 12345")
    else:
        print("❌ Checkout Form failed validation because of invalid first name: 12345")


# test form with invalid input for last name
def invalid_input_lastname():
    driver.find_element(By.NAME, "streetAddress").send_keys("123 Main St")
    driver.find_element(By.NAME, "addressOptional").send_keys("")
    driver.find_element(By.NAME, "zipCode").send_keys("10010")
    driver.find_element(By.NAME, "city").send_keys("Albany")
    driver.find_element(By.NAME, "state").send_keys("New York")
    driver.find_element(By.NAME, "country").send_keys("United States")
    driver.find_element(By.NAME, "firstName").send_keys("John")
    driver.find_element(By.NAME, "lastName").send_keys("12345") # invalid input here 12345
    driver.find_element(By.ID, "customerEmail").send_keys("johndoe@example.com")
    driver.find_element(By.ID, "customerPhone").send_keys("9162786011")

    is_valid = submit_form()

    if is_valid == False:
        print("✅ Checkout Form failed validation because of invalid last name: 12345")
    else:
        print("❌ Checkout Form failed validation because of invalid last name: 12345")


# test form with invalid input for email   
def invalid_input_email():
    driver.find_element(By.NAME, "streetAddress").send_keys("123 Main St")
    driver.find_element(By.NAME, "addressOptional").send_keys("")
    driver.find_element(By.NAME, "zipCode").send_keys("10010")
    driver.find_element(By.NAME, "city").send_keys("Albany")
    driver.find_element(By.NAME, "state").send_keys("New York")
    driver.find_element(By.NAME, "country").send_keys("United States")
    driver.find_element(By.NAME, "firstName").send_keys("John")
    driver.find_element(By.NAME, "lastName").send_keys("1234")
    driver.find_element(By.ID, "customerEmail").send_keys("johndoe@") # invalid input here johndoe@
    driver.find_element(By.ID, "customerPhone").send_keys("9162786011")

    is_valid = submit_form()

    if is_valid == False:
        print("✅ Checkout Form failed validation because of invalid email: johndoe@")
    else:
        print("❌ Checkout Form failed validation because of invalid email: johndoe@")


# test form with invalid input for phone characters
def invalid_input_phone_chars():
    driver.find_element(By.NAME, "streetAddress").send_keys("123 Main St")
    driver.find_element(By.NAME, "addressOptional").send_keys("")
    driver.find_element(By.NAME, "zipCode").send_keys("10010")
    driver.find_element(By.NAME, "city").send_keys("Albany")
    driver.find_element(By.NAME, "state").send_keys("New York")
    driver.find_element(By.NAME, "country").send_keys("United States")
    driver.find_element(By.NAME, "firstName").send_keys("John")
    driver.find_element(By.NAME, "lastName").send_keys("1234")
    driver.find_element(By.ID, "customerEmail").send_keys("johndoe@")
    driver.find_element(By.ID, "customerPhone").send_keys("abcdefghij") # invalid input here abcdefghij

    is_valid = submit_form()

    if is_valid == False:
        print("✅ Checkout Form failed validation because of invalid phone number characters: abcdefghij")
    else:
        print("❌ Checkout Form failed validation because of invalid phone number characters: abcdefghij")


# test form with invalid input for phone length  
def invalid_input_phone_length():
    driver.find_element(By.NAME, "streetAddress").send_keys("123 Main St")
    driver.find_element(By.NAME, "addressOptional").send_keys("")
    driver.find_element(By.NAME, "zipCode").send_keys("10010")
    driver.find_element(By.NAME, "city").send_keys("Albany")
    driver.find_element(By.NAME, "state").send_keys("New York")
    driver.find_element(By.NAME, "country").send_keys("United States")
    driver.find_element(By.NAME, "firstName").send_keys("John")
    driver.find_element(By.NAME, "lastName").send_keys("1234")
    driver.find_element(By.ID, "customerEmail").send_keys("johndoe@")
    driver.find_element(By.ID, "customerPhone").send_keys("1234567") # invalid input here 1234567: length of 7 need 10

    is_valid = submit_form()

    if is_valid == False:
        print("✅ Checkout Form failed validation because of invalid phone number length: 1234567 (length of 7, needs 10)")
    else:
        print("❌ Checkout Form failed validation because of invalid phone number length: 1234567 (length of 7, needs 10)")


# test form with invalid input for all: spaces for all input minus state (cause its a drop down select)     
def invalid_input_space_all():
    driver.find_element(By.NAME, "streetAddress").send_keys(" ")
    driver.find_element(By.NAME, "addressOptional").send_keys("")
    driver.find_element(By.NAME, "zipCode").send_keys(" ")
    driver.find_element(By.NAME, "city").send_keys(" ")
    driver.find_element(By.NAME, "state").send_keys(" ")
    driver.find_element(By.NAME, "country").send_keys("Albany")
    driver.find_element(By.NAME, "firstName").send_keys(" ")
    driver.find_element(By.NAME, "lastName").send_keys(" ")
    driver.find_element(By.ID, "customerEmail").send_keys(" ")
    driver.find_element(By.ID, "customerPhone").send_keys(" ")

    is_valid = submit_form()

    if is_valid == False:
        print("✅ Checkout Form failed validation because of all inputs with only a space")
    else:
        print("❌ Checkout Form failed validation because of all inputs with only a space")


# test form with invalid input for all: empty strings for all (minus state)    
def invalid_input_empty_all():
    driver.find_element(By.NAME, "streetAddress").send_keys("")
    driver.find_element(By.NAME, "addressOptional").send_keys("")
    driver.find_element(By.NAME, "zipCode").send_keys("")
    driver.find_element(By.NAME, "city").send_keys("")
    driver.find_element(By.NAME, "state").send_keys("")
    driver.find_element(By.NAME, "country").send_keys("Albany")
    driver.find_element(By.NAME, "firstName").send_keys("")
    driver.find_element(By.NAME, "lastName").send_keys("")
    driver.find_element(By.ID, "customerEmail").send_keys("")
    driver.find_element(By.ID, "customerPhone").send_keys("")

    is_valid = submit_form()

    if is_valid == False:
        print("✅ Checkout Form failed validation because of all inputs with empty string.")
    else:
        print("❌ Checkout Form failed validation because of all inputs with empty string.")


# clear input text boxes before next test sequence        
def clear_input():
    # close alerts, if any
    try:
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert.accept()
    except TimeoutException:
        # If no alert appears within 10 seconds, continue
        pass
    except UnexpectedAlertPresentException:
        # In case of unexpected alert
        pass
    print() # spacing purposes for prints

    # clear
    driver.find_element(By.NAME, "streetAddress").clear()
    driver.find_element(By.NAME, "addressOptional").clear()
    driver.find_element(By.NAME, "zipCode").clear()
    driver.find_element(By.NAME, "city").clear()
    #driver.find_element(By.NAME, "state").clear()
    driver.find_element(By.NAME, "country").clear()
    driver.find_element(By.NAME, "firstName").clear()
    driver.find_element(By.NAME, "lastName").clear()
    driver.find_element(By.ID, "customerEmail").clear()
    driver.find_element(By.ID, "customerPhone").clear()


# appear the test submit button that is hidden   
def submit_appear():
    driver.execute_script("""
        var element = document.getElementById('checkout_button');
        element.scrollIntoView({behavior: 'smooth', block: 'center'});  // Scroll the element into view
        element.style.display = 'block';  // Ensure it is not hidden
    """)


# after testing, hide test submit button again
def submit_disappear():
    driver.execute_script("""
        var element = document.getElementById('checkout_button');
        if (element) {
            element.scrollIntoView({behavior: 'smooth', block: 'center'});  // Scroll into view
            element.style.display = 'none';  // Hide the button
        }
    """)


# click on the test submit button to trigger form checking validation
# return the result of the validation   
def submit_form():
    is_valid = True # initial to form is valid
    is_valid = driver.execute_script("""
        return checkout_test_validation();
    """)
    return is_valid


if __name__ == "__main__":
    print("---------------------------------")
    print("Test for Checkout Form Validation")
    print("---------------------------------")
    print("         Requirements")
    print("---------------------------------")
    print("Street Address: Allows letters (A-Z, a-z), numbers (0-9), and spaces. No whitespaces or empty spaces.")
    print("Address Optional: Allows letters (A-Z, a-z), numbers (0-9), and spaces, if used. Allows empty space, not whitespaces.")
    print("Zip Code: Allow numbers (0-9). No whitespaces or empty spaces.")
    print("City: Allows letters (A-Z, a-z) and spaces. No whitespaces or empty spaces.")
    print("State: Selected via pre-loaded drop down bar.")
    print("First Name: Allows letters (A-Z, a-z) and spaces. No whitespaces or empty spaces.")
    print("Last Name: Allows letters (A-Z, a-z) and spaces. No whitespaces or empty spaces.")
    print("Email: Has to be in email format.")
    print("Phone: Allow numbers (0-9). Has to be in length 10 only. No whitespaces or empty spaces.")
    print("---------------------------------")
    print("")

    submit_appear()

    valid_input_optional()
    clear_input()
    valid_input_no_optional()
    clear_input()
    invalid_input_street()
    clear_input()
    invalid_input_optional()
    clear_input()
    invalid_input_zipcode()
    clear_input()
    invalid_input_city()
    clear_input()
    invalid_input_country()
    clear_input()
    invalid_input_firstname()
    clear_input()
    invalid_input_lastname()
    clear_input()
    invalid_input_email()
    clear_input()
    invalid_input_phone_chars()
    clear_input()
    invalid_input_phone_length()
    clear_input()
    invalid_input_space_all()
    clear_input()
    invalid_input_empty_all()

    submit_disappear()
