import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Ejecutivo", layout="wide")

st.title("📊 Dashboard Ejecutivo - Análisis Comercial")

# =============================
# CARGA DE DATOS
# =============================

@st.cache_data
def load_data():
    churn = pd.read_csv("churn_data.csv")
    clientes = pd.read_csv("clientes_base.csv")
    productos = pd.read_csv("productos_catalogo.csv")
    transacciones = pd.read_csv("transacciones.csv")
    ventas = pd.read_csv("ventas_historicas.csv")
    return churn, clientes, productos, transacciones, ventas

churn, clientes, productos, transacciones, ventas = load_data()

# =============================
# MÉTRICAS PRINCIPALES
# =============================

st.subheader("📌 KPIs Generales")

col1, col2, col3, col4 = st.columns(4)

total_ventas = ventas["ventas"].sum() if "ventas" in ventas.columns else len(transacciones)
total_clientes = clientes.shape[0]
total_productos = productos.shape[0]
churn_rate = churn["churn"].mean() * 100 if "churn" in churn.columns else 0

col1.metric("Ventas Totales", f"${total_ventas:,.0f}")
col2.metric("Clientes Totales", total_clientes)
col3.metric("Productos", total_productos)
col4.metric("Tasa de Churn (%)", f"{churn_rate:.2f}%")

# =============================
# VENTAS EN EL TIEMPO
# =============================

st.subheader("📈 Evolución de Ventas")

if "fecha" in ventas.columns:
    ventas["fecha"] = pd.to_datetime(ventas["fecha"])
    ventas_agrupadas = ventas.groupby("fecha")["ventas"].sum()

    fig, ax = plt.subplots()
    ax.plot(ventas_agrupadas.index, ventas_agrupadas.values)
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Ventas")
    st.pyplot(fig)

# =============================
# DISTRIBUCIÓN DE CHURN
# =============================

st.subheader("📉 Distribución de Churn")

if "churn" in churn.columns:
    churn_counts = churn["churn"].value_counts()

    fig2, ax2 = plt.subplots()
    ax2.pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%')
    st.pyplot(fig2)

# =============================
# TABLAS EXPLORABLES
# =============================

st.subheader("🔍 Exploración de Datos")

dataset_option = st.selectbox(
    "Selecciona dataset:",
    ["Clientes", "Productos", "Transacciones", "Ventas", "Churn"]
)

if dataset_option == "Clientes":
    st.dataframe(clientes)

elif dataset_option == "Productos":
    st.dataframe(productos)

elif dataset_option == "Transacciones":
    st.dataframe(transacciones)

elif dataset_option == "Ventas":
    st.dataframe(ventas)

elif dataset_option == "Churn":
    st.dataframe(churn)

st.success("Dashboard cargado correctamente 🚀")
