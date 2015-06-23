__author__ = 'Ian Bellamy'

import sys
# TODO: fix this environment variable
sys.path.append('/usr/local/lib/python3.4/dist-packages')

import unittest
import os

import requests
from couchtoes import CouchDB

class TestCouchToEs(unittest.TestCase):

    def setUp(self):
        self.headers = {"User-Agent": "admin:admin"}

    def test_couchdb_is_working(self):
        status = requests.get('http://localhost:5984/', #pronto_spartan',
                              headers=self.headers
                              )
        status.close()
        self.assertTrue(status.status_code == 200)

    def test_couchdb_connnection(self):
        session = CouchDB.connect()#auth=("admin", "admin"))
        self.assertTrue(session.isconnected())
        session.close()

    def test_couch_closing(self):
        session = CouchDB.connect(url='http://localhost:5984/', auth=("admin", "admin"))
        session.close()
        with self.assertRaises(AttributeError):
            session.status

    def test_couch_standard_get(self):
        session = CouchDB.connect(
            url='http://localhost:5984/',
            headers=self.headers
             )
        params = {"limit": 1}
        cursor = session.cursor()
        cursor(view="_all_docs", params=params)
        info = cursor.fetchone()
        print(info)
        info = cursor.fetchone()
        print(info)
        #self.assertGreater()


if __name__ == '__main__':
    unittest.main()




