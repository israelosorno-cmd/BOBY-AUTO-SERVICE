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
TU_TELEFONO = "17134018085" # Número ya integrado

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

# --- VISTA DEL CLIENTE (REPORTE PARA FIRMAR) ---
if es_cliente:
    nombre_c = query_params.get("cliente", "Estimado Cliente")
    monto_c = float(query_params.get("monto", 0))
    auto_c = query_params.get("auto", "Vehículo")
    total_con_tax = monto_c * 1.0715 # Tax de Utah

    st.markdown(f'<div class="main-header"><h1>REPORTE DE INSPECCIÓN DIGITAL</h1><h3>{auto_c}</h3></div>', unsafe_allow_html=True)
    st.write(f"### Hola {nombre_c},")
    st.write("A continuación se presenta el estado de su vehículo y el presupuesto para su aprobación.")
    
    st.metric("Total Presupuestado (inc. Tax 7.15%)", f"${total_con_tax:.2f}")
    
    st.markdown('<div class="section-blue">AUTORIZACIÓN LEGAL</div>', unsafe_allow_html=True)
    st.markdown('<div class="legal-box">Al firmar, autorizo a Service Pro Mobile a realizar las reparaciones. Entiendo que los precios son estimaciones y acepto las condiciones de servicio en Utah.</div>', unsafe_allow_html=True)
    
    firma = st.text_input("Escriba su nombre completo para firmar")
    if st.button("✅ APROBAR Y ENVIAR AL TALLER"):
        if firma:
            msg_conf = f"✅ *ORDEN APROBADA*\nYo, {firma}, autorizo el servicio para mi {auto_c} por un total de ${total_con_tax:.2f}."
            wa_api = f"https://api.whatsapp.com/send?phone={TU_TELEFONO}&text={urllib.parse.quote(msg_conf)}"
            st.success("¡Gracias! Presione el botón de abajo para enviar la confirmación final.")
            st.markdown(f'<a href="{wa_api}" target="_blank"><button style="width:100%; background-color:#004a99; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">Confirmar Firma vía WhatsApp 📲</button></a>', unsafe_allow_html=True)

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
                msg_w = f"🛠️ *SERVICE PRO MOBILE*\nHola {nombre}, adjunto el reporte de su {vehiculo}. Total: ${(presupuesto*1.0715):.2f}. Firme aquí: {link_f}"
                wa_send = f"https://api.whatsapp.com/send?phone={whatsapp}&text={urllib.parse.quote(msg_w)}"
                st.markdown(f'<a href="{wa_send}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">📲 ENVIAR REPORTE AL CLIENTE</button></a>', unsafe_allow_html=True)

    with tab2:
        st.header("Control de Ingresos Diarios")
        st.info("Aquí podrás ver el resumen de tus cierres diarios con el 7.15% de tax de Utah aplicado.")
