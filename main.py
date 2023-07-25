import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import os


SPEED_TEST = "https://www.speedtest.net/"
TWITTER = "https://twitter.com/i/flow/login?input_flow_data=%7B%22requested_variant%22%3A%22eyJsYW5nIjoiZW4ifQ%3D%3D%22%7D"

EMAIL = os.environ.get("Email")
PASS = os.environ.get("Password")
USERNAME = os.environ.get("User-Name")

class InternetSpeedTwitterBot:
    def __init__(self):
        chrome_driver_path = "C:\Development\chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        # options.add_argument("--headless")
        options.add_experimental_option("detach", True)
        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)

    def get_internet_speed(self):
        self.driver.get(SPEED_TEST)
        self.driver.find_element(by=By.CLASS_NAME, value="js-start-test").click()

        WebDriverWait(self.driver, timeout=120).until(
            EC.presence_of_element_located(self.driver.find_element(by=By.CLASS_NAME, value="download-speed")))

        download = self.driver.find_element(by=By.CLASS_NAME, value="download-speed").text
        upload = self.driver.find_element(by=By.CLASS_NAME, value="upload-speed").text
        return {'down' : download, 'up': upload}


    def tweet_at_provider(self, speed):
        self.driver.get(TWITTER)
        time.sleep(3)
        email_box = self.driver.find_element(by=By.NAME, value="text")

        ActionChains(self.driver).move_to_element(email_box).click().send_keys(EMAIL).perform()

        next_btn = self.driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Next')]")
        next_btn.click()
        time.sleep(3)

        try:
            self.driver.find_element(by=By.NAME, value="password")

        except NoSuchElementException:

            email_box = self.driver.find_element(by=By.NAME, value="text")
            ActionChains(self.driver).move_to_element(email_box).click().send_keys(USERNAME).perform()
            next_btn = self.driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Next')]")
            next_btn.click()

        time.sleep(3)
        password_box = self.driver.find_element(by=By.NAME, value="password")
        ActionChains(self.driver).move_to_element(password_box).click().send_keys(PASS).perform()
        time.sleep(1)

        login_btn = self.driver.find_element(by=By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/'
                                                                'div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
        login_btn.click()

        message = f"Hey Internet Provider, why is my internet speed {speed['down']}down / {speed['down']}Up " \
                  f"when I pay for 10down/10Up"
        time.sleep(5)

        tweet_box = self.driver.find_element(by=By.XPATH, value="//*[contains(text(), 'What is happening?!')]")
        ActionChains(self.driver).move_to_element(tweet_box).click().send_keys(message).perform()

        tweet_btn = self.driver.find_element(by=By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/'
                                                                'div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/'
                                                                'div[2]/div[2]/div/div/div[2]/div[3]/div')
        tweet_btn.click()
        self.driver.close()
        self.driver.quit()


Bot = InternetSpeedTwitterBot()
speed = Bot.get_internet_speed()
Bot.tweet_at_provider(speed)
