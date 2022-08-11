from flask import Flask, request, render_template, redirect, url_for, session
from bank_db_utils import Account, Transactions, Bank
from datetime import datetime
import requests


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
    elif account_type=="Current account":
        account_type=2
    password = request.form["password"]

    def password_ver(pas):
        password_check = Account().password_check(pas)
        if not password_check:
            msg = """
            Invalid password:
            From 6 to 20 characters long;
            At least one num;
            At least one uppercase;
            At least one lowercase;
            At least one of this symbols($@#)
            """
            return render_template('register.html', msg=msg)
        if password_check:
            Account().db_create_customer(
                (fname, lname, address, city, mobno, dob, password))
            gen_id_msg = f"Your account ID is {Account().db_get_generated_id()['max(account_id)']}, please save it somewhere safe."
            gen_id = Account().db_get_generated_id()['max(account_id)']
            Account().db_create_account((balance, overdraft, account_type, gen_id))
            return render_template('register.html', gen_id=gen_id_msg)
    return password_ver(password)


@app.route('/update')
def update():
    if 'loggedin' in session:
        return render_template("update.html")

@app.route('/update_details', methods = ['GET','POST'])
def update_details():
    if 'loggedin' in session:
        fname = request.form["account_first_name"]
        lname = request.form["account_last_names"]
        address = request.form["account_holder_address"]
        city = request.form["account_city"]
        mobno = request.form["account_holder_mobno"]
        dob = request.form["account_holder_dob"]
        password = request.form["password"]

        def password_ver(pas):
            password_check = Account().password_check(pas)
            if not password_check:
                msg = """
                Invalid password:
                From 6 to 20 characters long;
                At least one num;
                At least one uppercase;
                At least one lowercase;
                At least one of this symbols($@#)
                """
                return render_template('update.html',account_id=session['account_id'], msg=msg)
            if password_check:
                Account().db_update_costumer_account(
                    (fname, lname, address, city, mobno, dob, password, session['account_id'][0]['account_id']))
                confirmation = "Your details were updated successfully"
                return render_template('update.html',account_id=session['account_id'], confirmation=confirmation )
        return password_ver(password)
    return render_template("index.html")

@app.route('/options')
def options():
    if "loggedin" in session:
        username = Account().db_get_customer_info(session['account_id'][0]['account_id'])
        account_balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
        currencies = requests.get("http://api.frankfurter.app/currencies").json()
        currencies.pop("GBP")
        return render_template('options.html', account_balance=account_balance, currencies=currencies, username=username)
    return render_template("index.html")

@app.route('/customer_details')
def details():
    if 'loggedin' in session:
        res = Account().db_get_customer_info(session['account_id'][0]['account_id'])
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
            total_spent=f"You didn't spend money in this period of time"
            if [d['transaction_amount'] for d in res if d['transaction_type'] == 'Withdrawal'] == []:
                total_spent = f"You didn't spend money in this period of time"
            elif res:
                total_spent = f"Within this period you spent: {Bank().get_total_spent(res)[-1]} GBP"
            return render_template('transactions.html', account=res, total_spent=total_spent)
    return render_template('index.html')

@app.route('/withdrawal', methods=['GET','POST'])
def withdrawal():
    if 'loggedin' in session:
        balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
        return render_template('withdraw.html', balance=balance)

@app.route('/make_withdrawal', methods=['GET','POST'])
def make_withdrawal():
    if 'loggedin' in session:
        amount = int(request.form['withdraw'])
        msg = ""
        balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
        def check_amount(num):
            balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
            if num <= 0 and balance > num:
                msg = "Please insert amount greater than 0."
                balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
                return render_template('withdraw.html', account_id=session['account_id'], msg=msg, balance=balance)
            elif num > 0 and balance > num:
                Transactions().withdraw((session['account_id'][0]['account_id'], amount, session['account_id'][0]['account_id']))
                Transactions().update_transactions((0,session['account_id'][0]['account_id'],datetime.today().strftime('%Y-%m-%d'), 'Withdrawal', amount ))
                balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
                code = Transactions().withdraw((session['account_id'][0]['account_id'], 0, session['account_id'][0]['account_id']))
                msg = f"To get your money please insert this code: {code} into the ATM"
                return render_template('withdraw.html', balance=balance, msg = msg)
            elif balance < num:
                msg = f"You don't have enough money to complete this transaction"
                return render_template('withdraw.html', balance=balance, msg=msg)
            return render_template('withdraw.html', balance=balance)
        return check_amount(amount)
    return render_template('index.html')


@app.route('/deposit', methods=['GET','POST'])
def deposit():
    if 'loggedin' in session:
        balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
        return render_template('deposit.html', balance=balance)

@app.route('/make_deposit', methods=['GET','POST'])
def make_deposit():
    if 'loggedin' in session:
        amount = int(request.form['deposit'])
        def check_amount(num):
            if num <= 0:
                msg = "Please insert amount greater than 0."
                balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
                return render_template('deposit.html', account_id=session['account_id'], msg=msg, balance=balance)
            elif num > 0:
                Transactions().deposit((session['account_id'][0]['account_id'], amount, session['account_id'][0]['account_id']))
                Transactions().update_transactions((0,session['account_id'][0]['account_id'],datetime.today().strftime('%Y-%m-%d'), 'Deposit', amount ))
                balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
                msg = "Deposit successful"
                return render_template('deposit.html', balance=balance, msg=msg)
        return check_amount(amount)
    return render_template('index.html')

@app.route('/currency_exchange', methods=['GET','POST'])
def currency_exchange():
    if 'loggedin' in session:
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
                balance = Account().show_balance(session['account_id'][0]['account_id'])['account_balance']
                code = Transactions().withdraw((session['account_id'][0]['account_id'], balance, session['account_id'][0]['account_id']))
                msg = f"We are very sorry to see you leaving. To get your money back please insert this code: {code} into the ATM"
                return render_template('index.html', msg=msg)
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

