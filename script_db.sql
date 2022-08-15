CREATE DATABASE BANK_APP;
USE BANK_APP;

CREATE TABLE Customer_details (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    account_first_name VARCHAR(50) NOT NULL,
    account_last_name VARCHAR(50) NOT NULL,
    account_holder_address VARCHAR(200) DEFAULT NULL,
    account_city VARCHAR(100) DEFAULT NULL,
    account_holder_mobno BIGINT NOT NULL,
    account_holder_dob DATE,
    password VARCHAR(50) NOT NULL
);

ALTER TABLE Customer_details AUTO_INCREMENT=20001;

INSERT INTO Customer_details(account_id, account_first_name, account_last_name, account_holder_address, account_city, account_holder_mobno, account_holder_dob, password)
VALUES
(NULL,'Camille', 'Downie', '78, Holder Street', 'Glasgow', 07700900129, '1950-01-01',"isRx$^6L8*3*#"),
(NULL,'Chenelle', 'Brown', '34 Comer Road', 'Cardiff', 07700900800, '1960-02-02',"G&n0S&^A68UC#"),
(NULL,'Shania', 'Smith', '5 Downing Drive', 'London', 07700900716, '1970-03-03',"M58n4U%KpNko#"),
(NULL,'Tolu', 'Ademola', '90 Dolphin Road', 'Port Harcourt', 07700900700, '1970-04-04',"0O4Oz9aU*2pF"),
(NULL,'Efyah', 'Bonsu', '2 Kiki Close', 'Accra', 07700900815, '1970-05-05',"C4%2e94nC6bz"),
(NULL,'Efyah', 'Bonsu', '2 Kiki Close', 'Accra', 07700900580, '1970-06-06',"5X4G559@hOll"),
(NULL,'Mekhai', 'Sun', '78 Holder Street', 'Glasgow', 07700900287, '1970-07-07',"vknJN862RF#O"),
(NULL,'Abigail', 'Gordon', '1 Pluck Drive', 'Newcastle', 07700900497, '1970-08-08',"rVr5RR678*vO#x"),
(NULL,'Abigail', 'Gordon', '1 Pluck Drive', 'Newcastle', 07700900131, '1970-09-09',"xWUi#2^05%*r"),
(NULL,'Iris', 'Valadas', '18 Score Road', 'London', 07700900818, '1970-10-10',"7349a0DC%@kD"),
(NULL,'Charlotte', 'Diamond', '67 Range Road', 'Manchester', 07700900619, '1970-11-11',"oTN1g9%@7Tm6#"),
(NULL,'Gabriela', 'Rangel', '23 Cranham Gardens', 'Birmingham', 07700900728, '1970-12-12',"tlH@%OG9p56%");

CREATE TABLE Account_type (
    account_type_id INT NOT NULL,
    savings TINYINT(0),
    current_account TINYINT(0),
    overdraft_eligibility TINYINT(0),
    PRIMARY KEY (account_type_id)
);

 INSERT INTO Account_type(account_type_id, savings, current_account, overdraft_eligibility)
 VALUES
 (1, 1, 0, 0),
 (2, 0, 1, 1);

CREATE TABLE Accounts (
    account_id INT NOT NULL,
    account_balance FLOAT DEFAULT NULL,
    overdraft_amount FLOAT DEFAULT NULL,
    account_type_id INT NOT NULL,
    PRIMARY KEY (account_id),
    CONSTRAINT account_type_fk FOREIGN KEY (account_type_id)
        REFERENCES account_type (account_type_id)
);

 INSERT INTO Accounts(account_id, account_balance, overdraft_amount, account_type_id)
 VALUES
(20001, 5000, 2000, 2),
(20002, 6500, 2000, 2),
(20003, 20000, 0, 1),
(20004, 2000, 5000, 2),
(20005, 1000, 4000, 2),
(20006, 20000, 3000, 2),
(20007, 10000, 0, 1),
(20008, 1500, 0, 1),
(20009, 2500, 100, 2),
(20010, 2500, 2000, 2),
(20011, 2000, 1700, 2),
(20012, 3700, 3000, 2);

CREATE TABLE trandetails (
    tnumber INT AUTO_INCREMENT,
    account_id INT NOT NULL,
    dot DATE,
    transaction_type VARCHAR(20),
    transaction_amount INT(7),
    CONSTRAINT trandetails_tnumber_pk PRIMARY KEY (tnumber),
    CONSTRAINT trandetails_acnumber_fk FOREIGN KEY (account_id)
        REFERENCES Accounts (account_id)
);

INSERT INTO trandetails VALUES(null,20001,'2013-01-01','Deposit',2000);
INSERT INTO trandetails VALUES(null,20002,'2013-02-01','Withdrawal',1000);
INSERT INTO trandetails VALUES(null,20003,'2013-01-01','Deposit',2000);
INSERT INTO trandetails VALUES(null,20004,'2013-02-01','Deposit',3000);
INSERT INTO trandetails VALUES(null,20005,'2013-01-11','Deposit',7000);
INSERT INTO trandetails VALUES(null,20006,'2013-01-13','Deposit',9000);
INSERT INTO trandetails VALUES(null,20007,'2013-03-13','Deposit',4000);
INSERT INTO trandetails VALUES(null,20008,'2013-03-14','Deposit',3000);
INSERT INTO trandetails VALUES(null,20009,'2013-03-21','Withdrawal',9000);
INSERT INTO trandetails VALUES(null,20010,'2013-03-22','Withdrawal',2000);
INSERT INTO trandetails VALUES(null,20011,'2013-03-25','Withdrawal',7000);
INSERT INTO trandetails VALUES(null,20012,'2013-03-26','Withdrawal',2000);

CREATE TRIGGER create_account AFTER INSERT ON customer_details FOR EACH ROW INSERT INTO accounts Values((select max(account_id) from customer_details), null, null, 1);

CREATE TRIGGER delete_account
	after delete on trandetails
	for each row
	delete from accounts a where a.account_id = OLD.account_id;

CREATE TRIGGER delete_transactions
	after delete on customer_details
	for each row
	delete from trandetails t where t.account_id = OLD.account_id;
