from flask import Flask, request, render_template, redirect, url_for, session
from bank_db_utils import Account, Transactions
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

app.secret_key = "super secret key"

@app.route('/')
def index():
    return render_template("index.html")


@app.route("/login", methods=['GET','POST'])
def login():
    msg=''
    if request.method == 'POST':
        account_id = request.form['account_id']
        password = request.form['password']
        record = Account().db_customer_login((account_id, password))
        print(record)
        if record:
            session['loggedin'] = True
            session['account_id'] = record
            return redirect(url_for('options'))
        else:
            msg='Incorrect account number/ password. Try again!'
    return render_template('index.html', msg=msg)


@app.route('/register')
def register():
    msg = ''
    return render_template('register.html', msg=msg)

@app.route('/options')
def options():
    return render_template('options.html', account_id=session['account_id'])

@app.route('/customer_details')
def details():
    if 'loggedin' in session:
        res = Account().db_get_customer_info(session['account_id'][0]['account_id'])
        print(res)
        return render_template("display.html", account=res)
    return render_template('index.html')

@app.route('/transactions', methods=['GET','POST'])
def transactions():
    if 'loggedin' in session:
        return render_template('transactions.html')

@app.route('/select_transactions', methods=['GET','POST'])
def select_transactions():
    if 'loggedin' in session:
        if request.method == 'POST':
            date_from = request.form['date_from']
            date_to = request.form['date_to']
            res = Transactions().db_get_customer_transactions((session['account_id'][0]['account_id'], date_from, date_to))
            return render_template('transactions.html', account=res)
    return render_template('index.html')

@app.route('/withdraw')
def withdraw():
    return render_template('withdraw.html', account_id=session['account_id'])

@app.route('/deposit')
def deposit():
    return render_template('deposit.html', account_id=session['account_id'])

@app.route('/update')
def update():
    return render_template('update.html', account_id=session['account_id'])

@app.route('/delete')
def delete():
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)