from pathlib import Path
import json
import random
import string


class Bank:
    database = "database.json"
    data = []

    # -------------------- Load Database --------------------
    try:
        if Path(database).exists():
            with open(database) as f:
                data = json.load(f)
        else:
            data = []
    except Exception as err:
        print(f"Error loading database: {err}")
        data = []

    # -------------------- Save Database --------------------
    @classmethod
    def _update_database(cls):
        with open(cls.database, "w") as f:
            json.dump(cls.data, f, indent=4)

    # -------------------- Generate Account Number --------------------
    @staticmethod
    def _generate_account_no():
        letters = random.choices(string.ascii_uppercase, k=4)
        digits = random.choices(string.digits, k=6)
        acc = letters + digits
        random.shuffle(acc)
        return "".join(acc)

    # -------------------- Find User --------------------
    @staticmethod
    def _find_user(acc_no, pin):
        return next((u for u in Bank.data if u["account_no"] == acc_no and u["pin"] == pin), None)

    # -------------------- Create Account --------------------
    def create_account(self):
        name = input("Enter your name: ")
        email = input("Enter email: ")
        phone = input("Enter phone: ")

        pin = input("Enter 4-digit PIN: ")
        if len(pin) != 4 or not pin.isdigit():
            print("❌ Invalid PIN")
            return

        if len(phone) != 10 or not phone.isdigit():
            print("❌ Invalid phone number")
            return

        account_no = self._generate_account_no()
        print(f"✔ Your new account number: {account_no}")

        user = {
            "name": name,
            "email": email,
            "phone": phone,
            "pin": int(pin),
            "account_no": account_no,
            "balance": 0
        }

        Bank.data.append(user)
        Bank._update_database()
        print("✔ Account created successfully")

    # -------------------- Deposit Money --------------------
    def deposit_money(self):
        acc = input("Enter account no: ")
        pin = input("Enter PIN: ")

        if not pin.isdigit():
            print("❌ Invalid PIN")
            return

        user = self._find_user(acc, int(pin))

        if not user:
            print("❌ User not found")
            return

        amount = input("Enter deposit amount: ")

        if not amount.isdigit() or int(amount) <= 0:
            print("❌ Invalid amount")
            return

        amount = int(amount)
        if amount > 50000:
            print("❌ Cannot deposit more than 50,000 at once")
            return

        user["balance"] += amount
        Bank._update_database()
        print("✔ Deposit successful")

    # -------------------- Withdraw Money --------------------
    def withdraw_money(self):
        acc = input("Enter account no: ")
        pin = input("Enter PIN: ")

        if not pin.isdigit():
            print("❌ Invalid PIN")
            return

        user = self._find_user(acc, int(pin))

        if not user:
            print("❌ User not found")
            return

        amount = input("Enter withdraw amount: ")
        if not amount.isdigit():
            print("❌ Invalid amount")
            return

        amount = int(amount)

        if amount <= 0:
            print("❌ Invalid amount")
            return

        if amount > user["balance"]:
            print("❌ Insufficient balance")
            return

        user["balance"] -= amount
        Bank._update_database()
        print("✔ Withdrawal successful")

    # -------------------- Show Details --------------------
    def show_details(self):
        acc = input("Enter account no: ")
        pin = input("Enter PIN: ")

        if not pin.isdigit():
            print("❌ Invalid PIN")
            return

        user = self._find_user(acc, int(pin))

        if not user:
            print("❌ User not found")
            return

        print("\n------- ACCOUNT DETAILS -------")
        for k, v in user.items():
            print(f"{k} : {v}")
        print("--------------------------------")

    # -------------------- Update Details --------------------
    def update_details(self):
        acc = input("Enter account no: ")
        pin = input("Enter PIN: ")

        if not pin.isdigit():
            print("❌ Invalid PIN")
            return

        user = self._find_user(acc, int(pin))

        if not user:
            print("❌ User not found")
            return

        print("\nLeave empty to keep old value")

        name = input("New name: ") or user["name"]
        email = input("New email: ") or user["email"]
        phone = input("New phone: ") or user["phone"]
        new_pin = input("New 4-digit PIN: ") or str(user["pin"])

        if not (new_pin.isdigit() and len(new_pin) == 4):
            print("❌ Invalid PIN")
            return

        user["name"] = name
        user["email"] = email
        user["phone"] = phone
        user["pin"] = int(new_pin)

        Bank._update_database()
        print("✔ Details updated successfully")

    # -------------------- Delete Account --------------------
    def delete_account(self):
        acc = input("Enter account no: ")
        pin = input("Enter PIN: ")

        if not pin.isdigit():
            print("❌ Invalid PIN")
            return

        user = self._find_user(acc, int(pin))

        if not user:
            print("❌ User not found")
            return

        Bank.data.remove(user)
        Bank._update_database()

        print("✔ Account deleted successfully")


# -------------------- Main Program --------------------

bank = Bank()

while True:
    print("\n---------- BANK MENU ----------")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Show Details")
    print("5. Update Details")
    print("6. Delete Account")
    print("7. Exit")
    print("--------------------------------")

    choice = input("Enter choice: ")

    if choice == "1":
        bank.create_account()
    elif choice == "2":
        bank.deposit_money()
    elif choice == "3":
        bank.withdraw_money()
    elif choice == "4":
        bank.show_details()
    elif choice == "5":
        bank.update_details()
    elif choice == "6":
        bank.delete_account()
    elif choice == "7":
        print("Thank you for using our bank system!")
        break
    else:
        print("❌ Invalid choice")
