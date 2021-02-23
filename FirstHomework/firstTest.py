import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class MyFirstTestCase(unittest.TestCase):

    def setUp(self):
        self.emulatedBrowser = webdriver.Firefox()

    def tearDown(self):
        self.emulatedBrowser.quit()

    def test01_navigate_and_search(self):
        '''
        First test to try GitHub + PyCharm + PyUnit
        '''
        findField = False
        with self.emulatedBrowser as ff:
            ff.get('https://google.com')
            findField = ff.find_element_by_name('q')
        self.assertTrue(findField)


if __name__ == '__main__':
    unittest.main()
