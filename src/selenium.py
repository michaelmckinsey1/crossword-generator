import os
import base64

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PRINT_SETTINGS = {
    "recentDestinations": [{
        "id": "Save as PDF",
        "origin": "local",
        "account": "",
    }],
    "selectedDestinationId": "Save as PDF",
    "version": 2,
    "isHeaderFooterEnabled": False,
    "isLandscapeEnabled": True
}
SUBMIT_XPATH='/html/body/div/div[2]/div/div/div[2]/form/div[2]/button'
TITLE_XPATH='/html/body/div/div[2]/div/div/div[2]/form/input[1]'
WORD_CLUE_XPATH='/html/body/div/div[2]/div/div/div[2]/form/textarea'

ANSWER_XPATH='/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/label'


class Selenium:
    def __init__(
        self,
        driver_path='bin/chrome-headless-shell-win64\chrome-headless-shell.exe'
    ):
        self.driver_path = driver_path
        # setup binary location
        options = webdriver.ChromeOptions()
        options.binary_location = self.driver_path
        self.options = options
    
    def get_xword(self, word_clue_str, topic, output_filename='xword.pdf'):
        # Create driver
        driver = webdriver.Chrome(options=self.options)
        # Go to webpage
        driver.get("https://crosswordlabs.com/")

        # Send str to title box
        title_box = driver.find_element('xpath', TITLE_XPATH)
        title_box.send_keys(topic)

        # Send str to input box
        word_clue_box = driver.find_element('xpath', WORD_CLUE_XPATH)
        word_clue_box.send_keys(word_clue_str)

        # Click the submit button
        submit_button = driver.find_element('xpath', SUBMIT_XPATH)  # Replace with the actual submit button details
        submit_button.click()

        # Wait for load
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ANSWER_XPATH))
        )

        # Put file in temp dir
        if not os.path.exists("static"):
            os.makedirs("static")
        output_path = f"static/{output_filename}"
        # Print blank xword to pdf
        pdf_data = driver.execute_cdp_cmd("Page.printToPDF", PRINT_SETTINGS)
        with open(output_path, 'wb') as file:
            file.write(base64.b64decode(pdf_data['data']))

        # Click answer button
        answer_button = driver.find_element('xpath', ANSWER_XPATH)
        answer_button.click()
        # Write answer pdf
        answer_data = driver.execute_cdp_cmd("Page.printToPDF", PRINT_SETTINGS)
        with open("static/answer.pdf", 'wb') as file:
            file.write(base64.b64decode(answer_data['data']))

        return output_path