import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

st.title("📋 Registro de Ventas de Hamacas")

# Crear carpeta para los archivos si no existe
os.makedirs("ventas_por_dia", exist_ok=True)

# Obtener fecha de hoy
fecha_hoy = date.today().isoformat()
archivo_csv = f"ventas_por_dia/ventas_{fecha_hoy}.csv"

# Cargar ventas del archivo si ya existe
if "ventas" not in st.session_state or st.session_state.get("fecha") != fecha_hoy:
    if os.path.exists(archivo_csv):
        st.session_state.ventas = pd.read_csv(archivo_csv).to_dict("records")
    else:
        st.session_state.ventas = []
    st.session_state.fecha = fecha_hoy  # actualizar fecha en sesión

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
        hora_actual = datetime.now().strftime("%H:%M:%S")
        st.session_state.ventas.append({
            "Fecha": fecha_hoy,
            "Hora": hora_actual,
            "Hamaca": numero,
            "Primera línea": "Sí" if primera_linea else "No",
            "Forma de pago": forma_pago,
            "Precio": precio,
            "Cantidad": cantidad,
            "Total": total
        })
        st.success("✅ Venta registrada correctamente")

        # Guardar en el archivo CSV del día
        df_actualizado = pd.DataFrame(st.session_state.ventas)
        df_actualizado.to_csv(archivo_csv, index=False)

# Mostrar ventas registradas
df = pd.DataFrame(st.session_state.ventas)

if not df.empty:
    st.subheader("🧾 Ventas registradas")
    st.dataframe(df)

    st.subheader("📊 Resumen del día")

    # Cantidad y total por línea
    cantidad_primera = df[df["Primera línea"] == "Sí"]["Cantidad"].sum()
    cantidad_segunda = df[df["Primera línea"] == "No"]["Cantidad"].sum()

    total_primera = df[df["Primera línea"] == "Sí"]["Total"].sum()
    total_segunda = df[df["Primera línea"] == "No"]["Total"].sum()
    total_general = df["Total"].sum()
    cantidad_total = df["Cantidad"].sum()

    st.write(f"🟩 Cantidad Primera Línea: {cantidad_primera}")
    st.write(f"🟦 Cantidad Segunda Línea: {cantidad_segunda}")
    st.write(f"💰 Total Primera Línea: €{total_primera}")
    st.write(f"💳 Total Segunda Línea: €{total_segunda}")
    st.write(f"📦 Cantidad total de hamacas: {cantidad_total}")
    st.write(f"💵 Total general del día: €{total_general}")

    st.subheader("💳 Totales por forma de pago")
    resumen_pago = df.groupby("Forma de pago").agg(
        Cantidad=("Cantidad", "sum"),
        Total_Euros=("Total", "sum")
    ).reset_index()
    st.dataframe(resumen_pago)

    # Botón para descargar el archivo del día
    st.download_button(
        label="📥 Descargar CSV del día",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=archivo_csv.split("/")[-1],
        mime="text/csv"
    )

else:
    st.info("ℹ️ Aún no se ha registrado ninguna venta hoy.")
