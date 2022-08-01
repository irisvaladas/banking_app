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

        query = "SELECT * from customer_details where account_id = {}".format(account_id)

        try:
            cur.execute(query)
            result = cur.fetchone()  # this is a list with db records where each record is a tuple
        except Exception:
            raise DbConnectionError("Failed to read data from DB")

        return result

    def db_customer_login(self, data):
        query = """
                        SELECT
                            *
                        FROM sec_p 
                        where
                        account_id = %s and password = %s
                        """
        try:
            cur.execute(query,data)
            result = cur.fetchall()  # this is a list with db records where each record is a tuple
        except Exception:
            raise DbConnectionError("Failed to read data from DB")

        return result

    # def db_update_costumer_account(self, fname, mname, ltname, city, mobileno, occupation, dob):
    #     self.fname = fname
    #     self.mname = mname
    #     self.ltname = ltname
    #     self.city = city
    #     self.mobileno = mobileno
    #     self.occupation = occupation
    #     self.dob = dob
    #     db_connection = None
    #     try:
    #         db_name = 'bank'
    #         db_connection = _connect_to_db(db_name)
    #         cur = db_connection.cursor()
    #         print("Connected to DB: %s" % db_name)
    #         query = """
    #             UPDATE customer
    #             Set fname = %s, mname = %s, ltname = %s, city = %s, mobileno = %s, occupation = %s, dob = %s
    #             where custid = %s;
    #             """
    #         data = (fname, mname, ltname, city, mobileno, occupation, dob)
    #         cur.executemany(query, data)  # this is a list with db records where each record is a tuple
    #         db_connection.commit()
    #         cur.close()
    #     except Exception:
    #         raise DbConnectionError("Failed to read data from DB")
    #     finally:
    #         if db_connection:
    #             db_connection.close()
    #             print("DB connection is closed")


# class Transactions(Account):

#
#
# class Bank:
#
