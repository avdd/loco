import unittest
from werkzeug.test import Client

from loco import main


class Test(unittest.TestCase):

    def setUp(self):
        registry = main.URL_REGISTRY
        app = main.create_app(registry)
        self.client = Client(app)

    def test_redirects_to_home(self):
        rsp = self.client.get('/')
        self.assertEqual(rsp.status_code, 302)
        self.assertEqual(rsp.headers.get('location'), '/home')

    def test_not_found(self):
        rsp = self.client.get('/foooo')
        self.assertEqual(rsp.status_code, 404)

    def test_skeleton(self):
        skeleton_html = '<script>'
        main.SKELETON_HTML = skeleton_html
        rsp = self.client.get('/home')
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.text, skeleton_html)

    def test_environment_cookie(self):
        rsp = self.client.get('/')
        cookie = rsp.headers.get('set-cookie')
        self.assertTrue(cookie)
        self.assertIn('LOCO_ENVIRONMENT=development', cookie)


if __name__ == '__main__':
    unittest.main()
