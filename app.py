import streamlit as st
import time
from datetime import datetime
import requests

st.set_page_config(page_title="TaxiTech Systems (Producción)", page_icon="🚖", layout="wide")

# URL base de nuestra API REST en FastAPI
API_BASE_URL = "http://127.0.0.1:8000"

# --- Funciones de comunicación con la API ---

def api_iniciar_carrera(estado_inicial):
    try:
        response = requests.post(f"{API_BASE_URL}/carreras/iniciar", json={"estado_inicial": estado_inicial})
        if response.status_code == 200:
            return response.json().get("id_carrera")
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Error de conexión con la API REST.")
    return None

def api_actualizar_estado(carrera_id, estado_actual):
    try:
        requests.put(f"{API_BASE_URL}/carreras/{carrera_id}/estado", json={"estado_actual": estado_actual})
    except requests.exceptions.ConnectionError:
        pass

def api_finalizar_carrera(carrera_id, duracion, importe):
    try:
        payload = {"duracion_segundos": duracion, "importe_eur": importe}
        response = requests.post(f"{API_BASE_URL}/carreras/{carrera_id}/finalizar", json=payload)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Error de conexión al finalizar la carrera.")
    return None

def api_obtener_historial():
    try:
        response = requests.get(f"{API_BASE_URL}/carreras")
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.ConnectionError:
        return []
    return []

# --- Interfaz Gráfica con Streamlit ---

st.title("🚖 TaxiTech - Sistema de Taxímetro (Modo Producción)")

# Inicializar estados de sesión
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "carrera_activa" not in st.session_state:
    st.session_state.carrera_activa = False
if "carrera_id" not in st.session_state:
    st.session_state.carrera_id = None
if "estado_movimiento" not in st.session_state:
    st.session_state.estado_movimiento = "parado"
if "tiempo_inicio" not in st.session_state:
    st.session_state.tiempo_inicio = 0.0
if "ultima_carrera" not in st.session_state:
    st.session_state.ultima_carrera = None

# 1. Pantalla de Login (US-08)
if not st.session_state.autenticado:
    st.subheader("🔐 Acceso de Conductor / Gestor")
    password = st.text_input("Introduce la contraseña:", type="password")
    
    if st.button("Iniciar Sesión"):
        if password == "taxitech123":
            st.session_state.autenticado = True
            st.success("¡Acceso concedido!")
            st.rerun()
        else:
            st.error("Contraseña incorrecta. Prueba con 'taxitech123'")
else:
    # Barra superior
    col_info, col_btn = st.columns([3, 1])
    with col_info:
        st.success("✅ Sesión iniciada - Conectado a Backend FastAPI & SQLite")
    with col_btn:
        if st.button("Cerrar Sesión"):
            st.session_state.autenticado = False
            st.session_state.carrera_activa = False
            st.session_state.carrera_id = None
            st.session_state.ultima_carrera = None
            st.rerun()

    st.markdown("---")

    # 2. Pantalla Principal
    if not st.session_state.carrera_activa:
        st.subheader("🚗 Estado: Libre / Preparado")
        
        if st.session_state.ultima_carrera:
            st.success("🏁 ¡Carrera cobrada y registrada en la Base de Datos!")
            ticket = st.session_state.ultima_carrera
            st.info(f"""
            **🧾 TICKET DE CARRERA (ID: {ticket.get('id')})**
            - **Fecha:** {ticket['fecha']}
            - **Duración:** {ticket['duracion_segundos']} segundos
            - **Total Cobrado:** **{ticket['importe_eur']} €**
            """)
            st.markdown("---")

        if st.button("🟢 Iniciar Nueva Carrera", type="primary", use_container_width=True):
            nuevo_id = api_iniciar_carrera("parado")
            if nuevo_id:
                st.session_state.carrera_id = nuevo_id
                st.session_state.carrera_activa = True
                st.session_state.tiempo_inicio = time.time()
                st.session_state.estado_movimiento = "parado"
                st.session_state.ultima_carrera = None
                st.rerun()
            else:
                st.error("No se pudo iniciar la carrera con la API.")

        # --- PANEL WEB DEL GESTOR DE FLOTA (Requisito 3) ---
        st.markdown("---")
        st.subheader("📊 Panel de Flota: Historial Global de Operaciones")
        
        historial_flota = api_obtener_historial()
        if historial_flota:
            st.dataframe(
                historial_flota,
                column_config={
                    "id": "ID",
                    "fecha": "Fecha y Hora",
                    "duracion_segundos": "Duración (s)",
                    "importe_eur": "Importe (€)",
                    "estado_final": "Estado"
                },
                use_container_width=True
            )
        else:
            st.info("No hay carreras completadas registradas en la base de datos todavía.")

    else:
        st.subheader("⏱️ Carrera en Curso")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛑 Parado (<20 km/h) - 0.02€/s", use_container_width=True):
                st.session_state.estado_movimiento = "parado"
                api_actualizar_estado(st.session_state.carrera_id, "parado")
        with col2:
            if st.button("🚀 En Movimiento - 0.05€/s", use_container_width=True):
                st.session_state.estado_movimiento = "movimiento"
                api_actualizar_estado(st.session_state.carrera_id, "movimiento")

        if st.session_state.estado_movimiento == "parado":
            st.warning("🛑 Vehículo en estado: **PARADO (<20 km/h)** -> Tarifa: 0.02 €/s")
        else:
            st.info("🚀 Vehículo en estado: **EN MOVIMIENTO** -> Tarifa: 0.05 €/s")

        duracion_actual = time.time() - st.session_state.tiempo_inicio
        tarifa = 0.02 if st.session_state.estado_movimiento == "parado" else 0.05
        coste_actual = round(duracion_actual * tarifa, 2)

        st.metric(label="Importe Actual Estimado", value=f"{coste_actual:.2f} €", delta=f"{duracion_actual:.1f} s transcurridos")

        if st.button("🏁 Finalizar y Cobrar Carrera", type="secondary", use_container_width=True):
            duracion_final = round(duracion_actual, 2)
            resultado_carrera = api_finalizar_carrera(st.session_state.carrera_id, duracion_final, coste_actual)
            
            if resultado_carrera:
                st.session_state.ultima_carrera = resultado_carrera
                st.session_state.carrera_activa = False
                st.session_state.carrera_id = None
                st.balloons()
                st.rerun()
            
        time.sleep(1)
        st.rerun()