import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

file = "expenses.csv"

if os.path.exists(file):
    df = pd.read_csv(file)
else:
    df = pd.DataFrame(columns=["Type", "Category", "Amount"])

st.title("💰 Personal Expense Tracker")
st.write("Track your income and expenses easily")

# Sidebar Input
st.sidebar.header("➕ Add Transaction")

type = st.sidebar.selectbox("Transaction Type", ["Income", "Expense"])

category = st.sidebar.selectbox(
    "Category",
    ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Salary", "Other"]
)

amount = st.sidebar.number_input("Amount", min_value=0)

if st.sidebar.button("Add Transaction"):
    new_data = {"Type": type, "Category": category, "Amount": amount}
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(file, index=False)
    st.sidebar.success("Transaction Added")

# Calculations
income = df[df["Type"] == "Income"]["Amount"].sum()
expense = df[df["Type"] == "Expense"]["Amount"].sum()
balance = income - expense

# Dashboard Metrics
col1, col2, col3 = st.columns(3)

col1.metric("💵 Total Income", f"₹{income}")
col2.metric("💸 Total Expense", f"₹{expense}")
col3.metric("💰 Balance", f"₹{balance}")

st.divider()

# Transaction Table
st.subheader("📋 Transaction History")
st.dataframe(df, use_container_width=True)

# Charts
if not df.empty:
    st.subheader("📊 Expense Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Expenses by Category")
        expense_chart = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum()
        st.bar_chart(expense_chart)

    with col2:
        st.write("Income vs Expense")
        summary = pd.DataFrame({
            "Amount": [income, expense]
        }, index=["Income", "Expense"])
        st.bar_chart(summary)