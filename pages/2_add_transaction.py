import streamlit as st
import datetime
from database.db import get_session
from database.models import Transaction

st.title("➕ Add New Transaction")

with st.form("transaction_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        txn_type = st.selectbox("Type", ["Expense", "Income"])
        amount = st.number_input("Amount ($)", min_value=0.01, format="%.2f")
        txn_date = st.date_input("Date", datetime.date.today())
        
    with col2:
        if txn_type == "Expense":
            category = st.selectbox("Category", ["Food", "Rent", "Transport", "Entertainment", "Utilities", "Other"])
        else:
            category = st.selectbox("Category", ["Salary", "Freelance", "Investment", "Gift", "Other"])
            
        description = st.text_input("Description (Optional)")

    submitted = st.form_submit_button("Save Transaction")

    if submitted:
        session = get_session()
        try:
            new_txn = Transaction(
                amount=amount,
                category=category,
                type=txn_type,
                description=description,
                transaction_date=txn_date
            )
            session.add(new_txn)
            session.commit()
            st.success("✅ Transaction successfully added!")
        except Exception as e:
            session.rollback()
            st.error(f"Error saving transaction: {e}")
        finally:
            session.close()