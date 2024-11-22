import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestPomodoroTimer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the WebDriver (make sure to have the correct path to your WebDriver)
        cls.driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
        cls.driver.get('http://localhost:5000')  # Replace with the URL of your app

    def setUp(self):
        # Ensure the page has loaded and all elements are present
        self.driver.get('http://localhost:5000/pomodoro')  # Replace with the URL of your Pomodoro page
        time.sleep(2)  # Allow time for the page to load completely

    def test_start_timer(self):
        # Get the current window handle (initial window)
        initial_window = self.driver.current_window_handle

        # Switch to the correct window (if applicable)
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])

        # Ensure the window is still open
        if self.driver.current_window_handle != initial_window:
            # Wait until the timer element is present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "timer"))
            )

            # Start the timer by interacting with the start button (assuming it's the correct interaction)
            start_button = self.driver.find_element(By.ID, "start-button")
            start_button.click()

            # Wait for the timer to update
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element((By.ID, "timer"), "10:00")
            )

            # Get the updated time from the timer
            updated_time = self.driver.find_element(By.ID, "timer").text

            # Assert that the timer is showing the correct time
            self.assertEqual(updated_time, "10:00")

            # Optionally, handle any unexpected alerts if they appear
            try:
                alert = Alert(self.driver)
                alert.accept()
            except:
                pass  # No alert, continue with the test

    def test_restart_timer(self):
        # Test the restart timer functionality
        restart_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Restart')]")
        restart_button.click()
        time.sleep(1)  # Wait a moment for the timer to reset

        # Check if the timer has reset to 15:00
        timer_element = self.driver.find_element(By.ID, 'timer')
        self.assertEqual(timer_element.text, '15:00')

    def test_choose_time(self):
        # Handle any alert that may appear
        try:
            alert = Alert(self.driver)
            alert.accept()
        except:
            pass

        # Execute script to simulate user input for timer
        self.driver.execute_script("window.prompt = function() { return '10'; }")

        # Wait for the timer to update (adjust the element locator accordingly)
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "timer_display_id"), "10:00")
        )

        # Verify the timer value is set correctly
        timer_display = self.driver.find_element(By.ID, "timer_display_id")
        self.assertEqual(timer_display.text, "10:00")

    @classmethod
    def tearDownClass(cls):
        # Close the browser after the tests are completed
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
