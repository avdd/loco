import unittest
from unittest.mock import patch, mock_open
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

    def test_environment_cookie(self):
        cli = Client(main.hello)
        rsp = cli.get('/')
        cookie = rsp.headers.get('set-cookie')
        self.assertTrue(cookie)
        self.assertIn('LOCO_ENVIRONMENT=development', cookie)

    def test_static(self):
        data = 'blah'
        cli = Client(main.hello)
        with patch('builtins.open', mock_open(read_data=data)):
            rsp = cli.get('/app.js')
            self.assertEqual(rsp.text, data)


if __name__ == '__main__':
    unittest.main()
