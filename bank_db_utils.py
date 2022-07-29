import mysql.connector
from config import USER, PASSWORD, HOST


class DbConnectionError(Exception):
    pass


def _connect_to_db(db_name):
    cnx = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=db_name
    )
    return cnx

class Account:
    def __init__(self, account_id):
        self.account_id = account_id

    def db_get_customer_info(self):
        result = None
        db_connection = None
        try:
            db_name = 'bank_app'
            db_connection = _connect_to_db(db_name)
            cur = db_connection.cursor(dictionary=True)
            print("Connected to DB: %s" % db_name)
            query = """
                SELECT
                    *
                FROM customer_details 
                where
                customer_ref = %s
                """
            data = (self.account_id,)
            cur.execute(query, data)
            result = cur.fetchall()  # this is a list with db records where each record is a tuple
            cur.close()
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        finally:
            if db_connection:
                db_connection.close()
                print("DB connection is closed")
            return result

    def db_customer_login(self):
        result = None
        db_connection = None
        try:
            db_name = 'bank_app'
            db_connection = _connect_to_db(db_name)
            cur = db_connection.cursor(dictionary=True)
            print("Connected to DB: %s" % db_name)
            query = """
                SELECT
                    *
                FROM sec_p 
                where
                account_id = %s
                """
            data = (self.account_id,)
            cur.execute(query, data)
            result = cur.fetchall()  # this is a list with db records where each record is a tuple
            cur.close()
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        finally:
            if db_connection:
                db_connection.close()
                print("DB connection is closed")
            return result

    def db_update_costumer_account(self, fname, mname, ltname, city, mobileno, occupation, dob):
        self.fname = fname
        self.mname = mname
        self.ltname = ltname
        self.city = city
        self.mobileno = mobileno
        self.occupation = occupation
        self.dob = dob
        db_connection = None
        try:
            db_name = 'bank'
            db_connection = _connect_to_db(db_name)
            cur = db_connection.cursor()
            print("Connected to DB: %s" % db_name)
            query = """
                UPDATE customer
                Set fname = %s, mname = %s, ltname = %s, city = %s, mobileno = %s, occupation = %s, dob = %s
                where custid = %s;
                """
            data = (fname, mname, ltname, city, mobileno, occupation, dob)
            cur.executemany(query, data)  # this is a list with db records where each record is a tuple
            db_connection.commit()
            cur.close()
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        finally:
            if db_connection:
                db_connection.close()
                print("DB connection is closed")


# class Transactions():
#
#
# class Bank:
#



ramesh = Account(6623)
print(ramesh.db_get_customer_info())