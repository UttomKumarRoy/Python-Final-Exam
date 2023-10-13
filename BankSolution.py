class BankAccount:
    account_number = 1001
    accounts = {}
    allow_loans=True
    bankrupt=False

    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.loan_taken = 0
        self.transaction_history = []
        self.account_number = BankAccount.account_number
        BankAccount.account_number += 1
        BankAccount.accounts[self.account_number] = self

    def deposit(self, amount):
        if amount>0:
            self.balance += amount
            self.transaction_history.append(f"Deposited {amount} Tk.")
            return f"Successfully deposited {amount} Tk.\n"
        else:
            return "Negative or Zero amount can't be deposited\n"

    def withdraw(self, amount):
        if BankAccount.bankrupt==True:
            print("The bank is bankrupt")
            return
        if amount > self.balance:
            return "Withdrawal amount exceeded\n"
        self.balance -= amount
        self.transaction_history.append(f"Withdrew {amount} Tk.")
        return f"Successfully withdraw {amount} Tk.\n"


    def check_balance(self):
        return f"Current Balance: {self.balance} Tk.\n"

    def check_transaction_history(self):
        return self.transaction_history

    def take_loan(self, amount):
        if self.allow_loans==True:
            if self.loan_taken < 2:
                self.loan_taken += 1
                self.balance += amount
                self.transaction_history.append(f"Loan received: {amount} Tk.")
                return f"Loan {amount} Tk. received successfully.\n"
            return "You have already taken two loans.\n"
        else:
            return "You can't take loans right now.\n"

    def transfer(self, receiver_account_number, amount):
        if receiver_account_number in BankAccount.accounts:
            receiver = BankAccount.accounts[receiver_account_number]
            if amount <= self.balance:
                self.balance -= amount
                receiver.deposit(amount)
                self.transaction_history.append(f"Transferred {amount} Tk. to Account #{receiver_account_number}")
                return f"Transferred {amount} Tk. successfully.\n"
            else:
                return "Insufficient balance for the transfer.\n"
        else:
            return "Account does not exist.\n"


class Admin:
    state="enable"
    isBankrupt=False
    def __init__(self) -> None:
        pass

    def create_account(self, name, email, address, account_type):
        user = BankAccount(name, email, address, account_type)
        return f"\nAccount created successfully for {name}. Account number: {user.account_number}\n"

    def delete_account(self, account_number):
        if account_number in BankAccount.accounts:
            del BankAccount.accounts[account_number]
            return f"\nAccount number {account_number} deleted.\n"
        return "\nAccount not found.\n"

    def see_all_accounts(self):
        return BankAccount.accounts

    def total_balance(self):
        total = sum(account.balance for account in BankAccount.accounts.values())
        return f"Total available balance in the bank: {total} Tk.\n"

    def total_loan_amount(self):
        total_loan = sum(account.loan_taken for account in BankAccount.accounts.values())
        return f"Total loan amount in the bank: {total_loan} Tk.\n"

    def toggle_loan_feature(self):
        if Admin.state=="enable":
            Admin.state="disable"
            BankAccount.allow_loans = False
            return "Loan feature is now disabled\n"
        else:
            Admin.state="enable"
            BankAccount.allow_loans = True
            return "Loan feature is now enabled\n"

    def bankrupt(self):
        if(Admin.isBankrupt==False):
            Admin.isBankrupt=True
            BankAccount.bankrupt=True
            return "Bankrupt is active\n"
        else:
            Admin.isBankrupt=False
            BankAccount.bankrupt=False
            return "Bankrupt is not active\n"




currentUser=None

admin_name="admin"
admin_password=123


print("Welcome to our Bank Management System")


while(True):
        if currentUser==None:

            print("1. Login as Admin")
            print("2. Register as User")
            print("3. Login as User")
            print("4. Exit\n")
            op=int(input("Choice Option:"))
            if op==1:
                name=input("\nEnter name of Admin: ")
                password=int(input("Enter Admin password: "))
                if name==admin_name and password==admin_password:
                    print("\nCongratulations Admin!\n")
                    while True:
                        print("1. Create Account")
                        print("2. Delete Account")
                        print("3. See All Users Account")
                        print("4. Check the total available balance of the bank.  ")
                        print("5. Check the total loan amount.")
                        print("6. Loan features on/off.")
                        print("7. Bankrupt active or not")
                        print("8. Logout\n")
                        
                        op=int(input("Choice Option:"))
                        admin=Admin()
                        if op==1:
                            name=input("\nUser Name:")
                            email=input("Email:")
                            address=input("Address:")
                            account_type=input("Account (Savings/Current) :")
                            print(admin.create_account(name, email, address, account_type))
                        elif op==2:
                            account=int(input("Enter Account No. for Deletion:"))
                            print(admin.delete_account(account))
                        elif op==3:
                            print("Account Numbers and Account Holder Name:\n")
                            accounts=admin.see_all_accounts()  
                            for account in accounts.keys():
                                print(f"\t{account} \t\t\t{accounts[account].name}\n")                      
                        elif op==4:
                            print(admin.total_balance())  
                        elif op==5:
                            print(admin.total_loan_amount())  
                        elif op==6:
                            print(admin.toggle_loan_feature())
                        elif op==7:
                            print(admin.bankrupt())
                        elif op==8:
                            currentUser=None
                            print("Logout Successful\n")
                            break
                        else:
                            print("Invalid Option\n")
                else:
                    print("Oops! Admin name or password error\n")

            elif op==2:
                name=input("\nEnter Name:")
                email=input("Enter Email:")
                address=input("Enter Address:")
                account_type=input("Account (Savings/Current) :")
                user=BankAccount(name, email, address, account_type)
                print(f"\nCongratulations {name}! for creating account. Your account number:{user.account_number}\n")
            
            elif op==3:
                no=int(input("Enter your Account Number:"))
                if no in BankAccount.accounts:
                    currentUser=BankAccount.accounts[no]
                    print(f"Congratulations {currentUser.name}!\n")
                    while True:
                        print("1. Withdraw")
                        print("2. Deposit")
                        print("3. Check balance")
                        print("4. Transaction History")
                        print("5. Taking Loan")
                        print("6. Transfer Balance")
                        print("7. Logout\n")
                        
                        op=int(input("Choice Option:"))
                        
                        if op==1:
                            amount=int(input("Enter withdraw amount:"))
                            print(currentUser.withdraw(amount))
                            
                        elif op==2:
                            amount=int(input("Enter deposit amount:"))
                            print(currentUser.deposit(amount))
                        
                        elif op==3:
                            print(currentUser.check_balance())
                        
                        elif op==4:
                            print(currentUser.check_transaction_history())  
                            print("\n")     
                        
                        elif op==5:
                            amount=int(input("Enter loan amount:"))
                            print(currentUser.take_loan(amount))
                        
                        elif op==6:
                            receiver_account=int(input("Enter Receiver Account No.:"))
                            amount=int(input("Enter transfer amount:"))
                            print(currentUser.transfer(receiver_account, amount))

                        elif op==7:
                            currentUser=None
                            print("Logout Successful\n")
                            break
                        else:
                            print("Invalid Option\n")
                else:
                    print("User not found\n")
            elif op==4:
                print("Successfully exited")
                exit()
            else:
                print("Invalid Option\n")
