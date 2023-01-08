import unittest
from werkzeug.test import Client

from main import hello


class Test(unittest.TestCase):

    def test_redirects_to_home(self):
        cli = Client(hello)
        rsp = cli.get('/')
        self.assertEqual(rsp.status_code, 302)
        self.assertEqual(rsp.headers.get('location'), '/home')


if __name__ == '__main__':
    unittest.main()
