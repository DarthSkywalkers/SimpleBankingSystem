from random import randint


class BankingSystem:

    state = None
    accounts = {}
    card_number_entered = None
    authenticated = False

    def __init__(self):
        self.state = "main menu"

    def set_state(self, state):
        self.state = state

    def back_to_menu(self):
        self.set_state("main menu")
        self.main_menu()

    def show_main_menu(self):
        print("1. Create an account\n"
              "2. Log into account\n"
              "0. Exit")
        self.state = "choose option"

    def show_account_menu(self):
        print("\n1. Balance\n"
              "2. Log out\n"
              "0. Exit")
        self.state = "choose option"

    def main_menu(self, command=None):
        if self.state == "main menu":
            self.show_main_menu()
        elif self.state == "account menu" and self.authenticated:
            self.show_account_menu()
        elif self.state == "choose option":
            self.show_option(command)
        elif self.state == "login - entering card number" or self.state == "login - entering PIN":
            self.log_into_acc(command)

    def show_option(self, command):
        if not self.authenticated:
            if command == "1":
                self.set_state("creating account")
                self.create_acc()
            elif command == "2":
                self.set_state("logging into account")
                self.log_into_acc(command)
            elif command == "0":
                self.exit()
        elif self.authenticated:
            if command == "1":
                self.set_state("checking balance")
                self.show_balance()
            elif command == "2":
                self.set_state("logout")
                self.logout()
            elif command == "0":
                self.exit()

    def create_acc(self):
        card_number = None
        while card_number is None or card_number in list(self.accounts):
            card_number = f"400000{randint(0, 999999999):09}9"
        card_pin = f"{randint(0, 9999):04}"
        self.accounts[card_number] = {"pin": f"{card_pin}", "balance": 0}
        print("\nYour card has been created\n"
              "Your card number:\n"
              f"{card_number}\n"
              "Your card PIN:\n"
              f"{card_pin}\n")
        self.back_to_menu()

    def log_into_acc(self, command=None):
        if self.state == "logging into account":
            print("\nEnter your card number:")
            self.set_state("login - entering card number")
        elif self.state == "login - entering card number":
            self.card_number_entered = command
            print("Enter your PIN:")
            self.set_state("login - entering PIN")
        elif self.state == "login - entering PIN":
            card_pin = command
            if self.card_number_entered in list(self.accounts):
                if self.accounts[self.card_number_entered]["pin"] == card_pin:
                    self.authenticated = self.card_number_entered
                    self.card_number_entered = None
                    print("\nYou have successfully logged in!")
                    self.set_state("account menu")
                    self.main_menu()
                else:
                    print("Wrong card number or PIN!")
                    self.back_to_menu()
            else:
                print("Wrong card number or PIN!")
                self.back_to_menu()

    def show_balance(self):
        print("\nBalance:", self.accounts[self.authenticated]["balance"])
        self.set_state("account menu")
        self.main_menu()

    def logout(self):
        self.authenticated = False
        print("\nYou have successfully logged out!\n")
        self.back_to_menu()

    def exit(self):
        self.authenticated = False
        print("\nBye!")
        self.set_state("exiting")


bank = BankingSystem()
user_input = False
first_run = 1
while True:
    if bank.state == "exiting":
        break
    else:
        if first_run == 1:
            first_run = None
        else:
            user_input = input()
        bank.main_menu(user_input)
