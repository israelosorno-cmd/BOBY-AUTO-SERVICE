import streamlit as st
import urllib.parse

# 1. SISTEMA MULTI-IDIOMA
if 'lang' not in st.session_state:
    st.session_state.lang = 'Español'

def t(es, en):
    return es if st.session_state.lang == 'Español' else en

# 2. CONFIGURACIÓN Y ESTILOS
st.set_page_config(page_title="Service Pro Mobile - DVI", layout="wide", page_icon="🔧")

st.sidebar.selectbox("Language / Idioma", ["Español", "English"], key='lang')

st.markdown(f"""
    <style>
    .main-header {{ background-color: #004a99; color: white; padding: 20px; text-align: center; border-radius: 10px; margin-bottom: 20px; }}
    .category-header {{ background-color: #004a99; color: white; padding: 10px; font-weight: bold; margin-top: 25px; border-radius: 5px; text-transform: uppercase; border-left: 10px solid #ff4b4b; }}
    .legal-box {{ font-size: 11px; color: #444; background-color: #f0f2f6; padding: 15px; border-radius: 5px; border-left: 5px solid #ff4b4b; margin: 20px 0; }}
    .stButton>button {{ width: 100%; border-radius: 10px; font-weight: bold; height: 3em; }}
    </style>
    """, unsafe_allow_html=True)

# CONFIGURACIÓN MAESTRA
URL_APP = "https://fufwyy3an9x.streamlit.app"
TU_TELEFONO = "17134018085" 

query_params = st.query_params
es_cliente = "cliente" in query_params

def fila_inspeccion(label_es, label_en, key):
    label = t(label_es, label_en)
    col_text, col_status, col_photo = st.columns([3, 2, 2])
    with col_text:
        st.write(f"**{label}**")
    with col_status:
        estado = st.select_slider(t("Estado", "Status"), options=["🚨", "⚠️", "✅"], value="✅", key=f"status_{key}", label_visibility="collapsed")
    with col_photo:
        if st.checkbox(t("📸 Foto", "📸 Photo"), key=f"show_cam_{key}"):
            st.camera_input(f"Captura {label}", key=f"cam_{key}", label_visibility="collapsed")
    return estado

# --- VISTA DEL CLIENTE ---
if es_cliente:
    nombre_c = query_params.get("cliente", "Customer")
    monto_c = float(query_params.get("monto", 0))
    auto_c = query_params.get("auto", "Vehicle")
    total_con_tax = monto_c * 1.0715 

    st.markdown(f'<div class="main-header"><h1>{t("REPORTE DE INSPECCIÓN DIGITAL", "DIGITAL INSPECTION REPORT")}</h1><h3>{auto_c}</h3></div>', unsafe_allow_html=True)
    st.write(f"### {t('Hola', 'Hello')} {nombre_c},")
    st.write(t("Revise el estado de su vehículo y el presupuesto para su aprobación.", "Please review your vehicle's status and the estimate for your approval."))
    
    st.metric(t("Total (inc. Tax 7.15%)", "Total (inc. 7.15% Tax)"), f"${total_con_tax:.2f}")
    
    col_aprobar, col_rechazar = st.columns(2)
    with col_aprobar:
        st.subheader(t("Aprobar", "Approve"))
        firma = st.text_input(t("Nombre completo para FIRMAR", "Full name to SIGN"))
        if st.button(t("✅ ACEPTAR", "✅ ACCEPT")):
            if firma:
                msg = f"✅ *ORDER APPROVED*\n{t('Yo', 'I')}, {firma}, {t('autorizo el servicio por', 'authorize service for')} ${total_con_tax:.2f}."
                wa_api = f"https://api.whatsapp.com/send?phone={TU_TELEFONO}&text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{wa_api}" target="_blank"><button style="width:100%; background-color:#004a99; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">{t("Confirmar Firma", "Confirm Signature")} 📲</button></a>', unsafe_allow_html=True)

    with col_rechazar:
        st.subheader(t("Rechazar", "Decline"))
        motivo = st.text_input(t("Motivo (opcional)", "Reason (optional)"))
        if st.button(t("❌ RECHAZAR", "❌ DECLINE")):
            msg_r = f"❌ *SERVICE DECLINED*\n{t('El cliente', 'Customer')} {nombre_c} {t('rechazó el presupuesto', 'declined the estimate')}.\n{t('Motivo', 'Reason')}: {motivo if motivo else 'N/A'}."
            wa_api_r = f"https://api.whatsapp.com/send?phone={TU_TELEFONO}&text={urllib.parse.quote(msg_r)}"
            st.markdown(f'<a href="{wa_api_r}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">{t("Enviar Rechazo", "Send Decline")} 📲</button></a>', unsafe_allow_html=True)

# --- VISTA DEL TÉCNICO ---
else:
    st.markdown(f'<div class="main-header"><h1>Service Pro Mobile - {t("Panel Técnico", "Technician Panel")}</h1></div>', unsafe_allow_html=True)
    with st.form("inspeccion_total"):
        c1, c2, c3 = st.columns(3)
        nombre = c1.text_input(t("Nombre del Cliente", "Customer Name"))
        whatsapp = c1.text_input(t("WhatsApp (17134018085)", "WhatsApp (17134018085)"))
        vehiculo = c2.text_input(t("Vehículo", "Vehicle"))
        millaje = c2.text_input(t("Millaje", "Odometer"))
        presupuesto = c3.number_input(t("Presupuesto Base ($)", "Base Estimate ($)"), min_value=0.0)
        vin = c3.text_input("VIN")

        st.markdown(f'<div class="category-header">1. {t("Motor y Líquidos", "Engine & Fluids")}</div>', unsafe_allow_html=True)
        fila_inspeccion("Aceite y Filtro", "Oil & Filter", "oil")
        fila_inspeccion("Anticongelante", "Coolant", "coolant")
        fila_inspeccion("Líquido de Frenos", "Brake Fluid", "b_fluid")

        st.markdown(f'<div class="category-header">2. {t("Frenos y Llantas", "Brakes & Tires")}</div>', unsafe_allow_html=True)
        fila_inspeccion("Pastillas/Discos", "Pads/Rotors", "brakes_st")
        fila_inspeccion("Llantas", "Tires", "tires_st")

        if st.form_submit_button(f"🚀 {t('GENERAR REPORTE', 'GENERATE REPORT')}"):
            if nombre and whatsapp:
                total_tax = presupuesto * 1.0715
                p = f"?cliente={urllib.parse.quote(nombre)}&monto={presupuesto}&auto={urllib.parse.quote(vehiculo)}"
                link_f = URL_APP + p
                msg_w = f"🛠️ *REPORTE SERVICE PRO*\n{t('Hola', 'Hello')} {nombre}, {t('adjunto su reporte', 'here is your report')}. Total: ${total_tax:.2f}. {t('Firme aquí', 'Sign here')}: {link_f}"
                wa_send = f"https://api.whatsapp.com/send?phone={whatsapp}&text={urllib.parse.quote(msg_w)}"
                st.markdown(f'<a href="{wa_send}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">📲 {t("ENVIAR AL CLIENTE", "
