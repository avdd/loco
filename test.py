import sys
import subprocess
from selenium import webdriver

server = subprocess.Popen([sys.executable, 'main.py'])

opts = webdriver.FirefoxOptions()
opts.headless = True
browser = webdriver.Firefox(options=opts)
browser.get('http://localhost:8000/')

assert browser.current_url == 'http://localhost:8000/home'

p = browser.find_element('tag name', 'p')
assert p.text == 'Hello, world!'

browser.close()
server.terminate()
