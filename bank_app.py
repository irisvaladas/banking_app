from flask import Flask, request, render_template, redirect, url_for, session
from bank_db_utils import Account, Transactions, Bank
from datetime import datetime
import requests
import json
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
        if record:
            session['loggedin'] = True
            session['account_id'] = record
            return redirect(url_for('options'))
        else:
            msg='Incorrect account number/ password. Try again!'
    return render_template('index.html', msg=msg)

@app.route('/register')
def register():
    return render_template("register.html")
@app.route('/registration', methods = ['GET','POST'])
def registration():
    if request.method == 'POST':
        fname = request.form["account_first_name"]
        lname = request.form["account_last_names"]
        address = request.form["account_holder_address"]
        city = request.form["account_city"]
        mobno = request.form["account_holder_mobno"]
        dob = request.form["account_holder_dob"]
        balance = request.form["account_balance"]
        overdraft = request.form["overdraft_amount"]
        account_type = request.form["account_type"]
        if account_type=="Savings account":
            account_type=1
        elif account_type=="Savings account":
            account_type=2
        password = request.form["password"]
        Account().db_create_customer(
            (fname, lname, address, city, mobno, dob, password))
        gen_id = Account().db_get_generated_id()['max(account_id)']
        Account().db_create_account((balance,overdraft,account_type,gen_id))
        return render_template('index.html')

@app.route('/update', methods = ['GET','POST'])
def update():
    if 'loggedin' in session:
        if request.method == 'POST':
            fname = request.form["account_first_name"]
            lname = request.form["account_last_name"]
            address = request.form["account_holder_address"]
            city = request.form["account_city"]
            mobno = request.form["account_holder_mobno"]
            dob = request.form["account_holder_dob"]
            password = request.form["password"]
            Account().db_update_costumer_account((fname,lname,address,city,mobno,dob,password,session['account_id'][0]['account_id']))
        return render_template('update.html', account_id=session['account_id'])

@app.route('/options')
def options():
    username = Account().db_get_customer_info(session['account_id'][0]['account_id'])
    account_balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
    currencies = requests.get("http://api.frankfurter.app/currencies").json()
    return render_template('options.html', account_balance=account_balance, currencies=currencies, username=username)

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

@app.route('/withdrawal', methods=['GET','POST'])
def withdrawal():
    if 'loggedin' in session:
        balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
        return render_template('withdraw.html', balance=balance)

@app.route('/make_withdrawal', methods=['GET','POST'])
def make_withdrawal():
    if 'loggedin' in session:
        amount = 0
        if request.method == 'POST':
            amount = int(request.form['withdraw'])
            print(amount)
            Transactions().withdraw((session['account_id'][0]['account_id'], amount, session['account_id'][0]['account_id']))
            Transactions().update_transactions((0,session['account_id'][0]['account_id'],datetime.today().strftime('%Y-%m-%d'), 'Withdrawal', amount ))
            balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
            return render_template('withdraw.html', balance=balance)
    return render_template('index.html')


@app.route('/deposit', methods=['GET','POST'])
def deposit():
    if 'loggedin' in session:
        balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
        return render_template('deposit.html', balance=balance)

@app.route('/make_deposit', methods=['GET','POST'])
def make_deposit():
    if 'loggedin' in session:
        if request.method == 'POST':
            amount = int(request.form['deposit'])
            Transactions().deposit((session['account_id'][0]['account_id'], amount, session['account_id'][0]['account_id']))
            Transactions().update_transactions((0,session['account_id'][0]['account_id'],datetime.today().strftime('%Y-%m-%d'), 'Deposit', amount ))
            balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
            return render_template('deposit.html', balance=balance)
    return render_template('index.html')

@app.route('/currency_exchange', methods=['GET','POST'])
def currency_exchange():
    if 'loggedin' in session:
        if request.method == "POST":
            currency=request.form["currency"]
            username = Account().db_get_customer_info(session['account_id'][0]['account_id'])
            account_balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
            value = Bank().balance_currency_exchange(currency,session['account_id'][0]['account_id'])
            currencies = requests.get("http://api.frankfurter.app/currencies").json()
            return render_template('options.html', value=value, currencies=currencies, currency=currency, account_balance=account_balance, username=username)
    return render_template('index.html')

@app.route('/delete_account', methods=['GET','POST'])
def delete_account():
    if "loggedin" in session:
        if request.method == "POST":
            account_id = request.form['account_id']
            password = request.form['password']
            record = Account().db_customer_login((account_id, password))
            if record:
                Account().delete_account((account_id, password))
                return redirect(url_for('index'))
            else:
                msg = 'Incorrect account number/ password. Try again!'
            return render_template('delete_account.html', msg=msg)
    return render_template('delete_account.html')


@app.route('/delete')
def delete():
    return render_template('delete_account.html')


@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)

