import streamlit as st
import urllib.parse
import pandas as pd
import os
from datetime import datetime

# Configuración Profesional
st.set_page_config(page_title="Service Pro Mobile - Digital DVI", layout="wide", page_icon="🔧")

# --- BASE DE DATOS LOCAL ---
DB_FILE = "registro_aprobaciones.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["Fecha", "Cliente", "Vehiculo", "Total", "Estado", "Firma"]).to_csv(DB_FILE, index=False)

# Estilos inspirados en tu imagen de "Certified Service"
st.markdown("""
    <style>
    .main-header { background-color: #004a99; color: white; padding: 20px; text-align: center; border-radius: 10px; }
    .section-blue { background-color: #004a99; color: white; padding: 10px; font-weight: bold; margin-top: 20px; border-radius: 5px; }
    .legal-box { font-size: 11px; color: #444; background-color: #f0f2f6; padding: 15px; border-radius: 5px; border-left: 5px solid #ff4b4b; margin: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# Manejo de Vistas (Técnico vs Cliente)
if 'view' not in st.session_state: st.session_state.view = 'tecnico'

# --- TABS PRINCIPALES ---
tab_inspeccion, tab_reporte_diario = st.tabs(["📋 Inspección y Envío", "📈 Reporte de Ingresos"])

with tab_inspeccion:
    if st.session_state.view == 'tecnico':
        st.markdown('<div class="main-header"><h1>Service Pro Mobile - Utah</h1><h3>Certified Multi-Point Inspection</h3></div>', unsafe_allow_html=True)
        
        with st.form("form_tecnico"):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre del Cliente")
                tel = st.text_input("WhatsApp (801XXXXXXX)")
            with col2:
                auto = st.text_input("Vehículo (Ej: 2008 Toyota Sienna)")
                monto_base = st.number_input("Presupuesto ($)", min_value=0.0)

            st.markdown('<div class="section-blue">INSPECCIÓN DE 27 PUNTOS</div>', unsafe_allow_html=True)
            
            def fila_tecnica(label, key):
                c1, c2, c3 = st.columns([3, 2, 3])
                with c1: st.write(f"**{label}**")
                with c2: est = st.select_slider("Status", ["🚨", "⚠️", "✅"], value="✅", key=f"s_{key}", label_visibility="collapsed")
                with c3:
                    foto = None
                    if st.checkbox("📸 Cámara", key=f"b_{key}"):
                        foto = st.camera_input(f"Captura {label}", key=f"c_{key}", label_visibility="collapsed")
                st.divider()
                return {"item": label, "status": est, "foto": foto}

            items = []
            items.append(fila_tecnica("Aceite de Motor", "oil"))
            items.append(fila_tecnica("Sistema de Frenos", "brk"))
            items.append(fila_tecnica("Llantas y Suspensión", "susp"))
            
            notas = st.text_area("Recomendaciones adicionales")
            btn_enviar = st.form_submit_button("🚀 GENERAR Y ENVIAR REPORTE")

        if btn_enviar and nombre and tel:
            total_tax = monto_base * 1.0715 # Aplicando el 7.15% de Utah
            st.session_state.reporte = {"cliente": nombre, "tel": tel, "auto": auto, "total": total_tax, "items": items, "notas": notas}
            
            # --- CONFIGURACIÓN DEL LINK ---
            # Reemplaza esta URL con el link exacto que ves en tu navegador
            url_app = "https://tallerpy-jywboxpvgwzfufwyy3an9x.streamlit.app/" 
            
            mensaje = f"🛠️ *CERTIFIED SERVICE PRO*\nHola {nombre}, revisa las fotos y firma la aprobación de tu {auto} aquí: {url_app}"
            wa_url = f"https://wa.me/{tel}?text={urllib.parse.quote(mensaje)}"
            
            st.success("✅ Reporte generado.")
            st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">📲 ENVIAR POR WHATSAPP</button></a>', unsafe_allow_html=True)

    elif st.session_state.view == 'cliente':
        # (Aquí iría la vista del cliente con fotos y firma digital que diseñamos antes)
        st.button("Regresar al Panel", on_click=lambda: st.session_state.update({"view": 'tecnico'}))

with tab_reporte_diario:
    st.header("📊 Resumen Financiero del Día")
    if os.path.exists(DB_FILE):
        df_ventas = pd.read_csv(DB_FILE)
        df_ventas['Fecha'] = pd.to_datetime(df_ventas['Fecha'])
        hoy = datetime.now().date()
        ventas_hoy = df_ventas[df_ventas['Fecha'].dt.date == hoy]
        
        if not ventas_hoy.empty:
            total_dia = ventas_hoy['Total'].astype(float).sum()
            subtotal_neto = total_dia / 1.0715
            tax_recaudado = total_dia - subtotal_neto
            
            c_a, c_b, c_c = st.columns(3)
            c_a.metric("Ventas Totales", f"${total_dia:.2f}")
            c_b.metric("Ingreso Neto", f"${subtotal_neto:.2f}")
            c_c.metric("Impuestos (7.15%)", f"${tax_recaudado:.2f}")
            st.table(ventas_hoy[['Cliente', 'Vehiculo', 'Total', 'Firma']])
        else:

            st.info("No hay servicios aprobados hoy todavía.")


