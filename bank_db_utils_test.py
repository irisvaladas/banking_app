import unittest
from bank_db_utils import Account, Transactions, Bank
from datetime import datetime


class Test(unittest.TestCase):

    def test_db_get_customer_info(self):
        expected = dict
        returned = type(Account().db_get_customer_info(20008))
        self.assertEqual(expected, returned)

    def test_db_get_customer_info_error(self):
        expected = None
        returned = Account().db_get_customer_info(20000)
        self.assertEqual(expected, returned)

    def test_db_customer_login(self):
        expected = [{'account_id': 20008, 'password': 'rVr5RR678*vO#x'}]
        returned = Account().db_customer_login((20008,"rVr5RR678*vO#x"))
        self.assertEqual(expected, returned)

    def test_db_customer_login_error(self):
        expected = []
        returned = Account().db_customer_login((20008,"123654"))
        self.assertEqual(expected, returned)

    def test_db_update_costumer_account(self):
        expected = None
        returned = Account().db_update_costumer_account(("Tested","expected","test address","test city",123456789,"1999-02-01","rVr5RR678*vO#x",20008))
        self.assertEqual(expected, returned)

    def test_db_update_costumer_account_error(self):
        expected = None
        returned = Account().db_update_costumer_account(("Tested","expected","test address","test city",123456789,"1999-02-01","rVr5RR678*vO#x",20000))
        self.assertEqual(expected, returned)



    def test_db_get_generated_id(self):
        expected = Account().db_get_generated_id()
        returned = Account().db_get_generated_id()
        self.assertEqual(expected, returned)

    def test_db_create_account(self):
        expected = None
        returned = Account().db_create_account((1000,1000,1,20008))
        self.assertEqual(expected, returned)

    def test_db_create_account_error(self):
        expected = None
        returned = Account().db_create_account((1000,1000,1,22222))
        self.assertEqual(expected, returned)

    def test_show_balance(self):
        expected = dict
        returned = type(Account().show_balance((20008)))
        self.assertEqual(expected, returned)

    def test_show_balance_error(self):
        expected = None
        returned = Account().show_balance((22222))
        self.assertEqual(expected, returned)

    def test_overdraft_amount(self):
        expected = {'overdraft_amount': 1000.0}
        returned = Account().overdraft_amount((20008))
        self.assertEqual(expected, returned)

    def test_overdraft_amount_error(self):
        expected = None
        returned = Account().overdraft_amount((22222))
        self.assertEqual(expected, returned)

    def test_password_check(self):
        expected = True
        returned = Account().password_check("Ab#12asdf")
        self.assertEqual(expected, returned)

    def test_password_check_error(self):
        expected = None
        returned = Account().password_check("123456")
        self.assertEqual(expected, returned)

    def test_db_get_customer_transactions(self):
        expected = list
        returned = type(Transactions().db_get_customer_transactions(("20008", "2000-01-01", datetime.today().strftime('%Y-%m-%d'))))
        self.assertEqual(expected, returned)

    def test_db_get_customer_transactions_error(self):
        expected = []
        returned = Transactions().db_get_customer_transactions(("20000", "2000-01-01", datetime.today().strftime('%Y-%m-%d')))
        self.assertEqual(expected, returned)

    def test_withdraw(self):
        expected = str
        returned = type(Transactions().withdraw((20008,100,20008)))
        self.assertEqual(expected, returned)

    def test_deposit(self):
        expected = None
        returned = Transactions().deposit((20008,100,20008))
        self.assertEqual(expected, returned)

    def test_deposit_error(self):
        expected = None
        returned = Transactions().deposit((20008,100,20008))
        self.assertEqual(expected, returned)

    def test_update_transactions(self):
        expected = None
        returned = Transactions().update_transactions((0,20008,datetime.today().strftime('%Y-%m-%d'), 'Withdrawal', 100 ))
        self.assertEqual(expected, returned)

    def test_update_transactions_error(self):
        expected = None
        returned = Transactions().update_transactions((0,20008,datetime.today().strftime('%Y-%m-%d'), 'Withdrawal', 100 ))
        self.assertEqual(expected, returned)

    def test_balance_currency_exchange(self):
        expected = float
        returned = type(Bank().balance_currency_exchange("EUR",20008))
        self.assertEqual(expected, returned)

    def test_delete_account_b(self):
        expected = None
        returned = Account().delete_account((Account().db_get_generated_id()['max(account_id)']+1,"rVr5RR678*vO#x"))
        self.assertEqual(expected, returned)

    def test_delete_account_error(self):
        expected = None
        returned = Account().delete_account((22222,"156324"))
        self.assertEqual(expected, returned)

    def test_delete_transactions(self):
        expected = None
        returned = Account().delete_transactions(20008)
        self.assertEqual(expected, returned)

    def test_delete_transactions_error(self):
        expected = None
        returned = Account().delete_transactions((20000))
        self.assertEqual(expected, returned)

    # def test_delete_bank_account(self):
    #     expected = None
    #     returned = Account().delete_bank_account(20008)
    #     self.assertEqual(expected, returned)

    def test_delete_bank_account_error(self):
        expected = None
        returned = Account().delete_bank_account((20000))
        self.assertEqual(expected, returned)

    def test_db_create_customer(self):
        expected = None
        returned = Account().db_create_customer(("Test","expected","test address","test city",123456789,"1999-02-01","rVr5RR678*vO#x"))
        self.assertEqual(expected, returned)

    def test_db_create_customer_error(self):
        expected = None
        returned = Account().db_create_customer(("Test","expected","test address","test city",123456789,"1999-02-01","rVr5RR678*vO#x"))
        self.assertEqual(expected, returned)



if __name__ == '__main__':
    unittest.main()