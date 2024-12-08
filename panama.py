import streamlit as st
import pandas as pd
from datetime import datetime, date

# Configuración de la página
st.set_page_config(
    page_title="FinPath Panama",
    page_icon="💰",
    layout="wide"
)

# Inicializar el estado de la sesión
if 'transactions' not in st.session_state:
    st.session_state.transactions = []

# Navegación lateral
st.sidebar.title("FinPath 💰")
page = st.sidebar.radio(
    "Navegar a",
    ["Dashboard", "Agregar Transacción", "Reportes Financieros", "Progreso"]
)

# Página de Dashboard
if page == "Dashboard":
    st.title("Dashboard del Negocio")
    
    # Métricas clave
    col1, col2, col3 = st.columns(3)
    
    # Calcular métricas de transacciones
    total_income = sum(t['amount'] for t in st.session_state.transactions 
                      if t['type'] == 'Ingreso')
    total_expenses = sum(t['amount'] for t in st.session_state.transactions 
                        if t['type'] == 'Gasto')
    cash_flow = total_income - total_expenses
    
    with col1:
        st.metric("Ingresos Totales", f"${total_income:,.2f}", "")
    with col2:
        st.metric("Gastos Totales", f"${total_expenses:,.2f}", "")
    with col3:
        st.metric("Flujo de Caja", f"${cash_flow:,.2f}", "")
    
    # Tabla de transacciones
    if st.session_state.transactions:
        st.subheader("Transacciones Recientes")
        df = pd.DataFrame(st.session_state.transactions)
        st.dataframe(df)
        
        # Métricas adicionales
        st.subheader("Análisis Simple")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Distribución de Gastos por Categoría:")
            if len(df[df['type'] == 'Gasto']) > 0:
                gastos_por_categoria = df[df['type'] == 'Gasto'].groupby('category')['amount'].sum()
                st.bar_chart(gastos_por_categoria)
        
        with col2:
            st.write("Ingresos vs Gastos:")
            comparacion = pd.DataFrame({
                'Tipo': ['Ingresos', 'Gastos'],
                'Monto': [total_income, total_expenses]
            }).set_index('Tipo')
            st.bar_chart(comparacion)

# Página de Agregar Transacción
elif page == "Agregar Transacción":
    st.title("Agregar Nueva Transacción")
    
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
            receipt = st.file_uploader("Subir Recibo", type=['png', 'jpg', 'pdf'])
        
        submit = st.form_submit_button("Guardar Transacción")
        
        if submit:
            new_transaction = {
                'date': transaction_date.strftime('%Y-%m-%d'),
                'amount': amount,
                'type': transaction_type,
                'category': category,
                'description': description
            }
            st.session_state.transactions.append(new_transaction)
            st.success("¡Transacción guardada exitosamente!")

# Página de Reportes Financieros
elif page == "Reportes Financieros":
    st.title("Reportes Financieros")
    
    # Selector de período
    period = st.selectbox("Seleccionar Período", 
                         ["Este Mes", "Mes Pasado", "Últimos 3 Meses", "Este Año"])
    
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)
        
        st.subheader("Estado de Resultados Simple")
        
        income_statement = pd.DataFrame({
            'Ítem': ['Ingresos Totales', 'Gastos Totales', 'Ganancia Neta'],
            'Monto': [total_income, total_expenses, net_income]
        })
        
        st.table(income_statement)
        
        # Análisis por categoría
        st.subheader("Análisis por Categoría")
        category_analysis = df.groupby(['type', 'category'])['amount'].sum()
        st.write(category_analysis)

# Página de Progreso
elif page == "Progreso":
    st.title("Progreso del Negocio")
    
    if st.session_state.transactions:
        num_transactions = len(st.session_state.transactions)
        progress = min(num_transactions / 100, 1.0)
        
        st.subheader("Progreso de Formalización")
        st.progress(progress)
        st.write(f"Progreso: {progress*100:.1f}%")
        
        # Logros
        st.subheader("Logros")
        col1, col2 = st.columns(2)
        
        with col1:
            if num_transactions >= 1:
                st.success("✅ Primera transacción registrada")
            if num_transactions >= 10:
                st.success("✅ 10 transacciones registradas")
            if num_transactions >= 50:
                st.success("✅ 50 transacciones registradas")
        
        with col2:
            if total_income > 0:
                st.success("✅ Primer ingreso registrado")
            if total_income > 1000:
                st.success("✅ $1,000 en ingresos alcanzado")
            if total_income > 5000:
                st.success("✅ $5,000 en ingresos alcanzado")

# Pie de página
st.sidebar.markdown("---")
st.sidebar.markdown("FinPath - Apoyando el Crecimiento Empresarial en Panamá")
