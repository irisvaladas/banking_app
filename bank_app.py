from flask import Flask, request, render_template, redirect, url_for, session
from bank_db_utils import Account

app = Flask(__name__)

@app.route('/customer_details/<customer_ref>')
def get_customer_info(customer_ref):
    cust = Account(customer_ref)
    res = cust.db_get_customer_info()[0]
    return render_template("display.html", account=res)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

#
# Example
# @app.route('/students/<student_id>')
# def get_student_info(student_id):
#     res = db_get_student_info(student_id)
#     return jsonify(res)
#