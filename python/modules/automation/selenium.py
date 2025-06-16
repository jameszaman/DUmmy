from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumCustom:
    def __init__(self, headless=False):
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")

        # Automatically download and use drivers. GeckoDriverManager is for Firefox.
        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=options)
    
    def go_to(self, url):
        self.driver.get(url)
    
    def select(self, selector):
        return self.driver.find_elements(By.CSS_SELECTOR, selector)
    
    def wait_load_complete(self):
        WebDriverWait(self.driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")

    def sleep(self, seconds):
        sleep(seconds)

    def close(self):
        print("Closing the browser")
        if self.driver:
            self.driver.quit()
            self.driver = None
