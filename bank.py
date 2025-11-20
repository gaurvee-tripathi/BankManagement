import streamlit as st
import json
import random
import string
from pathlib import Path

# -----------------------------
# Bank Class (streamlit-safe)
# -----------------------------
class Bank:
    database = 'database.json'

    @classmethod
    def load_data(cls):
        if Path(cls.database).exists():
            with open(cls.database, "r") as f:
                return json.load(f)
        else:
            return []

    @classmethod
    def save_data(cls, data):
        with open(cls.database, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def generate_account_no():
        alpha = random.choices(string.ascii_letters, k=5)
        digits = random.choices(string.digits, k=4)
        id = alpha + digits
        random.shuffle(id)
        return "".join(id)

# Load data into Streamlit session
if "data" not in st.session_state:
    st.session_state.data = Bank.load_data()

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🏦 Simple Bank Application")

menu = st.selectbox(
    "Choose an operation:",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Show Details",
        "Update Details",
        "Delete Account"
    ]
)

# -----------------------------
# CREATE ACCOUNT
# -----------------------------
if menu == "Create Account":
    st.subheader("📝 Create New Account")

    name = st.text_input("Enter Name")
    email = st.text_input("Enter Email")
    phone = st.text_input("Enter Phone Number")
    pin = st.text_input("Enter 4-digit PIN", type="password")

    if st.button("Create Account"):
        if len(pin) != 4 or not pin.isdigit():
            st.error("❌ PIN must be 4 digits!")
        elif len(phone) != 10 or not phone.isdigit():
            st.error("❌ Phone number must be 10 digits!")
        else:
            acc_no = Bank.generate_account_no()
            new_user = {
                "name": name,
                "email": email,
                "phoneNo.": phone,
                "pin": int(pin),
                "Accountno.": acc_no,
                "balance": 0
            }

            st.session_state.data.append(new_user)
            Bank.save_data(st.session_state.data)

            st.success(f"🎉 Account created! Your Account No: **{acc_no}**")

# -----------------------------
# DEPOSIT MONEY
# -----------------------------
elif menu == "Deposit Money":
    st.subheader("💰 Deposit Money")

    acc = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")
    amount = st.number_input("Enter Amount", min_value=1)

    if st.button("Deposit"):
        user = [u for u in st.session_state.data if u["Accountno."] == acc and u["pin"] == int(pin)] if pin.isdigit() else []
        if not user:
            st.error("❌ User not found")
        elif amount > 10000:
            st.error("❌ Maximum deposit limit is 10,000")
        else:
            user[0]["balance"] += amount
            Bank.save_data(st.session_state.data)
            st.success("✅ Amount Deposited Successfully")

# -----------------------------
# WITHDRAW MONEY
# -----------------------------
elif menu == "Withdraw Money":
    st.subheader("🏧 Withdraw Money")

    acc = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")
    amount = st.number_input("Enter Amount", min_value=1)

    if st.button("Withdraw"):
        user = [u for u in st.session_state.data if u["Accountno."] == acc and u["pin"] == int(pin)] if pin.isdigit() else []
        if not user:
            st.error("❌ User not found")
        elif amount > 10000:
            st.error("❌ Maximum withdraw limit is 10,000")
        elif user[0]["balance"] < amount:
            st.error("❌ Insufficient Funds")
        else:
            user[0]["balance"] -= amount
            Bank.save_data(st.session_state.data)
            st.success("✅ Withdrawal Successful")

# -----------------------------
# SHOW DETAILS
# -----------------------------
elif menu == "Show Details":
    st.subheader("📄 Account Details")

    acc = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")

    if st.button("Show"):
        user = [u for u in st.session_state.data if u["Accountno."] == acc and u["pin"] == int(pin)] if pin.isdigit() else []
        if not user:
            st.error("❌ User not found")
        else:
            st.json(user[0])

# -----------------------------
# UPDATE DETAILS
# -----------------------------
elif menu == "Update Details":
    st.subheader("✏ Update Account Details")

    acc = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")

    if st.button("Load Details"):
        user = [u for u in st.session_state.data if u["Accountno."] == acc and u["pin"] == int(pin)] if pin.isdigit() else []
        
        if not user:
            st.error("❌ User not found")
        else:
            st.session_state.user_to_update = user[0]

    if "user_to_update" in st.session_state:
        u = st.session_state.user_to_update

        new_name = st.text_input("New Name", value=u["name"])
        new_email = st.text_input("New Email", value=u["email"])
        new_phone = st.text_input("New Phone", value=u["phoneNo."])
        new_pin = st.text_input("New PIN", value=str(u["pin"]))

        if st.button("Update"):
            u["name"] = new_name
            u["email"] = new_email
            u["phoneNo."] = new_phone
            u["pin"] = int(new_pin)

            Bank.save_data(st.session_state.data)
            st.success("✅ Details Updated Successfully")

# -----------------------------
# DELETE ACCOUNT
# -----------------------------
elif menu == "Delete Account":
    st.subheader("🗑 Delete Account")

    acc = st.text_input("Enter Account Number")
    pin = st.text_input("Enter PIN", type="password")

    if st.button("Delete"):
        before = len(st.session_state.data)
        st.session_state.data = [u for u in st.session_state.data if not (u["Accountno."] == acc and u["pin"] == int(pin))]
        after = len(st.session_state.data)

        Bank.save_data(st.session_state.data)

        if before == after:
            st.error("❌ User not found")
        else:
            st.success("🗑 Account Deleted Successfully")
