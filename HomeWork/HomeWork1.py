import unittest
from selenium import webdriver #import selenium
from selenium.webdriver.common.keys import Keys #import keys
from selenium.webdriver.common.by import By #import By class
from selenium.webdriver.support.ui import WebDriverWait #import wait
from selenium.webdriver.support import expected_conditions as EC #import Expected Conditions
from selenium.webdriver.firefox.options import Options as Options #import options
import re

class HomeWork1(unittest.TestCase):
    """
    2021-03-07 - Added class HomeWork1 rev1
    """

    URL = 'http://158.101.173.161/';
    URLADMIN = 'http://158.101.173.161/admin'
    LOGIN = 'testadmin'
    PASSWORD = 'R8MRDAYT_test'

    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument('--new-instance')
        options.add_argument('--console')
        options.add_argument('--foreground')
        # No option for maximized window found by me, need to c reate profile mock-up
        cls.emulatedBrowser = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.emulatedBrowser.quit()

    def test01_openAdmin(self):
        '''
        Test for opening URL
        '''

        loginSuccess = False
        self.emulatedBrowser.get(self.URLADMIN)
        try:
            WebDriverWait(self.emulatedBrowser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
            loginSuccess = True
            print('Admin page opened')
        except:
            self.emulatedBrowser.quit()
        self.assertTrue(loginSuccess, 'OpenURL Failed')

    def test02_loginAdmin(self):
        '''
        Test for Logging in
        '''
        logined = False
        if not self.emulatedBrowser:
            raise Exception('Browser not found, previous tests may failed')
        self.emulatedBrowser.find_element_by_xpath('//input[@name="username"]').send_keys(self.LOGIN)
        self.emulatedBrowser.find_element_by_xpath('//input[@type="password"]').send_keys(self.PASSWORD)
        self.emulatedBrowser.find_element_by_xpath('//button[@name="login"]').click()
        try:
            WebDriverWait(self.emulatedBrowser, 10).until(EC.presence_of_element_located((By.XPATH, '//li//a[contains(@href, "app")]')))
            logined = True
        except:
            self.emulatedBrowser.quit()
            print('Could not login to admin page, stopping tests')
        self.assertTrue(logined, 'Login to admin page Failed')

    def test03_clickElements(self):
        """
        Test for clicking all elements from left pane
        one by one
        """
        if not self.emulatedBrowser:
            raise Exception('Browser not found, previous tests may failed')
        #make list of all categories
        categories = []
        RegEx = r'.*\?app=(.*)\&'
        RegEx_sub = r'\&doc=(.*)$'
        base_xpath = '//li[contains(@class,"app")]//a[contains(@href, "'
        elements = self.emulatedBrowser.find_elements_by_xpath('//li[@class="app"]//a[contains(@href, "app")]')
        try:
            for element in elements:
                categories.append(re.search(RegEx,element.get_attribute('href')).group(1))
            print(f'Main Categories parsed from site {categories})')
            if categories:
                print('Clicking by categories')
                for categorie in categories:
                    hrefs = self.emulatedBrowser.find_elements_by_xpath(f'{base_xpath + categorie}")]')
                    hrefs[0].click()
                    WebDriverWait(self.emulatedBrowser, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.panel-heading')))
                    hrefs = self.emulatedBrowser.find_elements_by_xpath(f'{base_xpath + categorie}")]')
                    if len(hrefs) > 1:
                        sub_categories = []
                        for href in hrefs[1:]:
                            sub_categories.append(re.search(RegEx_sub, href.get_attribute('href')).group(1))
                        if sub_categories:
                            print(f'Subcategories found {sub_categories}')
                            for sub_categorie in sub_categories:
                                self.emulatedBrowser.find_element_by_xpath(f'//li[@data-code="{sub_categorie}"]/a[contains(@href, "{sub_categorie}")]').click()
                                WebDriverWait(self.emulatedBrowser, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.panel-heading')))
        except:
            raise Exception('Parsing Failed')
        finally:
            print('Page Menu elements were clicked')

if __name__ == '__main__':
    unittest.main()
