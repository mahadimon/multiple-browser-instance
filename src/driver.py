from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configuration import Configuration
from util import GetActivationKey
import asyncio
from configuration import PosUser

class Driver:
    def __init__(self, profilePath, configuration):
        self.profile = webdriver.ChromeOptions()
        self.profile.add_argument("user-data-dir="+profilePath)
        self.driver = webdriver.Chrome(options=self.profile)
        self.configuration: Configuration = configuration

    async def RunBrowser(self, posuser):
        self.driver.get(self.configuration.url)
        await self.WelcomeLogin(posuser)
        await self.PressConnect()
        await self.CashierLogin(posuser)
        await self.CashierLogOut()

    async def WelcomeLogin(self, posuser):
        input_username_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='userName']")))
        input_username_field.send_keys(self.configuration.username)

        input_password_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='password']")))
        input_password_field.send_keys(self.configuration.password)

        input_activation_key_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='activationKey']")))
        input_activation_key_field.send_keys(GetActivationKey(self.configuration.chainnumber, self.configuration.storenumber, posuser.posnumber))

        press_connect_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "submit-button")))
        press_connect_button.click()

        await asyncio.sleep(20)

    async def PressConnect(self):
        try:
            press_connect = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//login-lock/button/span[1]")))
            press_connect.click()
            await asyncio.sleep(5)
        except Exception as ex:
            print(f"Unexpected: {ex}, {type(ex)=}")

    async def CashierLogin(self, posuser: PosUser):
        try:
            input_cashier_number = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='cashierIdInput']")))
            input_cashier_number.send_keys(posuser.cashiernumber)

            input_cashier_number = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='cashierPasswordInput']")))
            input_cashier_number.send_keys(posuser.cashierpassword)

            press_continue_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//fiftytwo-login/login-fields/button")))
            press_continue_button.click()

            await asyncio.sleep(20)
        except Exception as ex:
            print(f"Unexpected: {ex}, {type(ex)=}")

    async def CashierLogOut(self):
        try:
            press_menu_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//fiftytwo-icon/mat-icon[contains(text(), 'menu')]")))
            press_menu_button.click()
            await asyncio.sleep(10)
            press_sign_off_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//mat-icon[contains(text(), 'exit_to_app')]")))
            press_sign_off_button.click()

            await asyncio.sleep(10)
        except Exception as ex:
            print(f"Unexpected: {ex}, {type(ex)=}")
    
