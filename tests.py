import os
import unittest

from banking_app import bank_app, bank_db_utils, bank_main

TEST_BANK_DB = 'test.bank_db_utils'


class BankTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        bank_app.config['TESTING'] = True
        bank_app.config['WTF_CSRF_ENABLED'] = False
        bank_app.config['DEBUG'] = False
        bank_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['BASEDIR'], TEST_BANK_DB)
        self.bank_app = bank_app.test_client()
        db.drop_all()
        db.create_all()


# Disable sending emails during unit testing
mail.init_app(bank_app)
self.assertEqual(app.debug, False)


# executed after each test
def tearDown():
    pass


# tests #


def test_main_page(self):
    response = self.bank_app.get('/', follow_redirects=True)
    self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()