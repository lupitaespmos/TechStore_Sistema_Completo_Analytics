import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
df = pd.read_csv("dataset.csv")  # usa tu archivo exportado

st.title("Dashboard Predictivo E-commerce")

st.sidebar.header("Simulador de Escenarios")

mejora = st.sidebar.slider(
    "Incremento en segmento premium (%)",
    0, 20, 5
) / 100

# KPIs
ingreso_total = df['monetary'].sum()
cluster_top = df.groupby('cluster_kmeans')['monetary'].mean().idxmax()
ingreso_segmento = df[df['cluster_kmeans']==cluster_top]['monetary'].sum()

incremento = ingreso_segmento * mejora
nuevo_ingreso = ingreso_total + incremento

st.metric("Ingreso Actual", f"${ingreso_total:,.0f}")
st.metric("Nuevo Ingreso Proyectado", f"${nuevo_ingreso:,.0f}")
st.metric("Incremento Estimado", f"{(incremento/ingreso_total)*100:.2f}%")

# Gráfico interactivo
fig = px.scatter(df,
                 x='recency',
                 y='monetary',
                 color='cluster_kmeans',
                 title='Segmentación de Clientes')
st.plotly_chart(fig)
