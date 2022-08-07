import mysql.connector
from config import USER, PASSWORD, HOST


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
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        finally:
            return result

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
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        finally:
            return result

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

    def show_balance(self, account_id):
        result = ""
        query = f"SELECT account_balance from accounts where account_id = {account_id};"

        try:
            cur.execute(query)
            result = cur.fetchone()  # this is a list with db records where each record is a tuple
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        return result


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
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        finally:
            return result

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


# class Bank:
#
# camille = Account()
# print(camille.show_balance(223344))
# trans1 = Transactions()
# # trans1.withdraw((223344, 100, 223344))
# trans1.deposit((223344, 100, 223344))
# trans1 = Transactions()
#print(camille.db_get_customer_info(223344))