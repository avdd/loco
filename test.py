import os
import sys
import subprocess
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.support.wait import WebDriverWait


class Test(unittest.TestCase):

    def start_server(self):
        main = os.path.join(os.path.dirname(__file__), 'main.py')
        # pylint: disable=consider-using-with
        server = subprocess.Popen([sys.executable, main])
        self.enterContext(server)
        self.addCleanup(server.terminate)

    def start_browser(self):
        opts = webdriver.FirefoxOptions()
        opts.headless = True
        browser = webdriver.Firefox(options=opts)
        self.addCleanup(browser.quit)
        browser.get('http://localhost:8000/')
        self.browser = browser

    def get_root(self):
        return self.browser.find_element('id', 'AppRoot')

    def setUp(self):
        self.start_server()
        self.start_browser()

    def test_redirects_to_home(self):
        self.assertEqual(self.browser.current_url,
                         'http://localhost:8000/home')

    @unittest.skip('todo')
    def test_skeleton_html(self):
        self.assertRaises(NoSuchElementException, self.get_root)

        # browser.execute_script('StartLoadingForTesting()')
        # wait = WebDriverWait(browser, timeout=5)

        # p = browser.find_element('tag name', 'p')
        # assert p.text == 'Hello, world!'


if __name__ == '__main__':
    unittest.main()
