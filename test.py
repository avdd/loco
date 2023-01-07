import os
import sys
import subprocess
from selenium import webdriver

path = os.path.dirname(__file__)
main = os.path.join(path, 'main.py')

with subprocess.Popen([sys.executable, main]) as server:

    opts = webdriver.FirefoxOptions()
    opts.headless = True
    with webdriver.Firefox(options=opts) as browser:
        browser.get('http://localhost:8000/')

        assert browser.current_url == 'http://localhost:8000/home'

        p = browser.find_element('tag name', 'p')
        assert p.text == 'Hello, world!'

    server.terminate()
