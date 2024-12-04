import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv

import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

URL = "https://px6.me/"

login_email = os.getenv('PROXY_EMAIL')
login_pass = os.getenv('PROXY_PASSWORD')


# maintain options
options = Options()
options.add_argument('--window-size=1524,1580')
# options.add_argument('--headless')
options.add_argument('--incognito')
options.add_argument('--disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--disable-notifications')
options.add_argument('--disable-default-apps')
options.add_argument('--disable-bundled-ppapi-flash')
options.add_argument('--disable-modal-animations')
options.add_argument('--disable-login-animations')
options.add_argument('--disable-pull-to-refresh-effect')
options.add_argument('--autoplay-policy=document-user-activation-required')

# Enable images
options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1,
              "profile.managed_default_content_settings.images": 2})  # '1' - enables images; '2' - disables

options.add_experimental_option("excludeSwitches", ["enable-logging"])

# max waiting time for load page
timeout_waits = 10

#locators
login_button = 'a[data-role="login"]'
email_prop = 'input[type="email"]'
pass_prop = 'input[type="password"]'
captcha_anchor = '#recaptcha-anchor'

def wait_for_element(driver, selector, timeout=timeout_waits):
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
    except Exception as e:
        logging.error(f"Timeout waiting for element {selector}: {e}")
        return None

def handle_page():
    driver = webdriver.Chrome(options=options)
    driver.get(URL)

    try:
        login = driver.find_element(By.CSS_SELECTOR, login_button) # click cookie accept button
        login.click()
    except NoSuchElementException:
        logging.error('Login button does not exist')

    try:
        email_field = WebDriverWait(driver, timeout_waits).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, email_prop))
        )
        password_field = WebDriverWait(driver, timeout_waits).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, pass_prop))
        )
        email_field.send_keys(login_email)
        password_field.send_keys(login_pass)
        logging.info('Email & password passed SUCCESS!')
        recaptcha = wait_for_element(driver, captcha_anchor)
    except NoSuchElementException as e:
        logging.error(f"Email input or pass doesn't exist | error: {e}")


    time.sleep(20) # TODO: remove it
    driver.quit()
handle_page()