import streamlit as st
import pandas as pd

st.title("Registro de Ventas de Hamacas")

# Estado inicial de las ventas
if "ventas" not in st.session_state:
    st.session_state.ventas = []

# Selección del día para definir precios
dia_especial = st.checkbox("¿Fin de Semana? (Precios: 40 / 35)")

precio_primera = 40 if dia_especial else 35
precio_segunda = 35 if dia_especial else 30

# Formulario para agregar nueva venta
with st.form("registro_venta"):
    numero = st.number_input("Número de hamaca", min_value=1, step=1)
    primera_linea = st.checkbox("¿Primera línea?")
    cantidad = st.number_input("Cantidad vendida", min_value=1, step=1)
    forma_pago = st.selectbox("Forma de pago", ["Efectivo", "Tarjeta", "Cuenta habitación", "Invitación"])
    submit = st.form_submit_button("Registrar venta")

    if submit:
        precio = precio_primera if primera_linea else precio_segunda
        total = precio * cantidad
        st.session_state.ventas.append({
            "Hamaca": numero,
            "Primera línea": "Sí" if primera_linea else "No",
            "Forma de pago": forma_pago,
            "Precio": precio,
            "Cantidad": cantidad,
            "Total": total
        })
        st.success("Venta registrada correctamente")

# Mostrar ventas registradas
df = pd.DataFrame(st.session_state.ventas)

if not df.empty:
    st.subheader("Ventas registradas")
    st.dataframe(df)

    st.subheader("Resumen del día")

    # Cantidad y total por línea
    cantidad_primera = df[df["Primera línea"] == "Sí"]["Cantidad"].sum()
    cantidad_segunda = df[df["Primera línea"] == "No"]["Cantidad"].sum()

    total_primera = df[df["Primera línea"] == "Sí"]["Total"].sum()
    total_segunda = df[df["Primera línea"] == "No"]["Total"].sum()
    total_general = df["Total"].sum()
    cantidad_total = df["Cantidad"].sum()

    st.write(f"Cantidad hamacas Primera Línea: {cantidad_primera}")
    st.write(f"Cantidad hamacas Segunda Línea: {cantidad_segunda}")
    st.write(f"Total Primera Línea: €{total_primera}")
    st.write(f"Total Segunda Línea: €{total_segunda}")
    st.write(f"Cantidad total de hamacas: {cantidad_total}")
    st.write(f"Total general: €{total_general}")

    st.subheader("Totales por forma de pago")
    resumen_pago = df.groupby("Forma de pago").agg(
        Cantidad=("Cantidad", "sum"),
        Total_Euros=("Total", "sum")
    ).reset_index()
    st.dataframe(resumen_pago)

else:
    st.info("Aún no se ha registrado ninguna venta.")
