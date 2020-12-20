from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
# Define Browser Options


class MyseleniumClass:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('log-level=3')
        chrome_path = r'C:\chromedriver\chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        self.htmltext = ''

    def GetHtmlsource(self, url):
        try:
            self.driver.get(url)
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Wait to load the page
                # Calculate new scroll height and compare with last height.
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            self.htmltext = self.driver.page_source
            # self.driver.quit()
            return self.htmltext
        except TimeoutException as ex:
            print(str(ex))


# Scroll page to load whole content


