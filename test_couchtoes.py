__author__ = 'Ian Bellamy'

import unittest
import requests
from couchtoes import *


class TestCouchToEs(unittest.TestCase):

    def setUp(self):
        self.headers = {"User-Agent": "admin:admin"}

    def test_couchdb_is_working(self):
        status = requests.get('http://localhost:5984/',
                              headers=self.headers
                              )
        status.close()
        self.assertTrue(
            status.status_code == 200,
            "Make sure couchdb is running on localhost:5984")

    def test_couchdb_connnection(self):
        session = CouchDB.connect(
            url='http://localhost:5984',
            headers=self.headers)
        self.assertTrue(session.isconnected())
        session.close()

    def test_couch_closing(self):
        session = CouchDB.connect(
            url='http://localhost:5984',
            headers=self.headers)
        session.close()
        with self.assertRaises(AttributeError):
            session.status

    def test_couch_standard_get(self):
        session = CouchDB.connect(
            url='http://localhost:5984',
            headers=self.headers
        )
        params = {"limit": 1}
        cursor = session.cursor()
        cursor(view="pronot_spartan/_all_docs", params=params)
        info = cursor.fetchone()
        self.assertEqual(len(info), 3)

    def test_raises_error_on_wrong_view(self):
        # certain view documents, such as _design/view, do not have rows
        session = CouchDB.connect(
            url='http://localhost:5984',
            headers=self.headers
        )
        cursor = session.cursor()
        with self.assertRaises(DataError):
            cursor(view="pronot_spartan/_design/sales", params={"limit": 100})

if __name__ == '__main__':
    unittest.main()
