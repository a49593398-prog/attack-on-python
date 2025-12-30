import sqlite3
from datetime import datetime

conn = sqlite3.connect('bank_management_system.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")
conn.commit()

# table to store user account details
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
        account_number INTEGER PRIMARY KEY ,
        user_name TEXT NOT NULL,
        pin TEXT NOT NULL,
        balance REAL DEFAULT 0.0
        )
    ''')
conn.commit()

# table to store transactions
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number INTEGER,
        type TEXT,
        amount REAL,
        timestamp TEXT,
        FOREIGN KEY(account_number)  REFERENCES Users (account_number) )
    ''')
conn.commit()



def open_account():
    print("\n----- OPEN NEW ACCOUNT -----")
    account = int(input('Enter your account number:- '))
    pin = int(input('Set your pin:- '))
    username = input('Enter your name:- ')

    conn = sqlite3.connect('bank_management_system.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO Users (account_number,pin,user_name)
                   VALUES(?,?,?)
            ''', (account,pin,username))
        conn.commit()
        print('Account added')
    except sqlite3.IntegrityError :
        print('Error: Account number already exists')
        return



def login():
    print("\n----- LOGIN -----")
    account = int(input('enter your account number : - '))
    pin = int(input('enter your pin : -'))

    conn = sqlite3.connect('bank_management_system.db')
    cursor = conn.cursor()
    cursor.execute('''
            SELECT account_number FROM Users WHERE account_number = ? AND pin = ?
    ''', (account,pin))
    user = cursor.fetchone()

    if user:
        print('user logged in ')
        return user [0]
    else:
        print('no such user')
        return None



def admin_login():
    print('\n----- BANK MANAGER LOGIN -----')
    username = input('Enter Manager Username:- ') 
    password = input('Enter Manager password:- ')
    if username.strip() == "bank manager" and password.strip() == "manager2025":
        print('Manager logged')
        return True
    else:
        print('Invalid Manager')
        return None



def admin(log):
    while True:
        print('Welocome to ABCD Bank')
        print('Choose what you want')
        ch = int(input('Enter your choice\n1.view all \n2.Search Transactions by account\n3.EXIT\nEnter choice:'))
        conn = sqlite3.connect('bank_management_system.db')
        cursor = conn.cursor()
        
        if ch == 1:
            cursor.execute('SELECT * FROM transactions')
            alldata = cursor.fetchall()
            for row in alldata:
                print(row)
        elif ch == 2:
            account = int(input("Enter account number to search:- "))
            cursor.execute('''SELECT * FROM transactions WHERE account_number = ?'''
                          ,(account,))
            alldata = cursor.fetchall()
            for row in alldata:
                print(row)
            else:
                print('invalid account number')
        conn.commit()
    


def apply_for_loan(acc):
    print("\n----LOAN APPLICATION----")
    loan_amount = float(input("Enter the amount you need:- "))
    salary = float(input("Enter your monthily salary:- "))
    loan_timing = int(input("Enter the loan timing in months:- "))

    if loan_amount <= (salary * 5):
        cursor.execute('''UPDATE Users SET balance = balance + ? WHERE account_number = ? '''
                       , (loan_amount,acc))
        cursor.execute('''INSERT INTO transactions (account_number, type, amount, timestamp) VALUES(?,?,?,?)'''
                       ,(acc,f'Loan ({loan_timing}months)', loan_amount , 
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        print(f"Congratulations Your loan of ${loan_amount} is approved and transferred to your account .")
    else:
        print("Sorry Your loan is denied. The amount is too high for your salary.")



def users(acc):
    while True:
        print("\n---- BANK MANAGEMENT SYSTEM ----")
        print("1. View Balance")
        print("2. Deposit Amount")
        print("3. Withdraw Amount")
        print("4. Transaction History")
        print("5. Apple for a Loan")
        print("6. Exit")   
        choice = input("Enter choice: ")
        conn = sqlite3.connect('bank_management_system.db')
        cursor = conn.cursor()

        if choice == '1':
            cursor.execute("SELECT balance FROM Users WHERE account_number = ?", (acc,))
            balance = cursor.fetchone()[0]
            print(f"\nAccount Balance: ${balance:.2f}")

        elif choice == '2':
            amount = float(input("Enter deposit amount: "))
            if amount > 0:
                cursor.execute("UPDATE Users SET balance = balance + ? WHERE account_number = ?", (amount, acc))
                cursor.execute("INSERT INTO transactions (account_number, type, amount, timestamp) VALUES (?, ?, ?, ?)",
                            (acc, 'Deposit',amount, 
                             datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                conn.commit()
                print("Deposit Successful.")
            else:
                print("Invalid amount.")

        elif choice == '3':
            amount = float(input("Enter withdrawal amount: "))
            cursor.execute("SELECT balance FROM Users WHERE account_number = ?", (acc,))
            current_balance = cursor.fetchone()[0]
            
            if 0 < amount <= current_balance:
                cursor.execute("UPDATE Users SET balance = balance - ? WHERE account_number = ?", (amount, acc))
                cursor.execute("INSERT INTO transactions (account_number, type, amount, timestamp) VALUES (?, ?, ?, ?)",
                        (acc, 'Withdrawal', amount, 
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                conn.commit()
                print("Withdrawal Successful.")
            else:
                print("Insufficient funds or invalid amount.")


        elif choice == '4':
            cursor.execute("SELECT type, amount, timestamp FROM transactions WHERE account_number = ?", (acc,))
            history = cursor.fetchall()
            print(f"\n{'Date & Time':<20} | {'Type':<16} | {'Amount':<10} |") 
            print("-" * 54)
            for record in history:
                print(f"{record[2]:<20} | {record[0]:<16} | ${record[1]:<10.2f}|")

        elif choice == '5':
            apply_for_loan(acc)
        elif choice == '6':
            break
        else:
            print("Invalid selection.")



def welcome():
    print("Welcome to ABCD Bank ")
    print('Choose what you want')
    ch = int(input('\n1.OPEN ACCOUNT\n2.LOGIN\n3.ADMIN LOGIN\n4.EXIT\nEnter choice:'))
    if ch == 1:
        open_account()
    elif ch == 2:
        acc = login()
        if acc is not None:
            users(acc)
    elif ch == 3:
        log = admin_login()
        if log is not None:
            admin(log)
       
if __name__=="__main__":
    welcome()