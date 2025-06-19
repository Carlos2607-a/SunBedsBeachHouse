import streamlit as st
import pandas as pd

st.title("Registro de Ventas de Hamacas")

# Estado inicial
if "ventas" not in st.session_state:
    st.session_state.ventas = []

# ¿Es fin de semana?
dia_especial = st.checkbox("¿Fin de Semana? (Precios: 40 / 35)")

precio_primera = 40 if dia_especial else 35
precio_segunda = 35 if dia_especial else 30

# Formulario para nueva venta
with st.form("registro_venta"):
    numero = st.number_input("Número de hamaca", min_value=1, step=1)
    primera_linea = st.checkbox("¿Primera línea?")
    cantidad = st.number_input("Cantidad vendida", min_value=1, step=1)
    forma_pago = st.selectbox("Forma de pago", ["Efectivo", "Tarjeta", "Cuenta habitación", "Invitación"])
    submit = st.form_submit_button("Registrar venta")

    if submit:
        precio_unitario = precio_primera if primera_linea else precio_segunda
        total = precio_unitario * cantidad
        st.session_state.ventas.append({
            "Hamaca": numero,
            "Primera línea": "Sí" if primera_linea else "No",
            "Forma de pago": forma_pago,
            "Cantidad": cantidad,
            "Precio unitario": precio_unitario,
            "Total": total
        })
        st.success("Venta registrada correctamente")

# Mostrar ventas
df = pd.DataFrame(st.session_state.ventas)
if not df.empty:
    st.subheader("Ventas registradas")
    st.dataframe(df)

    st.subheader("Resumen del día")

    # Total general de hamacas
    total_hamacas = df["Cantidad"].sum()
    total_euros = df["Total"].sum()
    st.write(f"🪑 Total de hamacas vendidas: **{total_hamacas}**")
    st.write(f"💶 Total general: **€{total_euros}**")

    # Desglose por precio unitario
    st.markdown("### 📊 Detalle por precio unitario")
    resumen_precio = df.groupby("Precio unitario").agg(
        Cantidad=("Cantidad", "sum"),
        Total_Euros=("Total", "sum")
    ).reset_index()
    st.dataframe(resumen_precio)

    # Desglose por forma de pago
    st.markdown("### 💳 Detalle por forma de pago")
    resumen_pago = df.groupby("Forma de pago").agg(
        Cantidad=("Cantidad", "sum"),
        Total_Euros=("Total", "sum")
    ).reset_index()
    st.dataframe(resumen_pago)

else:
    st.info("Aún no se ha registrado ninguna venta.")
