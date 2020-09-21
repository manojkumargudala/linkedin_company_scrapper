import time


import selenium.webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait
import commonutils.common as common

class Scraper(object):

    def __init__(self, cookie=None, scraperInstance=None, driver=selenium.webdriver.Chrome, driver_options={},
                 scroll_pause=0.1, scroll_increment=300, timeout=10):
        if type(self) is Scraper:
            raise Exception(
                'Scraper is an abstract class and cannot be instantiated directly')

        if scraperInstance:
            self.was_passed_instance = True
            self.driver = scraperInstance.driver
            self.scroll_increment = scraperInstance.scroll_increment
            self.timeout = scraperInstance.timeout
            self.scroll_pause = scraperInstance.scroll_pause
            return

        self.was_passed_instance = False
        self.driver = driver(**driver_options)
        self.scroll_pause = scroll_pause
        self.scroll_increment = scroll_increment
        self.timeout = timeout
        self.driver.get('http://www.linkedin.com')
        self.driver.set_window_size(1920, 1080)
        self.login(common.linkedin_login_user_name, common.linkedin_password )

    def wait(self, condition):
        return WebDriverWait(self.driver, self.timeout).until(condition)

    def wait_for_el(self, selector):
        return self.wait(EC.presence_of_element_located((
            By.CSS_SELECTOR, selector
        )))

    def wait_for_el_xpath(self, selector):
        return self.wait(EC.presence_of_element_located((
            By.XPATH, selector
        )))

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.quit()

    def quit(self):
        if self.driver and not self.was_passed_instance:
            self.driver.quit()

    def login(self, email, password):
        self.driver.find_element_by_xpath("//a[text()='Sign in']").click()
        time.sleep(5)
        timeout=1500;
        self.driver.implicitly_wait(10)  # seconds
        email_input_element=''
        password_input_element=''
        try :
            #WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#username')))
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'input#username'))
            WebDriverWait(self.driver, timeout).until(element_present)
            email_input_element = self.driver.find_element_by_css_selector('input#username')
        except NoSuchElementException:
            email_input_element = self.driver.find_element_by_css_selector('input#session_key')
        try :
            #WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(By.CSS_SELECTOR, 'input#password'))
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password'))
            WebDriverWait(self.driver, timeout).until(element_present)
            password_input_element = self.driver.find_element_by_css_selector(
                'input#password')
        except NoSuchElementException:
            password_input_element = self.driver.find_element_by_css_selector(
                'input#session_password')

        email_input_element.send_keys(email)
        password_input_element.send_keys(password)
        #print("test"+email_input_element.get_attribute("value"))
        #print("test123"+password_input_element.get_attribute("value"))
        password_input_element.send_keys(Keys.ENTER)
        #wait(EC.alert_is_present())