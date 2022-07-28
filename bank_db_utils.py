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

class Customer:
    def __init__(self, custid):
        self.custid = custid

    def db_get_customer_info(self):
        result = None
        db_connection = None
        try:
            db_name = 'bank'
            db_connection = _connect_to_db(db_name)
            cur = db_connection.cursor(dictionary=True)
            print("Connected to DB: %s" % db_name)
            query = """
                SELECT
                    c.fname, c.mname, c.ltname, c.city, c.mobileno, c.occupation, c.dob
                FROM customer c
                where
                c.custid = %s
                """
            data = (self.custid,)
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

    def db_update_costumer_info(self, fname, mname, ltname, city, mobileno, occupation, dob):
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
                where custid = "C00001";
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

#       


ramesh = Customer("C00001")
print(ramesh.db_get_customer_info())