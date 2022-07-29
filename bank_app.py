from flask import Flask, request, render_template, redirect, url_for, session
from bank_db_utils import Account

app = Flask(__name__)

app.secret_key = "super secret key"


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/options')
def options():
    return render_template('options.html', account_id=session['account_id'])


@app.route("/login", methods=['GET','POST'])
def login():
    msg=''
    if request.method == 'POST':
        account_id = request.form['account_id']
        password = request.form['password']
        cust = Account(account_id)
        record = cust.db_customer_login(password)
        if record:
            session['loggedin'] = True
            session['account_id'] = record
            return redirect(url_for('options'))
        else:
            msg='Incorrect account number/ password. Try again!'
    return render_template('index.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route('/customer_details/<account_id>')
def get_customer_info(account_id):
    cust = Account(account_id)
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