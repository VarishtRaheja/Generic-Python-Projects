# importing numpy package for random numbers.

import numpy as np

lst = []
ran_num = np.random.default_rng()
for i in range(np.random.randint(4,7)):
    lst.append(ran_num.integers(low=1,high=10).tolist())

number = int(''.join(map(str,lst)))
# print(number)

class CreateAccount:

    def __init__(self,account_number,name,initial_deposit):
        self.name = name
        self.initial_deposit = initial_deposit
        self.account_number = account_number

    def deposit_money(self,amount):
        self.initial_deposit += amount
        print(f"The deposited amount is: ${amount:.2f} to account number {self.account_number}. "
              f"Total balance is: ${self.initial_deposit}")

    def view_balance(self):
        print(f"Your account now has a balance of: ${self.initial_deposit:.2f}")


class BankingSystem:

    def __init__(self):
        self.accounts = {}

    def create_account(self,account_number, account_name,initial_deposit):
        if account_number in self.accounts:
            print('Account already exists!')
        else:
            self.accounts[account_number] = CreateAccount(number,account_name,initial_deposit)
            print(f"Account {account_number} in the name of {account_name}"
                  f" was created successfully with a deposit of ${initial_deposit}.")

    def get_account(self,account_number):
        return self.accounts.get(account_number)

def main():
    bank = BankingSystem()

    while True:
        print("1. Create Account\n2. Deposit Money\n3. View Balance\n4. Exit")
        user_choice = int(input('Enter the user choice (1-4): '))

        if user_choice==1:
            user_name = input("Enter user name: ")
            user_initial_deposit = int(input("Enter initial deposit: "))
            print(bank.create_account(number,user_name,user_initial_deposit))

        elif user_choice==2:
            account = bank.get_account(number)
            if account:
                amount = float(input("Enter the amount to be deposited: "))
                print(account.deposit_money(amount))
            else:
                print('Account not found!')

        elif user_choice==3:
            account = bank.get_account(number)
            if account:
                print(account.view_balance())
            else:
                print('Account not found or zero balance!')

        else:
            exit('Exiting... ')


print(main())


