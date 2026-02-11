import streamlit as st
import urllib.parse
import pandas as pd
import os
from datetime import datetime

# 1. CONFIGURACIÓN PROFESIONAL
st.set_page_config(page_title="Service Pro Mobile - Digital DVI", layout="wide", page_icon="🔧")

# URL de tu app (Actualizada según tu imagen)
URL_APP = "https://tallerpy-jywboxpvgwzfufwyy3an9x.streamlit.app"

# 2. CAPTURA DE DATOS DEL LINK (Lo que evita que el cliente vea tu panel)
query_params = st.query_params
es_cliente = "cliente" in query_params

# 3. ESTILOS
st.markdown("""
    <style>
    .main-header { background-color: #004a99; color: white; padding: 20px; text-align: center; border-radius: 10px; }
    .section-blue { background-color: #004a99; color: white; padding: 10px; font-weight: bold; margin-top: 20px; border-radius: 5px; }
    .legal-box { font-size: 11px; color: #444; background-color: #f0f2f6; padding: 15px; border-radius: 5px; border-left: 5px solid #ff4b4b; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- VISTA DEL CLIENTE (Lo que recibirá por WhatsApp) ---
if es_cliente:
    nombre_c = query_params["cliente"]
    monto_c = float(query_params.get("monto", 0))
    auto_c = query_params.get("auto", "Vehículo")
    total_con_tax = monto_c * 1.0715 # Tax de Utah aplicado

    st.markdown(f'<div class="main-header"><h1>REPORTE DE SERVICIO</h1><h3>{auto_c}</h3></div>', unsafe_allow_html=True)
    st.write(f"### Estimado(a) {nombre_c},")
    st.write("A continuación, presentamos los resultados de la inspección técnica y el presupuesto para su aprobación.")
    
    st.metric("Total a Pagar (inc. Tax 7.15%)", f"${total_con_tax:.2f}")
    
    st.markdown('<div class="section-blue">AUTORIZACIÓN LEGAL</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-box">
    Al firmar, autorizo a Service Pro Mobile a realizar las reparaciones descritas. 
    Entiendo que los precios son estimaciones y pueden variar. No nos hacemos responsables 
    por artículos dejados en el vehículo o daños pre-existentes no detectados.
    </div>
    """, unsafe_allow_html=True)
    
    firma = st.text_input("Escriba su nombre completo como firma de aceptación")
    if st.button("✅ APROBAR Y ENVIAR AL TALLER"):
        if firma:
            st.success("¡Gracias! Su aprobación ha sido enviada. El técnico iniciará el trabajo pronto.")
            # Aquí se guardaría en tu base de datos para tu reporte diario
        else:
            st.error("Por favor, escriba su nombre para firmar la aprobación.")

# --- VISTA DEL TÉCNICO (Lo que solo ves tú) ---
else:
    tab_inspeccion, tab_ingresos = st.tabs(["📋 Nueva Inspección", "📈 Reporte de Ingresos"])
    
    with tab_inspeccion:
        st.markdown('<div class="main-header"><h1>Panel de Control Técnico</h1></div>', unsafe_allow_html=True)
        with st.form("form_taller"):
            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input("Nombre del Cliente")
                tel = st.text_input("WhatsApp (Ej: 801XXXXXXX)")
            with col2:
                veh = st.text_input("Vehículo")
                pre = st.number_input("Presupuesto ($)", min_value=0.0)
            
            sent = st.form_submit_button("🚀 GENERAR LINK PARA CLIENTE")
            
            if sent and nom and tel:
                # CREACIÓN DEL LINK INTELIGENTE
                p = f"?cliente={urllib.parse.quote(nom)}&monto={pre}&auto={urllib.parse.quote(veh)}"
                link_final = URL_APP + p
                
                mensaje = f"🛠️ *SERVICE PRO MOBILE*\nHola {nom}, aquí puede ver el reporte y aprobar el servicio de su {veh}: {link_final}"
                wa_url = f"https://wa.me/{tel}?text={urllib.parse.quote(mensaje)}"
                
                st.info(f"Link generado para {nom}")
                st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">📲 ENVIAR POR WHATSAPP</button></a>', unsafe_allow_html=True)

    with tab_ingresos:
        st.header("Reporte de Ingresos Diarios")
        st.write("Aquí verás el resumen de lo aprobado hoy con el tax del 7.15%.")

