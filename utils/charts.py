import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Global SaaS Theme Settings
CHART_THEME = {
    'layout': go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="sans-serif", color="#E2E8F0"),
        margin=dict(l=20, r=20, t=40, b=20)
    )
}

def plot_expense_donut(df):
    expenses = df[df['type'] == 'Expense']
    if expenses.empty: return None
    
    fig = px.pie(expenses, values='amount', names='category', hole=0.6,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(CHART_THEME['layout'], title_text="Expense Distribution", title_x=0.5)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def plot_monthly_trend(df):
    df['month'] = pd.to_datetime(df['transaction_date']).dt.strftime('%b %Y')
    trend = df.groupby(['month', 'type'])['amount'].sum().reset_index()
    
    fig = px.area(trend, x='month', y='amount', color='type', 
                  color_discrete_map={'Income': '#10B981', 'Expense': '#EF4444'},
                  line_shape='spline') # Spline makes the lines curved and modern
    fig.update_layout(CHART_THEME['layout'], title_text="Cash Flow Trend", title_x=0.5,
                      xaxis_title="", yaxis_title="Amount ($)")
    return fig

def plot_spending_heatmap(df):
    """Generates a premium daily spending heatmap."""
    expenses = df[df['type'] == 'Expense'].copy()
    if expenses.empty: return None
    
    expenses['day_of_week'] = pd.to_datetime(expenses['transaction_date']).dt.day_name()
    expenses['week'] = pd.to_datetime(expenses['transaction_date']).dt.isocalendar().week
    
    heatmap_data = expenses.groupby(['day_of_week', 'week'])['amount'].sum().reset_index()
    
    fig = px.density_heatmap(heatmap_data, x='week', y='day_of_week', z='amount',
                             color_continuous_scale="Blues")
    fig.update_layout(CHART_THEME['layout'], title_text="Spending Intensity Heatmap", title_x=0.5)
    return fig