import streamlit as st
import pandas as pd
from datetime import datetime, date
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="FinPath Panama",
    page_icon="💰",
    layout="wide"
)

# Inicializar el estado de la sesión
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'customers' not in st.session_state:
    st.session_state.customers = []
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'goals' not in st.session_state:
    st.session_state.goals = {
        'monthly_revenue': 5000,
        'customer_growth': 0.1,
        'profit_margin': 0.3
    }

# Navegación lateral
st.sidebar.title("FinPath 💰")
page = st.sidebar.radio(
    "Navegar a",
    ["Dashboard", "Clientes", "Inventario", "Análisis de Negocio", "Transacciones", "Metas y KPIs"]
)

def calculate_business_metrics():
    if not st.session_state.transactions:
        return {}
    
    df = pd.DataFrame(st.session_state.transactions)
    df['date'] = pd.to_datetime(df['date'])
    
    # Métricas financieras básicas
    total_income = df[df['type'] == 'Ingreso']['amount'].sum()
    total_expenses = df[df['type'] == 'Gasto']['amount'].sum()
    
    # Análisis temporal
    monthly_revenue = df[df['type'] == 'Ingreso'].groupby(df['date'].dt.strftime('%Y-%m'))['amount'].sum()
    revenue_growth = monthly_revenue.pct_change().fillna(0)
    
    # Márgenes y rentabilidad
    profit_margin = (total_income - total_expenses) / total_income if total_income > 0 else 0
    
    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'profit_margin': profit_margin,
        'monthly_revenue': monthly_revenue,
        'revenue_growth': revenue_growth
    }

if page == "Dashboard":
    st.title("Dashboard Ejecutivo")
    
    metrics = calculate_business_metrics()
    
    # KPIs principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Ingresos Totales", f"${metrics.get('total_income', 0):,.2f}")
    with col2:
        st.metric("Margen de Beneficio", f"{metrics.get('profit_margin', 0)*100:.1f}%")
    with col3:
        st.metric("Clientes Activos", len(st.session_state.customers))
    with col4:
        recent_growth = metrics.get('revenue_growth', pd.Series()).iloc[-1] if len(metrics.get('revenue_growth', pd.Series())) > 0 else 0
        st.metric("Crecimiento Mensual", f"{recent_growth*100:.1f}%")
    
    # Gráficos de tendencias
    st.subheader("Tendencias del Negocio")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Ingresos Mensuales")
        if 'monthly_revenue' in metrics:
            st.line_chart(metrics['monthly_revenue'])
    
    with col2:
        st.write("Crecimiento de Ingresos")
        if 'revenue_growth' in metrics:
            st.line_chart(metrics['revenue_growth'])

elif page == "Clientes":
    st.title("Gestión de Clientes")
    
    # Agregar nuevo cliente
    with st.expander("Agregar Nuevo Cliente"):
        with st.form("new_customer"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nombre")
                email = st.text_input("Email")
                phone = st.text_input("Teléfono")
            with col2:
                category = st.selectbox("Categoría", ["Regular", "Premium", "Corporativo"])
                acquisition_date = st.date_input("Fecha de Adquisición")
            
            if st.form_submit_button("Guardar Cliente"):
                new_customer = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'category': category,
                    'acquisition_date': acquisition_date.strftime('%Y-%m-%d'),
                    'lifetime_value': 0
                }
                st.session_state.customers.append(new_customer)
                st.success("Cliente agregado exitosamente")
    
    # Análisis de clientes
    if st.session_state.customers:
        st.subheader("Análisis de Clientes")
        
        df_customers = pd.DataFrame(st.session_state.customers)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("Distribución por Categoría")
            category_dist = df_customers['category'].value_counts()
            st.bar_chart(category_dist)
        
        with col2:
            st.write("Adquisición de Clientes por Mes")
            df_customers['acquisition_date'] = pd.to_datetime(df_customers['acquisition_date'])
            monthly_acquisition = df_customers.groupby(df_customers['acquisition_date'].dt.strftime('%Y-%m')).size()
            st.line_chart(monthly_acquisition)

elif page == "Análisis de Negocio":
    st.title("Análisis Profundo del Negocio")
    
    metrics = calculate_business_metrics()
    
    # Análisis de rentabilidad
    st.subheader("Análisis de Rentabilidad")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Margen de Beneficio por Mes")
        if st.session_state.transactions:
            df = pd.DataFrame(st.session_state.transactions)
            df['date'] = pd.to_datetime(df['date'])
            monthly_data = df.groupby([df['date'].dt.strftime('%Y-%m'), 'type'])['amount'].sum().unstack()
            monthly_margin = (monthly_data['Ingreso'] - monthly_data['Gasto']) / monthly_data['Ingreso']
            st.line_chart(monthly_margin)
    
    with col2:
        st.write("Distribución de Gastos")
        if st.session_state.transactions:
            expenses = df[df['type'] == 'Gasto'].groupby('category')['amount'].sum()
            st.bar_chart(expenses)
    
    # Análisis predictivo simple
    st.subheader("Predicciones y Tendencias")
    if 'monthly_revenue' in metrics and len(metrics['monthly_revenue']) > 0:
        # Tendencia lineal simple
        x = np.arange(len(metrics['monthly_revenue']))
        y = metrics['monthly_revenue'].values
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        
        next_month_prediction = p(len(x))
        st.metric(
            "Predicción de Ingresos Próximo Mes",
            f"${next_month_prediction:,.2f}",
            f"{((next_month_prediction/metrics['monthly_revenue'].iloc[-1])-1)*100:.1f}%"
        )

elif page == "Metas y KPIs":
    st.title("Metas y KPIs del Negocio")
    
    # Configurar metas
    st.subheader("Configurar Metas del Negocio")
    with st.form("goals_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            monthly_revenue_goal = st.number_input(
                "Meta de Ingresos Mensuales ($)",
                value=st.session_state.goals['monthly_revenue']
            )
        with col2:
            customer_growth_goal = st.number_input(
                "Meta de Crecimiento de Clientes (%)",
                value=st.session_state.goals['customer_growth'] * 100
            ) / 100
        with col3:
            profit_margin_goal = st.number_input(
                "Meta de Margen de Beneficio (%)",
                value=st.session_state.goals['profit_margin'] * 100
            ) / 100
        
        if st.form_submit_button("Actualizar Metas"):
            st.session_state.goals.update({
                'monthly_revenue': monthly_revenue_goal,
                'customer_growth': customer_growth_goal,
                'profit_margin': profit_margin_goal
            })
            st.success("Metas actualizadas exitosamente")
    
    # Seguimiento de KPIs
    st.subheader("Seguimiento de KPIs")
    metrics = calculate_business_metrics()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_monthly_revenue = metrics.get('monthly_revenue', pd.Series()).iloc[-1] if len(metrics.get('monthly_revenue', pd.Series())) > 0 else 0
        revenue_progress = current_monthly_revenue / st.session_state.goals['monthly_revenue']
        st.metric(
            "Progreso hacia Meta de Ingresos",
            f"${current_monthly_revenue:,.2f}",
            f"Meta: ${st.session_state.goals['monthly_revenue']:,.2f}"
        )
        st.progress(min(revenue_progress, 1.0))
    
    with col2:
        current_margin = metrics.get('profit_margin', 0)
        st.metric(
            "Progreso hacia Meta de Margen",
            f"{current_margin*100:.1f}%",
            f"Meta: {st.session_state.goals['profit_margin']*100:.1f}%"
        )
        st.progress(min(current_margin / st.session_state.goals['profit_margin'], 1.0))
    
    with col3:
        # Calcular crecimiento de clientes
        if st.session_state.customers:
            df_customers = pd.DataFrame(st.session_state.customers)
            df_customers['acquisition_date'] = pd.to_datetime(df_customers['acquisition_date'])
            monthly_customers = df_customers.groupby(df_customers['acquisition_date'].dt.strftime('%Y-%m')).size()
            customer_growth = monthly_customers.pct_change().iloc[-1] if len(monthly_customers) > 1 else 0
        else:
            customer_growth = 0
        
        st.metric(
            "Crecimiento de Clientes",
            f"{customer_growth*100:.1f}%",
            f"Meta: {st.session_state.goals['customer_growth']*100:.1f}%"
        )
        st.progress(min(customer_growth / st.session_state.goals['customer_growth'], 1.0))

# Mantener la página de transacciones existente...
elif page == "Transacciones":
    st.title("Registro de Transacciones")
    
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            transaction_date = st.date_input("Fecha", date.today())
            amount = st.number_input("Monto ($)", min_value=0.0)
            transaction_type = st.selectbox("Tipo", ["Ingreso", "Gasto"])
        
        with col2:
            category = st.selectbox(
                "Categoría",
                ["Ventas", "Servicios", "Inventario", "Alquiler", "Servicios Públicos", "Otro"]
            )
            description = st.text_input("Descripción")
            customer = st.selectbox(
                "Cliente",
                [""] + [c['name'] for c in st.session_state.customers]
            ) if st.session_state.customers else st.text_input("Cliente")
        
        submit = st.form_submit_button("Guardar Transacción")
        
        if submit:
            new_transaction = {
                'date': transaction_date.strftime('%Y-%m-%d'),
                'amount': amount,
                'type': transaction_type,
                'category': category,
                'description': description,
                'customer': customer
            }
            st.session_state.transactions.append(new_transaction)
            
            # Actualizar lifetime value del cliente si existe
            if customer and st.session_state.customers:
                for c in st.session_state.customers:
                    if c['name'] == customer and transaction_type == 'Ingreso':
                        c['lifetime_value'] = c.get('lifetime_value', 0) + amount
            
            st.success("¡Transacción guardada exitosamente!")

# Pie de página
st.sidebar.markdown("---")
st.sidebar.markdown("FinPath - Impulsando el Crecimiento Empresarial en Panamá")
