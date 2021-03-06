import unnittest
from runBrowser_with_options import runffTests as FFTestCase

class firefoxTests(FFTestCase):

    def test01_geturl(self):
        emulatedBrowser.get('http://158.101.173.161/')
        print('Good')

if __name__ == '__main__':
    unittest.main()