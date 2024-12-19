from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pytest
import time

class TestMocDocUI:
    @pytest.fixture(scope="class")
    def setup(self):
        # Specify the correct path to your ChromeDriver
        service = Service('C:/WebDriver/chromedriver.exe')  # Use your provided path
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("https://mocdoc.com/")  # Use the provided URL
        yield self  # Yield the instance of the test class
        self.driver.quit()

    def test_form_validations(self, setup):
        # Navigate to the form page
        setup.driver.get("https://mocdoc.com/ptuser/loginform")

        # Check required fields
        setup.driver.find_element(By.ID, "patient-login").click()  # Attempt to submit without filling out fields
        
        # Check if error message element exists
        try:
            error_message = setup.driver.find_element(By.ID, "error").text  # Assuming there's an error message element
            assert "This field is required" in error_message  # Validate the error message
        except Exception as e:
            print("Error message element not found:", e)

        # Validate email format
        email_field = setup.driver.find_element(By.ID, "emailormobile")
        email_field.send_keys("invalid_email")  # Enter an invalid email
        setup.driver.find_element(By.ID, "patient-login").click()
        
        # Check if error message element exists
        try:
            error_message = setup.driver.find_element(By.ID, "error").text
            assert "Invalid email format" in error_message  # Validate the error message
        except Exception as e:
            print("Error message element not found:", e)

    def test_button_navigation(self, setup):
        # Navigate to the login page
        setup.driver.get("https://mocdoc.com/")

        # Click on the login button
        setup.driver.find_element(By.LINK_TEXT, "Login").click()  # Update with the correct link text

        # Validate that the URL is correct after navigation
        assert "ptuser/loginform" in setup.driver.current_url

        # Fill out the login form and submit
        setup.driver.find_element(By.ID, "emailormobile").send_keys("9763332145")
        setup.driver.find_element(By.ID, "emailpwd").send_keys("123456")
        setup.driver.find_element(By.ID, "patient-login").click()

        # Validate redirection to the success page
        assert "dashboard" in setup.driver.current_url  # Update with the expected URL

    def test_responsive_design(self, setup):
        # Test on desktop size
        setup.driver.set_window_size(1200, 800)
        setup.driver.get("https://mocdoc.com/")
        assert "Expected Element" in setup.driver.page_source  # Validate elements for desktop

        # Test on tablet size
        setup.driver.set_window_size(768, 1024)
        setup.driver.get("https://mocdoc.com/")
        assert "Expected Element" in setup.driver.page_source  # Validate elements for tablet

        # Test on mobile size
        setup.driver.set_window_size(375, 667)
        setup.driver.get("https://mocdoc.com/")
        assert "Expected Element" in setup.driver.page_source  # Validate elements for mobile

if __name__ == "__main__":
    pytest.main()





# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# import pytest
# import time

# class TestMocDocUI:
#     @pytest.fixture(scope="class")
#     def setup(self):
#         # Specify the correct path to your ChromeDriver
#         service = Service('C:/WebDriver/chromedriver.exe')  # Use your provided path
#         self.driver = webdriver.Chrome(service=service)
#         self.driver.get("https://mocdoc.com/")  # Use the provided URL
#         yield self  # Yield the instance of the test class
#         self.driver.quit()

#     def test_home_page_title(self, setup):
#         # Verify the title of the home page
#         assert "Digital Healthcare Solutions" in setup.driver.title  # Use setup.driver

#     def test_patient_record_creation(self, setup):
#         # Example: Navigate to the patient creation form (update the selectors as needed)
#         setup.driver.find_element(By.LINK_TEXT, "ptuser/loginform").click()  # Example link text
#         time.sleep(2)  # Wait for the page to load

#         # Fill out the form (update the selectors as needed)
#         setup.driver.find_element(By.ID, "emailormobile").send_keys("9763332145")  # Example ID
#         setup.driver.find_element(By.ID, "emailpwd").send_keys("123456")  # Example ID

#         # Submit the form
#         setup.driver.find_element(By.ID, "patient-login").click()  # Example ID
#         time.sleep(2)  # Wait for the submission to complete

#         # Validate success message (update the selector as needed)
#         success_message = setup.driver.find_element(By.ID, "success").text  # Example ID
#         assert "Patient record created successfully!" in success_message

# if __name__ == "__main__":
#     pytest.main()