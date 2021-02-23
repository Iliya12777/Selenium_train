import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class MyFirstTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.emulatedBrowser = webdriver.Firefox()
        wait = WebDriverWait(self.emulatedBrowser, 10)

    @classmethod
    def tearDownClass(self):
        self.emulatedBrowser.quit()

    def test01_navigate_and_search(self):
        '''
        First test to try GitHub + PyCharm + PyUnit
        '''
        with self.emulatedBrowser as ff:
            ff.get('https://google.com')
            findField = ff.find_element_by_name('q')
        self.assertTrue(findField)


if __name__ == '__main__':
    unittest.main()
