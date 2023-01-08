import unittest
from werkzeug.test import Client

from loco import main


class Test(unittest.TestCase):

    def test_redirects_to_home(self):
        cli = Client(main.app)
        rsp = cli.get('/')
        self.assertEqual(rsp.status_code, 302)
        self.assertEqual(rsp.headers.get('location'), '/home')

    def test_not_found(self):
        cli = Client(main.app)
        rsp = cli.get('/fooooo')
        self.assertEqual(rsp.status_code, 404)

    def test_skeleton(self):
        skeleton_html = '<script>'
        main.SKELETON_HTML = skeleton_html
        cli = Client(main.app)
        rsp = cli.get('/home')
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.text, skeleton_html)

    def test_environment_cookie(self):
        cli = Client(main.app)
        rsp = cli.get('/')
        cookie = rsp.headers.get('set-cookie')
        self.assertTrue(cookie)
        self.assertIn('LOCO_ENVIRONMENT=development', cookie)


if __name__ == '__main__':
    unittest.main()