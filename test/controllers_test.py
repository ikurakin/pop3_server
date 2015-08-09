__author__ = 'ikurakin'

from unittest import TestCase
import hashlib

from controllers import DBQueries


class DbQueriesTestCaise(TestCase):

    def setUp(self):
        self.queries = DBQueries()
        self.queries.clear_tables()
        self.queries.fill_users()
        self.queries.fill_emails()

    def tearDown(self):
        self.queries.clear_tables()

    def test_user_exists(self):
        self.assertTrue(self.queries.user_exists("Pablo"))
        self.assertFalse(self.queries.user_exists("Hose"))

    def test_authenticate_user(self):
        self.assertTrue(self.queries.authenticate_user("Pablo", "Pikasso"))
        self.assertFalse(self.queries.authenticate_user("Pablo", "qwerty"))

    def test_passw_hash(self):
        passw_hash = hashlib.sha224("qwerty").hexdigest()
        self.assertEqual(self.queries.passw_hash("qwerty"), passw_hash)
        self.assertNotEqual(self.queries.passw_hash("asdfg"), passw_hash)

    def test_get_user_emails(self):
        self.assertEqual(self.queries.get_user_emails("Khil"), ["1 Khil's email"])
        self.assertNotEqual(self.queries.get_user_emails("Pablo"), ["1 Khil's email"])

    def test_get_email(self):
        expected_subject = "Pablo's email"
        expected_body = ";ksjhdflvkahbdcjsdhbfcsjkdavkjsdhvcakjs"
        subject, body = self.queries.get_email(2)
        self.assertEqual(subject, expected_subject)
        self.assertEqual(body, expected_body)
        subject, body = self.queries.get_email(1)
        self.assertNotEqual(subject, expected_subject)
        self.assertNotEqual(body, expected_body)




