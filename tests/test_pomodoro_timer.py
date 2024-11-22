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

    

    def test_restart_timer(self):
        # Test the restart timer functionality
        restart_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Restart')]")
        restart_button.click()
        time.sleep(1)  # Wait a moment for the timer to reset

        # Check if the timer has reset to 15:00
        timer_element = self.driver.find_element(By.ID, 'timer')
        self.assertEqual(timer_element.text, '15:00')

    
    @classmethod
    def tearDownClass(cls):
        # Close the browser after the tests are completed
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
