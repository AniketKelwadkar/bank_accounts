import random
import datetime
import unittest

# Creating a class for Basic Account
class BasicAccount:
    """
    Creating a counter to track account numbers.
    Will generate account number in serial 0,1,2 and so on.
    """
    serial_acc_counter = 0
    def __init__(self, ac_name, opening_balance):
        """Initializing function for Basic Account
        Includes - Account name, Opening balance and account number.
        name: (string) Account holder's name.
        ac_num: (int) Account number.
        balance: (float) Account balance.
        """
        BasicAccount.serial_acc_counter += 1
        self.ac_num = int(BasicAccount.serial_acc_counter)
        self.name = ac_name
        self.balance = opening_balance
    def __str__(self):
        """
        String representation for an account.
        Returns - Account name & Account balance.
        """
        return f"Account name: {self.name} Account balance: £{self.balance:.2f}"
    def deposit(self, amount):
        """
        Deposit/credit amount into specific account.
        Amount(float) to be deposited into the account.
        The method increases the account balance if it is positive.
        For negative amounts, program will print an error message.
        """
        if amount > 0:
            self.balance += amount
            return "Transaction successful."
        else:
            return "Transaction error - Deposit amount needs to be positive."
    def withdraw(self, amount):
        """
        Withdraw amount (float) from the account.
        Checks for valid and invalid conditions.
        """
        if amount <= 0:
            return f"Can not withdraw £{amount:.2f}"
        elif amount > self.balance:
            return f"Can not withdraw £{amount:.2f}"
        else:
            self.balance -= amount
            return f"{self.name} has withdrawn £{amount:.2f}. New balance is £{self.balance:.2f}"
    def close_account(self):
        """
        Method for closing the account.
        """
        self.withdraw(self.balance)
        return True
    def issue_new_card(self):
        """
        Method for issuing new card.
        Provides new card number with card expiry date.
        New card is assigned to an account.
        """
        self.card_num = self.iden_card_num()
        self.card_exp = self.iden_card_exp()
        return (self.card_num, self.card_exp)
    def get_balance(self):
        """
        Method to provide current account balance.
        """
        return self.balance
    def get_available_balance(self):
        """
        Method to provide available balance from the account.
        """
        return self.balance
    def get_name(self):
        """
        Provides account holder's name.
        """
        return self.name
    def get_ac_num(self):
        """
        Provides account number.
        Returns values as a string.
        """
        return str(self.ac_num)
    def print_balance(self):
        """
        Provide current account balance.
        """
        return f"Account balance: £{self.balance:.2f}"
    def iden_card_num(self):
        """
        Provides a new card number.
        """
        return ''.join([str(random.randint(0, 9)) for _ in range(16)])
    def iden_card_exp(self):
        """
        Provides an expiry date for the new card.
        """
        current_date = datetime.date.today()
        yr_exp = current_date.year + 3
        yr_exp_string = str(yr_exp)[-2:]
        return (current_date.month, int(yr_exp_string))

# Creating a class for Premium Account
class PremiumAccount(BasicAccount):
    """
    Class for PremiumAccount with additional overdraft features.
    Connected with BasicAccount.
    """
    def __init__(self, ac_name, opening_balance, initial_overdraft):
        """
        Initializing Premium account with name, opening balance and overdraft limit.
        """
        super().__init__(ac_name, opening_balance)
        self.overdraft_limit = initial_overdraft
        self.overdraft = False
    def __str__(self):
        """
        Provides account holder's name, balance, and overdraft limit.
        """
        return f"Account name: {self.name}\nAccount balance: £{self.balance:.2f}\nOverdraft limit: £{self.overdraft_limit}"
    def withdraw(self, amount):
        """
        Method to withdraw amount from the account, based on the overdraft limit.
        """
        if amount <= 0:
            return f"Can not withdraw £{amount:.2f}"
        elif amount > self.balance + self.overdraft_limit:
            return f"Can not withdraw £{amount:.2f}"
        else:
            self.balance -= amount
            self.overdraft = self.balance < 0
            return f"{self.name} has withdrawn £{amount:.2f}. New balance is £{self.balance:.2f}"
    def close_account(self):
        """
        Method to close the account.
        Takes into consideration overdraft limit, and overdraft used if any.
        """
        if self.balance < 0 and self.balance >= -self.overdraft_limit:
            overdraft_amount = abs(self.balance)
            return f"Can not close account due to customer being overdrawn by £{overdraft_amount}"
        else:
            self.withdraw(self.balance)
            return "Account closed."
    def set_overdraft_limit(self, new_limit):
        """
        Method to set overdraft limit on the account.
        """
        if new_limit >= 0:
            self.overdraft_limit = new_limit
        else:
            return "ERROR"
    def get_available_balance(self):
        """
        Provides available balance from the account,
        takes overdraft limit into consideration.
        """
        return self.balance + self.overdraft_limit
    def print_balance(self):
        """
        Provides account balance.
        If overdraft used, returns amount overdrawn.
        """
        if self.overdraft:
            return f"Overdraft used: £-{(self.balance)}"
        else:
            return f"Premium Account balance: £{self.balance}"

class TestBankAccounts(unittest.TestCase):
    
    def setUp(self):
        self.basic_acc = BasicAccount("Mark Hamill", 1000)
        self.premium_acc = PremiumAccount("Kate Hamill", 500, 1000)
    
    def testing_basic_account_creation(self):
        self.assertEqual(self.basic_acc.get_name(), "Mark Hamill")
        self.assertEqual(self.basic_acc.get_balance(), 1000)
    
    def testing_premium_account_creation(self):
        self.assertEqual(self.premium_acc.get_name(), "Kate Hamill")
        self.assertEqual(self.premium_acc.get_balance(), 500)
        self.assertEqual(self.premium_acc.get_available_balance(), 1500)
    
    def testing_deposit_basic_account(self):
        self.basic_acc.deposit(500)
        self.assertEqual(self.basic_acc.get_balance(), 1500)
    
    def testing_withdraw_basic_account(self):
        self.basic_acc.withdraw(300)
        self.assertEqual(self.basic_acc.get_balance(), 700)
    
    def testing_withdraw_more_than_balance_basic_account(self):
        self.basic_acc.withdraw(2000)
        self.assertEqual(self.basic_acc.get_balance(), 1000)
    
    def testing_close_basic_account(self):
        self.basic_acc.close_account()
        self.assertEqual(self.basic_acc.get_balance(), 0)
    
    def testing_deposit_premium_account(self):
        self.premium_acc.deposit(500)
        self.assertEqual(self.premium_acc.get_balance(), 1000)
    
    def testing_withdraw_premium_account(self):
        self.premium_acc.withdraw(300)
        self.assertEqual(self.premium_acc.get_balance(), 200)
    
    def testing_withdraw_more_than_balance_premium_account(self):
        self.premium_acc.withdraw(2000)
        self.assertEqual(self.premium_acc.get_balance(), 500)
    
    def testing_withdraw_within_overdraft_premium_account(self):
        self.premium_acc.withdraw(1200)
        self.assertEqual(self.premium_acc.get_balance(), -700)
        self.assertTrue(self.premium_acc.overdraft)
    
    def testing_close_premium_account(self):
        self.premium_acc.withdraw(800)  # Overdraw the account
        closed = self.premium_acc.close_account()
        self.assertEqual(closed, "Can not close account due to customer being overdrawn by £300.00")
    
    def testing_set_overdraft_limit(self):
        self.premium_acc.set_overdraft_limit(2000)
        self.assertEqual(self.premium_acc.overdraft_limit, 2000)
    
if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)