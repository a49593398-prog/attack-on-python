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

#  table to store loan requests
cursor.execute('''
    CREATE TABLE IF NOT EXISTS loan_requests(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_number INTEGER,
        amount REAL,
        salary REAL,
        months INTEGER,
        request_time Text,
        status TEXT DEFAULT 'pending')''')
conn.commit()

def apply_for_loan(acc):
    print("\n----LOAN APPLICATION----")
    loan_amount = float(input("Enter the amount you need:- "))
    salary = float(input("Enter your monthily salary:- "))
    loan_timing = int(input("Enter the loan timing in months:- "))
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        INSERT INTO loan_requests
        (account_number,amount,salary,months,request_time,status)
                   VALUES(?,?,?,?,?,?)
        ''',(acc,loan_amount,salary,loan_timing,current_time,'pending'))
    conn.commit()
    print(f"Application sent on {current_time}. Please wait for Admin approval.")

def approve_loans():
    print("\n----PENDING LOAN REQUESTS----")
    cursor.execute('''
        SELECT * FROM loan_requests WHERE status = 'pending' ''')
    requests = cursor.fetchall()
    if not requests :
        print("No pending loan requests.")
        return

    for req in requests:
        print(f"\nID: {req[0]} | Account: {req[1]} | Amount: {req[2]} | Salary: {req[3]} | Months: {req[4]} | Applied at: {req[5]}")

        ch = input("Approve this loan ? (YES/NO)\n:-").upper().strip()

        if ch == 'YES':
            cursor.execute('''
                UPDATE Users SET balance = balance + ? WHERE account_number = ?
                ''',(req[2] , req[1]))
            cursor.execute('''
                UPDATE loan_requests SET status = 'Approved' WHERE id = ?
                ''',(req[0],))
            conn.commit()

            approval_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO transactions(account_number,type,amount,timestamp)
                        VALUES(?,?,?,?)
                ''',(req[1],f'Loan Approved ({req[4]} months)',req[2], approval_time))
            conn.commit()
            print("Loan Approved and funds transferred into yuor account.")
        
        else :
            cursor.execute('''
                UPDATE loan_requests SET status = 'Denied' WHERE id = ?
                ''',(req[0],))
            print(" Sorry your loan is denied. The amount is too high for your salary.")
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
    account = int(input('Enter your account number : - '))
    pin = int(input('Enter your pin : -'))

    conn = sqlite3.connect('bank_management_system.db')
    cursor = conn.cursor()
    cursor.execute('''
            SELECT account_number FROM Users WHERE account_number = ? AND pin = ?
    ''', (account,pin))
    user = cursor.fetchone()
    conn.commit()

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
    if username.strip() == "bank manager" and password.strip() == "manager2026":
        print('Manager logged')
        return True
    else:
        print('Invalid Manager')
        return None
        
def admin(log):
    while True:
        print('\nWelocome to ABCD Bank')
        print('Choose what you want\n')
        print("1. View All transactions")
        print("2. Search Transactions by Account Number")
        print("3. Apprve Loan Applications")
        print("4. EXIT")

        ch = int(input('Enter your choice:'))
        conn = sqlite3.connect('bank_management_system.db')
        cursor = conn.cursor()
        
        if ch == 1:
            cursor.execute('SELECT * FROM transactions')
            alldata = cursor.fetchall()

            print(f"\n{'ID':<5} | {'Account Nmber':<16} | {'Type':<25} | {'Amount':<10} | {'Date & Time':<20} |") 
            print("-" * 90)
            for record in alldata:
                print(f"{record[0]:<5} | {record[1]:<16} | {record[2]:<25} | ${record[3]:<10.2f} | {record[4]:<10} |")

        elif ch == 2:
            account = int(input("Enter account number to search:- "))
            cursor.execute('''SELECT * FROM transactions WHERE account_number = ?'''
                          ,(account,))
            alldata = cursor.fetchall()
            if admin_login:
                
                print(f"\n{'ID':<5} | {'Account Nmber':<16} | {'Type':<25} | {'Amount':<10} | {'Date & Time':<20} |") 
                print("-" * 74)
                for record in alldata:
                    print(f"{record[0]:<5} | {record[1]:<16} | {record[2]:<25} | ${record[3]:<10.2f} | {record[4]:<10} |")

            else:
                print('invalid account number')
        elif ch == 3 :
            approve_loans()
        conn.commit()

def change_pin(acc):
    account = int(input('Enter your account number:- '))
    old_pin = int(input("Enter your current pin:- "))
    nwe_pin = int(input("Enter your new pin:- "))

    conn = sqlite3.connect('bank_management_system.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE Users SET pin = ? WHERE account_number = ? and pin = ?
        ''',(nwe_pin,acc,old_pin))
    
    if cursor.rowcount > 0:
        conn.commit()
        print("PIN changed successfully")
    else:
        print("Error. Account number or old PIN incorrect.\n try again")

def users(acc):
    while True:
        print("\n---- BANK MANAGEMENT SYSTEM ----")
        print("1. View Balance")
        print("2. Deposit Amount")
        print("3. Withdraw Amount")
        print("4. Transaction History")
        print("5. Apple for a Loan")
        print("6. See Loan Status")
        print("7. Change Pin")
        print("8. Exit")   
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
            print(f"\n{'Date & Time':<20} | {'Type':<25} | {'Amount':<10} |") 
            print("-" * 54)
            for record in history:
                print(f"{record[2]:<20} | {record[0]:<25} | ${record[1]:<10.2f}|")

        elif choice == '5':
            apply_for_loan(acc)

        elif choice == '6':
            cursor.execute('''
                SELECT amount,status,request_time FROM loan_requests WHERE account_number = ?
                ''',(acc,))
            status_loan = cursor.fetchall()
            for s in status_loan:
                print(f"Time: {s[2]} | Amount: {s[0]} | Status: {s[1]}")

        elif choice == '7':
            change_pin(acc)

        elif choice == '8':
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
