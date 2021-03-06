import unittest
#import webdriver
from selenium import webdriver
#import needed for options, while running FF
from selenium.webdriver.firefox.options import Options

class runffTests(unittest.TestCase):
    @classmethod
    def setUp(cls):
        options = Options()
        # Can make browser invisible, not needed in phase of training
        options.headless = False
        options.add_argument('-console -foreground -new-instance')
        cls.emulatedBrowser = webdriver.Firefox(options=options)

    @classmethod
    def tearDown(cls):
        cls.emulatedBrowser.quit()

if __name__ == '__main__':
    unittest.main()
