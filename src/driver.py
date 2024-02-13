from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configuration import Configuration
from util import GetActivationKey
import asyncio
class Driver:
    def __init__(self, profilePath, configuration):
        self.profile = webdriver.ChromeOptions()
        self.profile.add_argument("user-data-dir="+profilePath)
        self.driver = webdriver.Chrome(options=self.profile)
        self.configuration: Configuration = configuration

    async def RunBrowser(self, posnumber):
        self.driver.get(self.configuration.url)
        await self.WelcomeLogin(posnumber)
        await self.PressConnect()

    async def WelcomeLogin(self, posnumber):
        input_username_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='userName']")))
        input_username_field.send_keys(self.configuration.username)

        input_password_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='password']")))
        input_password_field.send_keys(self.configuration.password)

        input_activation_key_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='activationKey']")))
        input_activation_key_field.send_keys(GetActivationKey(self.configuration.chainnumber, self.configuration.storenumber, posnumber))

        press_connect_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "submit-button")))
        press_connect_button.click()

        await asyncio.sleep(20)

    async def PressConnect(self):
        press_connect = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//login-lock/button/span[1]")))
        press_connect.click()
        await asyncio.sleep(5)


    
