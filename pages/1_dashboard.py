import streamlit as st
from utils.helpers import fetch_all_transactions, calculate_kpis

st.title("📊 Financial Dashboard")

df = fetch_all_transactions()

if df.empty:
    st.warning("No data found. Please add transactions.")
else:
    # Top KPI Cards
    income, expense, savings, savings_pct = calculate_kpis(df)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Income", value=f"${income:,.2f}")
    with col2:
        st.metric(label="Total Expenses", value=f"${expense:,.2f}")
    with col3:
        st.metric(label="Net Savings", value=f"${savings:,.2f}")
    with col4:
        st.metric(label="Savings Rate", value=f"{savings_pct:.1f}%")

    st.markdown("---")
    
    # Recent Transactions Table
    st.subheader("Recent Transactions")
    recent_df = df.sort_values(by='transaction_date', ascending=False).head(10)
    
    # Optional CSV Export
    csv = recent_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Recent Data as CSV",
        data=csv,
        file_name='recent_transactions.csv',
        mime='text/csv',
    )
    
    st.dataframe(
        recent_df[['transaction_date', 'type', 'category', 'amount', 'description']],
        use_container_width=True,
        hide_index=True
    )