import mysql.connector
from config import USER, PASSWORD, HOST
import requests


class DbConnectionError(Exception):
    pass

class Database:
    cnx = cur = None

    def __init__(self):
        global cnx, cur
        cnx = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database="bank_app"
        )
        cur = cnx.cursor(dictionary=True)

    def __del__(self):
        cnx.commit()


class Account(Database):
    def db_get_customer_info(self,account_id):
        result = ""
        query = "SELECT * from customer_details where account_id = {}".format(account_id)

        try:
            cur.execute(query)
            result = cur.fetchone()  # this is a list with db records where each record is a tuple
            return result
        except Exception:
            raise DbConnectionError("Failed to read data from DB")

    def db_customer_login(self, data):
        result = ""
        query = """
                        SELECT
                            account_id,password
                        FROM customer_details 
                        where
                        account_id = %s and password = %s
                        """
        try:
            cur.execute(query,data)
            result = cur.fetchall()  # this is a list with db records where each record is a tuple
            return result
        except Exception:
            raise DbConnectionError("Failed to read data from DB")

    def db_update_costumer_account(self, data):
        query = """
                        UPDATE customer_details
                        Set account_first_name = %s, account_last_name = %s, account_holder_address = %s, account_city = %s, 
                        account_holder_mobno = %s, account_holder_dob = %s, password = %s
                        where account_id = %s;
                        """
        try:
            cur.execute(query, data)  # this is a list with db records where each record is a tuple
            cnx.commit()
        except Exception:
            raise DbConnectionError("Failed to read data from DB")

    def db_create_customer(self, data):
        query = """INSERT INTO customer_details 
        VALUES(null,%s,%s,%s,%s,%s,%s,%s);"""
        try:
            cur.execute(query, data)  # this is a list with db records where each record is a tuple
            cnx.commit()
        except Exception:
            raise DbConnectionError("Failed to read data from DB")

    def db_get_generated_id(self):
        result = ""
        query = """select max(account_id) from customer_details"""
        try:
            cur.execute(query)  # this is a list with db records where each record is a tuple
            result=cur.fetchone()
            return result
        except Exception:
            raise DbConnectionError("Failed to read data from DB")

    def db_create_account(self, data):
        query = """Update accounts set account_balance = %s, 
        overdraft_amount = %s, account_type_id = %s where account_id = %s;
        """
        try:
            cur.execute(query, data)  # this is a list with db records where each record is a tuple
            cnx.commit()
        except Exception:
            raise DbConnectionError("Failed to read data from DB")

    def show_balance(self, account_id):
        result = ""
        query = f"SELECT account_balance from accounts where account_id = {account_id};"
        try:
            cur.execute(query)
            result = cur.fetchone()  # this is a list with db records where each record is a tuple
            return result
        except Exception:
            raise DbConnectionError("Failed to read data from DB")


    def delete_account(self, data):
        query = """Delete from Customer_details where account_id = %s and password = %s
        """
        try:
            cur.execute(query, data)
            cnx.commit()
        except Exception:
            raise DbConnectionError("Failed to read data from DB")


class Transactions(Account):
    def db_get_customer_transactions(self, data):
        result=""
        query = """SELECT * from trandetails 
        where account_id = %s 
        AND dot between %s and %s;"""
        # AND dot between cast( % s as date) and cast( % s as date);"""
        try:
            cur.execute(query,data)
            result = cur.fetchall()  # this is a list with db records where each record is a tuple
            return result
        except Exception:
            raise DbConnectionError("Failed to read data from DB")


    def withdraw(self, data):
        query = """update accounts set account_balance = ((select account_balance where account_id = %s) - %s) 
                   where account_id = %s;"""
        if (self.show_balance(data[0]))['account_balance'] >= data[1]:
            try:
                cur.execute(query, data)
                cnx.commit()
            except Exception:
                raise DbConnectionError("Failed to read data from DB")


    def deposit(self, data):
        query = """update accounts set account_balance = ((select account_balance where account_id = %s) + %s) 
                   where account_id = %s;"""
        try:
            cur.execute(query, data)
            cnx.commit()
        except Exception:
            raise DbConnectionError("Failed to read data from DB")


    def update_transactions(self, data):
        query = """INSERT INTO trandetails 
        VALUES(%s,%s,%s,%s,%s);"""
        try:
            cur.execute(query, data)
            cnx.commit()
        except Exception:
            raise DbConnectionError("Failed to read data from DB")

class Bank(Account):
    def balance_currency_exchange(self, to_currency, account_id):
        from_currency = 'GBP'
        balance = float(self.show_balance(account_id).get('account_balance'))
        result = requests.get(
            f"https://api.frankfurter.app/latest?amount={balance}&from={from_currency}&to={to_currency}")
        return result.json()['rates'][to_currency]

print(Bank().balance_currency_exchange("EUR",20001))