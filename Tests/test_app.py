import requests

url = "http://127.0.0.1:5001/"
session = requests.Session()
session.post(url=f'{url}login', data={'account_id': 20001, 'password': "isRx$^6L8*3*#"})


def test_request_login():
    response = requests.get(url)
    assert 'Login' in response.text


def test_request_login_post():
    response = requests.post(f'{url}login', data={'account_id': 1, 'password': 1})
    assert 'Incorrect account number/ password' in response.text


def test_request_login_post_auth():
    response = requests.post(f'{url}options', data={'account_id': 20001, 'password': "isRx$^6L8*3*#"})
    assert response.url == f'{url}options'


def test_request_register():
    response = requests.get(f'{url}register')
    assert 'Sign up for an account' in response.text


def test_request_registration_no_data():
    response = requests.post(f'{url}registration')
    assert response.status_code == 500


def test_request_registration_with_data():
    data = dict(account_first_name='first name', account_last_names='last name',
                account_holder_address='78, Holder Street', account_city='Glasgow', account_holder_mobno='7700900129',
                account_holder_dob='1970-08-08', account_balance='1000', overdraft_amount='1000',
                account_type='Savings account', password='123456')
    response = requests.post(f'{url}registration', data=data)
    assert response.status_code == 200


def test_request_options():
    response = session.get(f'{url}/options')
    assert response.status_code == 200


def test_request_customer_details():
    response = session.get(f'{url}/customer_details')
    assert response.status_code == 200


def test_request_transactions():
    response = session.get(f'{url}/transactions')
    assert response.status_code == 200


def test_request_withdrawal():
    response = session.get(f'{url}/withdrawal')
    assert response.status_code == 200


def test_request_select_transactions():
    data = {
        'date_from': '2013-01-01',
        'date_to': '2013-02-02'
    }
    response = session.post(f'{url}/select_transactions', data=data)
    assert response.status_code == 200

def test_request_make_withdrawal():
    data = dict(withdraw='1000')
    response = session.post(f'{url}/make_withdrawal', data=data)
    assert response.status_code == 200


def test_request_currency_exchange():
    data = {
        'currency': 'USD'
    }
    response = session.post(f'{url}/currency_exchange', data=data)
    assert response.status_code == 200


def test_request_deposit():
    response = session.post(f'{url}/deposit')
    assert response.status_code == 200


def test_request_delete_account():
    response = requests.post(f'{url}delete_account', data={'account_id': 200015, 'password': 123456})
    assert response.status_code == 200


def test_request_delete():
    response = requests.get(f'{url}delete')
    assert response.status_code == 200


def test_request_logout():
    response = requests.get(f'{url}logout')
    assert response.status_code == 200
