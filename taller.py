import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN Y ESTILOS PROFESIONALES
st.set_page_config(page_title="Service Pro Mobile - DVI", layout="wide", page_icon="🔧")

st.markdown("""
    <style>
    .main-header { background-color: #004a99; color: white; padding: 20px; text-align: center; border-radius: 10px; margin-bottom: 20px; }
    .category-header { background-color: #004a99; color: white; padding: 10px; font-weight: bold; margin-top: 30px; border-radius: 5px; text-transform: uppercase; }
    .legal-box { font-size: 11px; color: #444; background-color: #f0f2f6; padding: 15px; border-radius: 5px; border-left: 5px solid #ff4b4b; margin: 20px 0; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# CONFIGURACIÓN MAESTRA
URL_APP = "https://fufwyy3an9x.streamlit.app"
TU_TELEFONO = "17134018085" # Tu número de Utah integrado

query_params = st.query_params
es_cliente = "cliente" in query_params

# Función para crear filas de inspección
def fila_inspeccion(label, key):
    col_text, col_status, col_photo = st.columns([3, 2, 2])
    with col_text:
        st.write(f"**{label}**")
    with col_status:
        estado = st.select_slider("Estado", options=["🚨", "⚠️", "✅"], value="✅", key=f"status_{key}", label_visibility="collapsed")
    with col_photo:
        if st.checkbox("📸 Foto", key=f"show_cam_{key}"):
            st.camera_input(f"Captura {label}", key=f"cam_{key}", label_visibility="collapsed")
    return estado

# --- VISTA DEL CLIENTE (REPORTE PARA FIRMAR O RECHAZAR) ---
if es_cliente:
    nombre_c = query_params.get("cliente", "Estimado Cliente")
    monto_c = float(query_params.get("monto", 0))
    auto_c = query_params.get("auto", "Vehículo")
    total_con_tax = monto_c * 1.0715 # Tax de Utah

    st.markdown(f'<div class="main-header"><h1>REPORTE DE INSPECCIÓN DIGITAL</h1><h3>{auto_c}</h3></div>', unsafe_allow_html=True)
    st.write(f"### Hola {nombre_c},")
    st.write("Revise el presupuesto y el estado de su vehículo para proceder con la autorización.")
    
    st.metric("Total Presupuestado (inc. Tax 7.15%)", f"${total_con_tax:.2f}")
    
    st.markdown('<div class="legal-box">Al autorizar, Service Pro Mobile procederá con la reparación. Si decide rechazar, se le pedirá informar el motivo para nuestros registros.</div>', unsafe_allow_html=True)
    
    col_aprobar, col_rechazar = st.columns(2)
    
    with col_aprobar:
        firma = st.text_input("Escriba su nombre para ACEPTAR")
        if st.button("✅ APROBAR SERVICIO"):
            if firma:
                msg_conf = f"✅ *ORDEN APROBADA*\nYo, {firma}, autorizo el servicio para mi {auto_c} por un total de ${total_con_tax:.2f}."
                wa_api = f"https://api.whatsapp.com/send?phone={7134018085}&text={urllib.parse.quote(msg_conf)}"
                st.success("¡Aprobado! Presione abajo para confirmar.")
                st.markdown(f'<a href="{wa_api}" target="_blank"><button style="width:100%; background-color:#004a99; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">Confirmar Aprobación 📲</button></a>', unsafe_allow_html=True)
            else:
                st.error("Debe firmar para aprobar.")

    with col_rechazar:
        motivo = st.text_input("Motivo del RECHAZO (opcional)")
        if st.button("❌ RECHAZAR SERVICIO"):
            msg_rechazo = f"❌ *SERVICIO RECHAZADO*\nEl cliente {nombre_c} ha rechazado el presupuesto para su {auto_c}.\nMotivo: {motivo if motivo else 'No especificado'}."
            wa_api_r = f"https://api.whatsapp.com/send?phone={7134018085}&text={urllib.parse.quote(msg_rechazo)}"
            st.warning("Rechazo registrado. Por favor, infórmenos vía WhatsApp.")
            st.markdown(f'<a href="{wa_api_r}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">Enviar Rechazo al Técnico 📲</button></a>', unsafe_allow_html=True)

# --- VISTA DEL TÉCNICO (PANEL DE CONTROL) ---
else:
    tab1, tab2 = st.tabs(["📋 Nueva Inspección", "📈 Reporte de Ingresos"])
    
    with tab1:
        st.markdown('<div class="main-header"><h1>Service Pro Mobile - Panel Técnico</h1></div>', unsafe_allow_html=True)
        with st.form("inspeccion_completa"):
            c1, c2 = st.columns(2)
            nombre = c1.text_input("Nombre del Cliente")
            whatsapp = c1.text_input("WhatsApp Cliente (1801XXXXXXX)")
            vehiculo = c2.text_input("Vehículo (Año/Modelo)")
            presupuesto = c2.number_input("Presupuesto Base ($)", min_value=0.0)

            st.markdown('<div class="category-header">1. Motor y Líquidos</div>', unsafe_allow_html=True)
            fila_inspeccion("Aceite y Filtro", "oil")
            fila_inspeccion("Líquido de Frenos", "b_fluid")
            st.text_area("Notas Motor", key="n_motor")

            st.markdown('<div class="category-header">2. Frenos y Llantas</div>', unsafe_allow_html=True)
            fila_inspeccion("Frenos Delanteros", "f_brakes")
            fila_inspeccion("Llantas / Presión", "tires")
            st.text_area("Notas Frenos", key="n_frenos")

            enviar = st.form_submit_button("🚀 GENERAR REPORTE")

            if enviar and nombre and whatsapp:
                p = f"?cliente={urllib.parse.quote(nombre)}&monto={presupuesto}&auto={urllib.parse.quote(vehiculo)}"
                link_f = URL_APP + p
                msg_w = f"🛠️ *SERVICE PRO MOBILE*\nHola {nombre}, adjunto el reporte de su {vehiculo}. Total: ${(presupuesto*1.0715):.2f}. Revise aquí: {link_f}"
                wa_send = f"https://api.whatsapp.com/send?phone={whatsapp}&text={urllib.parse.quote(msg_w)}"
                st.markdown(f'<a href="{wa_send}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">📲 ENVIAR REPORTE AL CLIENTE</button></a>', unsafe_allow_html=True)

    with tab2:
        st.header("Control de Ingresos Diarios")
        st.info("Aquí podrás ver el resumen de tus cierres diarios con el 7.15% de tax de Utah aplicado.")

