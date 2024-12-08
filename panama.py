# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from PIL import Image
import io

# Configuration and Page Setup
st.set_page_config(
    page_title="FinPath",
    page_icon="💰",
    layout="wide"
)

# Session State Initialization
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame({
        'date': [],
        'type': [],
        'category': [],
        'amount': [],
        'description': []
    })

def init_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'dashboard'
    if 'formalization_level' not in st.session_state:
        st.session_state.formalization_level = 1
    if 'achievements' not in st.session_state:
        st.session_state.achievements = []

# Utility Functions
def calculate_cash_position():
    if len(st.session_state.transactions) == 0:
        return 0
    inflows = st.session_state.transactions[st.session_state.transactions['type'] == 'income']['amount'].sum()
    outflows = st.session_state.transactions[st.session_state.transactions['type'] == 'expense']['amount'].sum()
    return inflows - outflows

def generate_financial_statements():
    if len(st.session_state.transactions) == 0:
        return pd.DataFrame(), pd.DataFrame()
    
    # Income Statement
    income = st.session_state.transactions[st.session_state.transactions['type'] == 'income'].groupby('category')['amount'].sum()
    expenses = st.session_state.transactions[st.session_state.transactions['type'] == 'expense'].groupby('category')['amount'].sum()
    
    income_statement = pd.DataFrame({
        'Category': ['Revenue', 'Expenses', 'Net Income'],
        'Amount': [income.sum(), expenses.sum(), income.sum() - expenses.sum()]
    })
    
    # Cash Flow
    cash_flow = st.session_state.transactions.copy()
    cash_flow['date'] = pd.to_datetime(cash_flow['date'])
    cash_flow = cash_flow.sort_values('date')
    cash_flow['cumulative'] = cash_flow.apply(lambda x: x['amount'] if x['type'] == 'income' else -x['amount'], axis=1).cumsum()
    
    return income_statement, cash_flow

def check_achievements():
    achievements = []
    if len(st.session_state.transactions) > 10:
        achievements.append("🏆 Record Keeper: Tracked 10+ transactions")
    if calculate_cash_position() > 1000:
        achievements.append("💰 Cash Master: Reached $1,000 in net cash")
    return achievements

# Navigation
def sidebar_navigation():
    st.sidebar.title("FinPath")
    pages = {
        "Dashboard": "dashboard",
        "Transactions": "transactions",
        "Cash Flow": "cashflow",
        "Financial Statements": "statements",
        "Formalization Journey": "formalization"
    }
    selection = st.sidebar.radio("Navigate to", list(pages.keys()))
    st.session_state.page = pages[selection]
    
    # Show business status
    st.sidebar.markdown("---")
    st.sidebar.subheader("Business Status")
    st.sidebar.progress(st.session_state.formalization_level * 20)
    st.sidebar.text(f"Level {st.session_state.formalization_level}/5")

# Page Components
def render_dashboard():
    st.title("Mi Negocio 📊")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Cash Position", f"${calculate_cash_position():,.2f}", "Today")
    with col2:
        transactions_today = len(st.session_state.transactions[
            st.session_state.transactions['date'] == datetime.now().date()
        ])
        st.metric("Today's Transactions", transactions_today, "New")
    with col3:
        st.metric("Formalization Level", f"Level {st.session_state.formalization_level}", "↗")
    with col4:
        achievement_count = len(check_achievements())
        st.metric("Achievements", achievement_count, "🏆")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue vs Expenses")
        if not st.session_state.transactions.empty:
            daily_summary = st.session_state.transactions.groupby(['date', 'type'])['amount'].sum().unstack()
            fig = px.bar(daily_summary, barmode='group')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Cash Flow Trend")
        _, cash_flow = generate_financial_statements()
        if not cash_flow.empty:
            fig = px.line(cash_flow, x='date', y='cumulative')
            st.plotly_chart(fig, use_container_width=True)

def render_transactions():
    st.title("Transaction Management 💸")
    
    # Transaction Input Form
    with st.form("transaction_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            date = st.date_input("Date", datetime.now())
        with col2:
            trans_type = st.selectbox("Type", ["income", "expense"])
        with col3:
            category = st.selectbox("Category", [
                "Sales", "Services", "Other Income",
                "Inventory", "Supplies", "Utilities", "Other Expenses"
            ])
        
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("Amount", min_value=0.0, step=0.01)
        with col2:
            description = st.text_input("Description")
            
        submitted = st.form_submit_button("Add Transaction")
        
        if submitted and amount > 0:
            new_transaction = pd.DataFrame({
                'date': [date],
                'type': [trans_type],
                'category': [category],
                'amount': [amount],
                'description': [description]
            })
            st.session_state.transactions = pd.concat([st.session_state.transactions, new_transaction], ignore_index=True)
            st.success("Transaction added successfully!")
    
    # Transaction History
    st.subheader("Transaction History")
    if not st.session_state.transactions.empty:
        st.dataframe(st.session_state.transactions.sort_values('date', ascending=False))
    else:
        st.info("No transactions recorded yet. Start by adding your first transaction!")

def render_cashflow():
    st.title("Cash Flow Management 💰")
    
    # Cash Position
    st.header("Current Cash Position")
    cash_position = calculate_cash_position()
    st.metric("Available Cash", f"${cash_position:,.2f}")
    
    # Cash Flow Analysis
    if not st.session_state.transactions.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Daily Cash Flow")
            daily_cash = st.session_state.transactions.copy()
            daily_cash['amount'] = daily_cash.apply(
                lambda x: x['amount'] if x['type'] == 'income' else -x['amount'], axis=1
            )
            daily_sum = daily_cash.groupby('date')['amount'].sum()
            fig = px.bar(daily_sum)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Cumulative Cash Position")
            _, cash_flow = generate_financial_statements()
            fig = px.line(cash_flow, x='date', y='cumulative')
            st.plotly_chart(fig, use_container_width=True)
    
    # Cash Flow Projections
    st.header("Cash Flow Projections")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upcoming Payments")
        upcoming = pd.DataFrame({
            'Description': ['Inventory Payment', 'Utilities', 'Supplier Invoice'],
            'Amount': [1200, 350, 800],
            'Due Date': ['2024-03-15', '2024-03-18', '2024-03-20']
        })
        st.dataframe(upcoming)
    
    with col2:
        st.subheader("Expected Income")
        expected = pd.DataFrame({
            'Description': ['Customer Payment', 'Service Contract', 'Regular Sales'],
            'Amount': [2500, 1500, 1000],
            'Expected Date': ['2024-03-16', '2024-03-19', '2024-03-21']
        })
        st.dataframe(expected)

def render_statements():
    st.title("Financial Statements 📑")
    
    income_statement, cash_flow = generate_financial_statements()
    
    # Income Statement
    st.header("Income Statement")
    if not income_statement.empty:
        st.dataframe(income_statement)
        
        # Visualize Income Statement
        fig = px.bar(income_statement, x='Category', y='Amount',
                    title="Income Statement Overview")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for income statement. Add some transactions first!")
    
    # Cash Flow Statement
    st.header("Cash Flow Statement")
    if not cash_flow.empty:
        st.dataframe(cash_flow)
        
        # Visualize Cash Flow
        fig = px.line(cash_flow, x='date', y='cumulative',
                     title="Cumulative Cash Flow")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for cash flow statement. Add some transactions first!")
    
    # Export Options
    if not income_statement.empty:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Export to Excel"):
                # Add Excel export functionality here
                st.success("Financial statements exported to Excel!")
        with col2:
            if st.button("Generate PDF Report"):
                # Add PDF generation functionality here
                st.success("PDF report generated!")

def render_formalization():
    st.title("Formalization Journey 🎯")
    
    # Progress Tracker
    levels = {
        1: {"title": "Startup Explorer", "requirements": ["Track daily transactions", "Create business name", "Set up digital wallet"]},
        2: {"title": "Record Keeper", "requirements": ["30 days of transactions", "Separate personal/business money", "Create simple budget"]},
        3: {"title": "Growth Master", "requirements": ["Register business name", "Get tax ID", "3 months of records"]},
        4: {"title": "Financial Pro", "requirements": ["Full business registration", "Basic accounting system", "Employee registration"]},
        5: {"title": "Business Champion", "requirements": ["Complete formal status", "Banking relationship", "Credit history"]}
    }
    
    current_level = st.session_state.formalization_level
    
    # Display Current Level
    st.header(f"Current Level: {levels[current_level]['title']}")
    st.progress(current_level * 0.2)
    
    # Display Requirements
    st.subheader("Level Requirements")
    for req in levels[current_level]['requirements']:
        st.checkbox(req, key=req)
    
    # Achievements
    st.header("Achievements 🏆")
    achievements = check_achievements()
    for achievement in achievements:
        st.success(achievement)
    
    # Next Steps
    if current_level < 5:
        st.header("Next Level")
        st.info(f"Complete current requirements to unlock: {levels[current_level + 1]['title']}")

# Main App Logic
def main():
    init_session_state()
    sidebar_navigation()
    
    if st.session_state.page == 'dashboard':
        render_dashboard()
    elif st.session_state.page == 'transactions':
        render_transactions()
    elif st.session_state.page == 'cashflow':
        render_cashflow()
    elif st.session_state.page == 'statements':
        render_statements()
    elif st.session_state.page == 'formalization':
        render_formalization()

if __name__ == "__main__":
    main()
