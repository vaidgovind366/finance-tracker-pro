import pandas as pd
from database.db import get_session
from database.models import Transaction

def fetch_all_transactions():
    """Fetch all transactions and return as a Pandas DataFrame."""
    session = get_session()
    query = session.query(Transaction)
    df = pd.read_sql(query.statement, session.bind)
    session.close()
    return df

def calculate_kpis(df):
    """Calculate total income, expenses, and savings."""
    if df.empty:
        return 0.0, 0.0, 0.0, 0.0
    
    income = df[df['type'] == 'Income']['amount'].sum()
    expense = df[df['type'] == 'Expense']['amount'].sum()
    savings = income - expense
    savings_pct = (savings / income * 100) if income > 0 else 0
    
    return income, expense, savings, savings_pct

def get_financial_insights(df):
    """Generate basic AI-style text insights."""
    if df.empty:
        return "Not enough data for insights."
    
    expenses_df = df[df['type'] == 'Expense']
    if not expenses_df.empty:
        top_category = expenses_df.groupby('category')['amount'].sum().idxmax()
        highest_expense = expenses_df['amount'].max()
        return f"💡 **Insight:** You spent the most on **{top_category}** recently. Your highest single expense was **${highest_expense:.2f}**."
    return "💡 **Insight:** Keep tracking your expenses to see trends!"