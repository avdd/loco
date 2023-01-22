import subprocess
import sys
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # pylint: disable=consider-using-with
        args = [sys.executable, '-m', 'loco.main']
        env = {'LOCO_ENVIRONMENT': 'SELENIUM_TEST'}
        server = subprocess.Popen(args, env=env)
        cls.addClassCleanup(server.wait)
        cls.addClassCleanup(server.terminate)

        opts = webdriver.FirefoxOptions()
        opts.headless = True
        opts.page_load_strategy = 'eager'
        service = Service(log_path='/tmp/geckodriver.log')
        browser = webdriver.Firefox(options=opts, service=service)
        cls.addClassCleanup(browser.quit)
        cls.browser = browser

    def setUp(self):
        self.browser.get('http://localhost:8000/')

    def get_home(self):
        return self.browser.find_element('class name', 'Home')

    def test_redirects_to_home(self):
        self.assertEqual(self.browser.current_url,
                         'http://localhost:8000/home')

    def test_skeleton_empty(self):
        self.assertRaises(NoSuchElementException, self.get_home)

    def test_start_loading_empty(self):
        browser = self.browser
        browser.execute_script('window.__LOCO_SELENIUM_START()')
        self.assertRaises(NoSuchElementException, self.get_home)

    def test_has_stylesheet(self):
        browser = self.browser
        browser.execute_script('window.__LOCO_SELENIUM_START()')
        wait = WebDriverWait(browser, timeout=2)
        wait.until(lambda x: self.get_home())
        n = browser.execute_script('return document.styleSheets.length')
        self.assertGreater(n, 0)
        script = 'return document.getElementById("LocoStylesheet").textContent'
        css = browser.execute_script(script)
        self.assertTrue('.Home' in css)

    def test_page_ready(self):
        browser = self.browser
        browser.execute_script('window.__LOCO_SELENIUM_START()')
        wait = WebDriverWait(browser, timeout=2)
        wait.until(lambda _: self.get_home())
        self.assertEqual(self.get_home().text, 'Hello, world!')


if __name__ == '__main__':
    unittest.main()
