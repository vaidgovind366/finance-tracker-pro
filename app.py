import streamlit as st
import pandas as pd
import io
from database.db import init_db, get_session, seed_dummy_data
from database.models import Transaction
from utils.ui import inject_custom_css
from utils.analytics import calculate_financial_health, generate_ai_insights, get_budget_progress
from utils.charts import plot_expense_donut, plot_monthly_trend, plot_spending_heatmap

# 1. App Configuration
st.set_page_config(page_title="Finance Tracker Pro", page_icon="🏦", layout="wide")
inject_custom_css()
init_db()
seed_dummy_data() # Ensure DB has data for the dashboard to render

# 2. Data Fetching & State
@st.cache_data(ttl=60)
def load_data():
    session = get_session()
    query = session.query(Transaction)
    df = pd.read_sql(query.statement, session.bind)
    session.close()
    return df

df = load_data()

# 3. Sidebar Filtering (Global State)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2953/2953412.png", width=60)
    st.markdown("## Finance Pro")
    st.markdown("---")
    st.markdown("### 🎛️ Filters")
    
    if not df.empty:
        min_date, max_date = pd.to_datetime(df['transaction_date']).min(), pd.to_datetime(df['transaction_date']).max()
        date_range = st.date_input("Date Range", [min_date, max_date])
        selected_type = st.multiselect("Transaction Type", ["Income", "Expense"], default=["Income", "Expense"])
        
        # Apply Filters
        if len(date_range) == 2:
            mask = (pd.to_datetime(df['transaction_date']).dt.date >= date_range[0]) & \
                   (pd.to_datetime(df['transaction_date']).dt.date <= date_range[1]) & \
                   (df['type'].isin(selected_type))
            filtered_df = df.loc[mask]
        else:
            filtered_df = df
    else:
        filtered_df = df

# 4. Main Dashboard Header
st.title("Financial Command Center 📊")
st.markdown("Monitor your cash flow, track budgets, and discover actionable AI insights.")

if filtered_df.empty:
    st.warning("No data found for the selected filters.")
    st.stop()

# 5. Core KPIs
income = filtered_df[filtered_df['type'] == 'Income']['amount'].sum()
expense = filtered_df[filtered_df['type'] == 'Expense']['amount'].sum()
savings = income - expense
health_score = calculate_financial_health(income, expense)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Gross Income", f"${income:,.2f}", "+12% MoM") # MoM is dummy string for visual layout
col2.metric("Total Expenses", f"${expense:,.2f}", "-5% MoM", delta_color="inverse")
col3.metric("Net Savings", f"${savings:,.2f}", f"{(savings/income*100) if income>0 else 0:.1f}% Margin")
col4.metric("Financial Health", f"{health_score}/100", "Score based on savings rate")

st.markdown("---")

# 6. Tabbed Interface for Clean UX
tab1, tab2, tab3 = st.tabs(["📈 Overview Analytics", "🤖 AI Insights & Budget", "📋 Ledger & Export"])

with tab1:
    col_chart1, col_chart2 = st.columns([2, 1])
    with col_chart1:
        st.plotly_chart(plot_monthly_trend(filtered_df), use_container_width=True)
    with col_chart2:
        st.plotly_chart(plot_expense_donut(filtered_df), use_container_width=True)
        
    st.plotly_chart(plot_spending_heatmap(filtered_df), use_container_width=True)

with tab2:
    col_ai, col_budget = st.columns(2)
    with col_ai:
        st.subheader("🤖 Smart Insights")
        insights = generate_ai_insights(filtered_df)
        for insight in insights:
            st.info(insight)
            
    with col_budget:
        st.subheader("🎯 Monthly Budget Tracking")
        spent, budget, progress = get_budget_progress(filtered_df, monthly_budget=4000)
        st.progress(progress)
        st.markdown(f"**${spent:,.2f}** spent of **${budget:,.2f}** budget ({progress*100:.1f}%)")

with tab3:
    st.subheader("Transaction Ledger")
    
    # Advanced Dataframe with column configuration
    st.dataframe(
        filtered_df.sort_values(by='transaction_date', ascending=False),
        column_config={
            "amount": st.column_config.NumberColumn("Amount ($)", format="$%.2f"),
            "transaction_date": st.column_config.DateColumn("Date"),
            "type": st.column_config.TextColumn("Type"),
            "category": st.column_config.TextColumn("Category")
        },
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # Export Engine
    st.markdown("### 💾 Export Data")
    col_ex1, col_ex2 = st.columns([1, 4])
    
    with col_ex1:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV 📄", data=csv, file_name='finance_report.csv', mime='text/csv')
    
    with col_ex2:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, index=False, sheet_name='Transactions')
        excel_data = output.getvalue()
        st.download_button("Download Excel 📊", data=excel_data, file_name='finance_report.xlsx', 
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')