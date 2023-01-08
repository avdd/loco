import unittest
from werkzeug.test import Client

import main


class Test(unittest.TestCase):

    def test_redirects_to_home(self):
        cli = Client(main.hello)
        rsp = cli.get('/')
        self.assertEqual(rsp.status_code, 302)
        self.assertEqual(rsp.headers.get('location'), '/home')

    def test_skeleton(self):
        skeleton_html = '<script>'
        main.SKELETON_HTML = skeleton_html
        cli = Client(main.hello)
        rsp = cli.get('/home')
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.text, skeleton_html)


if __name__ == '__main__':
    unittest.main()
