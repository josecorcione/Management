import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="FinPath Panama",
    page_icon="💰",
    layout="wide"
)

# Initialize session state
if 'transactions' not in st.session_state:
    st.session_state.transactions = []

# Sidebar navigation
st.sidebar.title("FinPath 💰")
page = st.sidebar.radio(
    "Navigate to",
    ["Dashboard", "Add Transaction", "Financial Reports", "Business Progress"]
)

# Dashboard page
if page == "Dashboard":
    st.title("Business Dashboard")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    # Calculate metrics from transactions
    total_income = sum(t['amount'] for t in st.session_state.transactions 
                      if t['type'] == 'Income')
    total_expenses = sum(t['amount'] for t in st.session_state.transactions 
                        if t['type'] == 'Expense')
    cash_flow = total_income - total_expenses
    
    with col1:
        st.metric("Total Income", f"${total_income:,.2f}", "")
    with col2:
        st.metric("Total Expenses", f"${total_expenses:,.2f}", "")
    with col3:
        st.metric("Cash Flow", f"${cash_flow:,.2f}", "")
    
    # Transactions table
    if st.session_state.transactions:
        st.subheader("Recent Transactions")
        df = pd.DataFrame(st.session_state.transactions)
        st.dataframe(df)
        
        # Simple visualization
        if len(df) > 0:
            fig = px.pie(df, values='amount', names='type', title='Income vs Expenses')
            st.plotly_chart(fig)

# Add Transaction page
elif page == "Add Transaction":
    st.title("Add New Transaction")
    
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            transaction_date = st.date_input("Date", date.today())
            amount = st.number_input("Amount ($)", min_value=0.0)
            transaction_type = st.selectbox("Type", ["Income", "Expense"])
        
        with col2:
            category = st.selectbox(
                "Category",
                ["Sales", "Services", "Inventory", "Rent", "Utilities", "Other"]
            )
            description = st.text_input("Description")
            receipt = st.file_uploader("Upload Receipt", type=['png', 'jpg', 'pdf'])
        
        submit = st.form_submit_button("Save Transaction")
        
        if submit:
            new_transaction = {
                'date': transaction_date.strftime('%Y-%m-%d'),
                'amount': amount,
                'type': transaction_type,
                'category': category,
                'description': description
            }
            st.session_state.transactions.append(new_transaction)
            st.success("Transaction saved successfully!")

# Financial Reports page
elif page == "Financial Reports":
    st.title("Financial Reports")
    
    # Time period selector
    period = st.selectbox("Select Period", ["This Month", "Last Month", "Last 3 Months", "This Year"])
    
    tab1, tab2 = st.tabs(["Income Statement", "Cash Flow"])
    
    with tab1:
        if st.session_state.transactions:
            df = pd.DataFrame(st.session_state.transactions)
            
            # Income Statement
            st.subheader("Simple Income Statement")
            
            total_income = df[df['type'] == 'Income']['amount'].sum()
            total_expenses = df[df['type'] == 'Expense']['amount'].sum()
            net_income = total_income - total_expenses
            
            income_statement = pd.DataFrame({
                'Item': ['Total Income', 'Total Expenses', 'Net Income'],
                'Amount': [total_income, total_expenses, net_income]
            })
            
            st.dataframe(income_statement)
            
            # Visualization
            fig = go.Figure(data=[
                go.Bar(name='Income', x=['Income'], y=[total_income]),
                go.Bar(name='Expenses', x=['Expenses'], y=[total_expenses]),
                go.Bar(name='Net Income', x=['Net Income'], y=[net_income])
            ])
            st.plotly_chart(fig)
    
    with tab2:
        st.subheader("Cash Flow Statement")
        if st.session_state.transactions:
            df['date'] = pd.to_datetime(df['date'])
            df_sorted = df.sort_values('date')
            
            # Calculate running balance
            df_sorted['running_balance'] = df_sorted.apply(
                lambda x: x['amount'] if x['type'] == 'Income' else -x['amount'],
                axis=1
            ).cumsum()
            
            # Plot cash flow over time
            fig = px.line(df_sorted, x='date', y='running_balance', 
                         title='Cash Flow Over Time')
            st.plotly_chart(fig)

# Business Progress page
elif page == "Business Progress":
    st.title("Business Progress")
    
    # Progress metrics
    if st.session_state.transactions:
        num_transactions = len(st.session_state.transactions)
        progress = min(num_transactions / 100, 1.0)  # Example progress calculation
        
        st.subheader("Formalization Progress")
        st.progress(progress)
        st.write(f"Progress: {progress*100:.1f}%")
        
        # Achievements
        st.subheader("Achievements")
        col1, col2 = st.columns(2)
        
        with col1:
            if num_transactions >= 1:
                st.success("✅ First transaction recorded")
            if num_transactions >= 10:
                st.success("✅ 10 transactions milestone")
            if num_transactions >= 50:
                st.success("✅ 50 transactions milestone")
        
        with col2:
            if total_income > 0:
                st.success("✅ First income recorded")
            if total_income > 1000:
                st.success("✅ $1,000 income milestone")
            if total_income > 5000:
                st.success("✅ $5,000 income milestone")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("FinPath - Supporting Panama's Business Growth")
