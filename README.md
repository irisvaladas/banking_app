# Banking_app
This is a flask app for a Customer Banking System.
This app is to work like an online banking system, with Python Flask for the driver code. HTML and CSS for the webpage design. Database for the customers is within an SQL script.
​
## Features of this app include:
- New Customer Account registration
- Customer Login
- Money Withdraw & Deposit - Using app code at an ATM
- Account Balance View
- View Transactions
- Update Customer Details
- View Currency exchange rate 
​
​
## Setup
### Install the Following Python Libraries:
- flask
- requests
- python-dateutil
- datetime
- mysql-connector-python
- uuid
- itertools
- pytest 
​
### Install MySql Community Server
Link - https://dev.mysql.com/downloads/mysql/
​
### Open Database and run it
Open script_db.sql in MySql
​
### config.py
Edit these properties in the config.py file to match with your MySql settings.
- HOST = "localhost"
- USER = "root"
- PASSWORD = ""
​
## Run app
In pyCharm run the file # bank_app.py 
The following should come up:
![Screenshot 2022-08-12 at 19 52 13](https://user-images.githubusercontent.com/107502259/184424737-273a3c37-83b5-4d64-a0a8-ff5e6d2c2539.png)
Select the http: link and the app will run.
​
## Please Note
- The port the app will be run on can be changed in the bottom of bank_app.py, do this if an error comes up with the port is already in use.
- This user is not a real user but for testing only:
![image](https://user-images.githubusercontent.com/107502259/184261872-43c531e5-8e23-4628-b2b6-17ccc12a08c0.png)
​
​
## Running Tests
There are 2 tests for this applications: test_app.py(Inside Tests folder) and bank_db_utils.py:
​

Install pytest module and:
- Run test_app.py
- If the port was changed in bank_app.py (refer to 'Please Note' section), then the port will need to be changed to match that in this file at the top of the file.
​

Install unittest module and uninstall pytest module:

- The reason why there is the need to uninstall pytest is because there is an issue when pytest is installed the tests within bank_db_utils_test.py do not run.
- Run bank_db_utils_tests.py that can be found in banking_app.py