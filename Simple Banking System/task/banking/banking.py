import sqlite3
from random import randint


class BankingSystem:
    state = None
    card_number_entered = None
    authenticated = False

    def __init__(self):
        self.state = "main menu"
        self.BIN = 400000
        self.conn = sqlite3.connect("card.s3db")
        self.c = self.conn.cursor()
        self.db_init()

    def main_menu(self, command=None):
        if self.state == "main menu":
            self.show_main_menu()
        elif self.state == "account menu" and self.authenticated:
            self.show_account_menu()
        elif self.state == "choose option":
            self.show_option(command)
        elif self.state == "login - entering card number" or self.state == "login - entering PIN":
            self.log_into_acc(command)

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
        while card_number is None:
            card_number = self.new_account_number()
            q_param = (card_number,)
            self.c.execute("SELECT count(number) FROM card WHERE number = ?", q_param)
            if self.c.fetchone()[0] != 0:
                card_number = None
        card_pin = f"{randint(0, 9999):04}"
        self.db_add_card(card_number, card_pin)
        print("\nYour card has been created\n"
              "Your card number:\n"
              f"{card_number}\n"
              "Your card PIN:\n"
              f"{card_pin}\n")
        self.back_to_menu()

    def new_account_number(self):
        number = str(self.BIN * pow(10, 9) + randint(0, 999999999))

        digits = []
        step = 1
        for n in number:
            n = int(n)
            if step % 2 != 0:
                n *= 2
                if n > 9:
                    n -= 9
            digits.append(n)
            step += 1

        sum_digits = sum(digits)
        checksum = 0
        while (sum_digits + checksum) % 10 != 0:
            checksum += 1

        return f"{number}{checksum}"

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
            q_param = (self.card_number_entered,)
            self.c.execute("SELECT count(number) FROM card WHERE number = ?", q_param)
            if self.c.fetchone()[0] == 1:
                self.c.execute("SELECT number, pin FROM card WHERE number = ?", q_param)
                query_result = self.c.fetchone()
                if self.card_number_entered == query_result[0] and card_pin == query_result[1]:
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

    def db_init(self):
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS card (
                id INTEGER PRIMARY KEY,
                number TEXT NOT NULL,
                pin TEXT NOT NULL,
                balance INTEGER DEFAULT 0);
            """)
        self.conn.commit()

    def db_add_card(self, card_number, card_pin):
        insert = (card_number, card_pin,)
        self.c.execute("INSERT INTO card (number, pin) VALUES (?, ?)", insert)
        self.conn.commit()

    def show_balance(self):
        q_param = (self.authenticated,)
        self.c.execute("SELECT balance FROM card WHERE number = ?", q_param)
        print("\nBalance:", self.c.fetchone()[0])
        self.set_state("account menu")
        self.main_menu()

    def set_state(self, state):
        self.state = state

    def back_to_menu(self):
        self.set_state("main menu")
        self.main_menu()

    def logout(self):
        self.authenticated = False
        print("\nYou have successfully logged out!\n")
        self.back_to_menu()

    def exit(self):
        self.conn.close()
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
