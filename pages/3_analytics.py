import pandas as pd
import numpy as np
from datetime import datetime

def calculate_financial_health(income, expenses):
    """Calculates a score from 0-100 based on savings rate."""
    if income == 0: return 0
    savings_rate = ((income - expenses) / income) * 100
    # Perfect score if saving 30% or more
    score = min(100, max(0, (savings_rate / 30) * 100))
    return int(score)

def generate_ai_insights(df):
    """Generates intelligent text insights comparing current vs past data."""
    if df.empty:
        return ["Not enough data to generate insights."]
    
    insights = []
    df['date'] = pd.to_datetime(df['transaction_date'])
    current_month = datetime.now().month
    
    current_df = df[df['date'].dt.month == current_month]
    expenses = current_df[current_df['type'] == 'Expense']
    income = current_df[current_df['type'] == 'Income']['amount'].sum()
    total_expense = expenses['amount'].sum()

    # Insight 1: Top Category
    if not expenses.empty:
        top_cat = expenses.groupby('category')['amount'].sum().idxmax()
        top_amt = expenses.groupby('category')['amount'].sum().max()
        insights.append(f"🔍 **Top Expense:** You spent the most on **{top_cat}** (${top_amt:,.2f}) this month.")

    # Insight 2: Warning Alert
    if total_expense > income and income > 0:
        insights.append("⚠️ **Warning:** Your expenses have exceeded your income this month. Consider adjusting your budget.")
    elif total_expense > 0 and income > 0:
        savings_rate = ((income - total_expense) / income) * 100
        if savings_rate >= 20:
            insights.append(f"🎯 **Great Job:** You are saving {savings_rate:.1f}% of your income. Keep it up!")
            
    # Insight 3: Largest single transaction
    if not expenses.empty:
        max_txn = expenses.loc[expenses['amount'].idxmax()]
        insights.append(f"💸 **Largest Transaction:** ${max_txn['amount']:,.2f} for {max_txn['category']} on {max_txn['date'].strftime('%b %d')}.")

    return insights

def get_budget_progress(df, monthly_budget=5000):
    """Calculates how much of the budget has been used."""
    current_month = datetime.now().month
    current_expenses = df[(pd.to_datetime(df['transaction_date']).dt.month == current_month) & 
                          (df['type'] == 'Expense')]['amount'].sum()
    
    progress = min(current_expenses / monthly_budget, 1.0)
    return current_expenses, monthly_budget, progress