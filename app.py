import streamlit as st
import time
import json
import os
from datetime import datetime

st.set_page_config(page_title="TaxiTech Systems", page_icon="🚖")

HISTORY_FILE = "historial_carreras.json"

def guardar_carrera(datos_carrera):
    historial = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                historial = json.load(f)
        except json.JSONDecodeError:
            historial = []
    historial.append(datos_carrera)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=4, ensure_ascii=False)

st.title("🚖 TaxiTech - Sistema de Taxímetro (Madrid)")

# Inicializar estados de sesión
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "carrera_activa" not in st.session_state:
    st.session_state.carrera_activa = False
if "estado_movimiento" not in st.session_state:
    st.session_state.estado_movimiento = "parado"
if "tiempo_inicio" not in st.session_state:
    st.session_state.tiempo_inicio = 0.0
if "ultima_carrera" not in st.session_state:
    st.session_state.ultima_carrera = None

# 1. Pantalla de Login (US-08)
if not st.session_state.autenticado:
    st.subheader("🔐 Acceso de Conductor")
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
        st.success("✅ Sesión iniciada como Conductor Autorizado")
    with col_btn:
        if st.button("Cerrar Sesión"):
            st.session_state.autenticado = False
            st.session_state.carrera_activa = False
            st.session_state.ultima_carrera = None
            st.rerun()

    st.markdown("---")

    # 2. Pantalla Principal (Libre o En Curso)
    if not st.session_state.carrera_activa:
        st.subheader("🚗 Estado: Libre / Preparado")
        
        # Si hay una carrera reciente, mostramos su ticket en pantalla
        if st.session_state.ultima_carrera:
            st.success("🏁 ¡Última carrera cobrada con éxito!")
            ticket = st.session_state.ultima_carrera
            st.info(f"""
            **🧾 TICKET DE CARRERA**
            - **Fecha:** {ticket['fecha']}
            - **Duración:** {ticket['duracion_segundos']} segundos
            - **Total Cobrado:** **{ticket['importe_eur']} €**
            """)
            st.markdown("---")

        if st.button("🟢 Iniciar Nueva Carrera", type="primary", use_container_width=True):
            st.session_state.carrera_activa = True
            st.session_state.tiempo_inicio = time.time()
            st.session_state.estado_movimiento = "parado"
            st.session_state.ultima_carrera = None # Limpiamos el ticket anterior al iniciar una nueva
            st.rerun()
    else:
        st.subheader("⏱️ Carrera en Curso")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛑 Parado (<20 km/h) - 0.02€/s", use_container_width=True):
                st.session_state.estado_movimiento = "parado"
        with col2:
            if st.button("🚀 En Movimiento - 0.05€/s", use_container_width=True):
                st.session_state.estado_movimiento = "movimiento"

        if st.session_state.estado_movimiento == "parado":
            st.warning("🛑 Vehículo en estado: **PARADO (<20 km/h)** -> Tarifa: 0.02 €/s")
        else:
            st.info("🚀 Vehículo en estado: **EN MOVIMIENTO** -> Tarifa: 0.05 €/s")

        # Cálculo en tiempo real
        duracion_actual = time.time() - st.session_state.tiempo_inicio
        tarifa = 0.02 if st.session_state.estado_movimiento == "parado" else 0.05
        coste_actual = round(duracion_actual * tarifa, 2)

        st.metric(label="Importe Actual Estimado", value=f"{coste_actual:.2f} €", delta=f"{duracion_actual:.1f} s transcurridos")

        # Botón Finalizar
        if st.button("🏁 Finalizar y Cobrar Carrera", type="secondary", use_container_width=True):
            datos_carrera = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "duracion_segundos": round(duracion_actual, 2),
                "importe_eur": coste_actual
            }
            guardar_carrera(datos_carrera)
            
            # Guardamos en la sesión para mostrar el ticket en la pantalla principal
            st.session_state.ultima_carrera = datos_carrera
            st.session_state.carrera_activa = False
            st.balloons()
            st.rerun()
            
        # Refresco automático de la pantalla cada segundo mientras dura la carrera
        time.sleep(1)
        st.rerun()