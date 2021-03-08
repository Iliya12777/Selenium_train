import unittest
import datetime
import time
from random import choice
from random import randint
from selenium import webdriver #import selenium
from selenium.webdriver.common.by import By #import By class
from selenium.webdriver.support.ui import WebDriverWait #import wait
from selenium.webdriver.support import expected_conditions as EC #import Expected Conditions
from selenium.webdriver.firefox.options import Options as Options #import options


class HomeWork2(unittest.TestCase):
    """
    2021-03-08 - Added class HomeWork2 rev1
    """

    URL = 'http://158.101.173.161/'

    @classmethod
    def setUpClass(cls):
        options = Options()
        # options.add_argument('--new-instance')
        options.add_argument('--console')
        options.add_argument('--foreground')
        cls.emulatedBrowser = webdriver.Firefox()
        cls.emulatedBrowser.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.emulatedBrowser.quit()

    def test01_openPage(self):
        '''
        Test for opening URL
        '''
        print('Trying to load webpage...')
        starttime = datetime.datetime.now()
        pageOpened = False
        self.emulatedBrowser.get(self.URL)
        try:
            WebDriverWait(self.emulatedBrowser, 10).until(EC.presence_of_element_located((By.XPATH, '//img[contains(@src, "rocket-cart")]')))
            pageOpened = True
            print(f'Page loaded in {str(datetime.datetime.now()-starttime)}')
        except:
            self.emulatedBrowser.quit()
        self.assertTrue(pageOpened, 'OpenURL Failed')

    def test02_addDuckstoCart(self):
        '''
        Add random quantity of Ducks to cart
        Wait until Ducks counter is changed
        '''
        ducks_hrefs = []
        bought_ducks = 0
        add_btn = r'//button[@name="add_cart_product"]'
        cart_root = r'//a[contains(@href, "checkout")]//div'
        if not self.emulatedBrowser:
            raise Exception('Browser not found, stopping tests')
        # parse all ducks from Popular Products to get their Unique hrefs
        for duck in self.emulatedBrowser.find_elements_by_xpath('//section[@id="box-popular-products"]//a'):
            ducks_hrefs.append(duck.get_attribute('href'))
        print(f'{"-"*100}')
        print('Unique ducks found at "popular section" with links:')
        print('\n'.join(ducks_hrefs))
        print(f'{"-" * 100}')
        for i in range(randint(1,5)):
            curDuck = choice(ducks_hrefs)
            cart_elem = self.emulatedBrowser.find_element_by_xpath(cart_root)
            starttime = datetime.datetime.now()
            print(f'Navigating to duck {curDuck}')
            self.emulatedBrowser.get(curDuck)
            # waint until page is loaded(add button found)
            WebDriverWait(self.emulatedBrowser, 10).until(
                EC.visibility_of_element_located((By.XPATH, add_btn)))
            print(f'Page loaded in {str(datetime.datetime.now() - starttime)}')
            print(f'Adding duck #{i} in cart...')
            # here we are dealing with maximized browser, and in 1080p accept cookies do not interfer with button
            # but if we can click "accept" will do it
            try:
                accept_cookies = self.emulatedBrowser.find_element_by_xpath('//button[@name="accept_cookies"]')
                accept_cookies.click()
            except:
                print('Cookies button clicked')
            finally:
                self.emulatedBrowser.find_element_by_xpath(add_btn).click()
                print('Button clicked')
                bought_ducks += 1
                WebDriverWait(self.emulatedBrowser, 10).until(EC.staleness_of(cart_elem))
                # here is question
                # in case we do not have implicit sleep staleness of element is too speedy and we can see only animations
                # and empty cart
                time.sleep(2)
                self.emulatedBrowser.back()
                WebDriverWait(self.emulatedBrowser, 10).until(EC.presence_of_element_located((By.XPATH, '//img[contains(@src, "rocket-cart")]')))
            print(f'{"-" * 100}')
            print(f'Bought {i+1} ducks')
            print(f'{"-" * 100}')
        self.assertEqual(i+1, bought_ducks, 'Count of bought ducks and tries of buiyng them differs')


    def test03_deleteDuckfromCart(self):
        """
        Delete all ducks from cart
        """
        btn_remove = r'//button[@title="Remove"]'
        message = r'//div[@id="content"]/p'
        if not self.emulatedBrowser:
            raise Exception('Browser not found, stopping tests')
        # Navigate to checkout page
        self.emulatedBrowser.get('http://158.101.173.161/checkout')
        WebDriverWait(self.emulatedBrowser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@name="confirm_order"]')))
        print('Loaded checkout page')
        DucksCount = len(self.emulatedBrowser.find_elements_by_xpath(btn_remove))
        print(f'Evaluated count of unique ducks to be deleted - {DucksCount} ducks')
        for i in range(DucksCount):
            ducks_buttons = self.emulatedBrowser.find_element_by_xpath('//button[@name="confirm_order"]')
            self.emulatedBrowser.find_element_by_xpath(btn_remove).click()
            WebDriverWait(self.emulatedBrowser, 10).until(EC.staleness_of(ducks_buttons))
            print(f'Deleted duck#{i} from cart')
        WebDriverWait(self.emulatedBrowser, 10).until(EC.presence_of_element_located((By.XPATH, message)))
        self.assertEqual(self.emulatedBrowser.find_element_by_xpath(message).text, r'There are no items in your cart.',
                         'Something went wrong while deleting ducks')
        print('Cart is empty')

if __name__ == '__main__':
    unittest.main()
