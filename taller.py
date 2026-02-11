import streamlit as st
import urllib.parse

# 1. SISTEMA DE IDIOMAS (Superior Derecha)
if 'lang' not in st.session_state:
    st.session_state.lang = 'Español'

def t(es, en):
    return es if st.session_state.lang == 'Español' else en

# 2. CONFIGURACIÓN Y ESTILOS
st.set_page_config(page_title="Service Pro Mobile - Full DVI", layout="wide", page_icon="🔧")

st.markdown(f"""
    <style>
    .main-header {{ background-color: #004a99; color: white; padding: 20px; text-align: center; border-radius: 10px; margin-bottom: 20px; }}
    .category-header {{ background-color: #004a99; color: white; padding: 10px; font-weight: bold; margin-top: 25px; border-radius: 5px; text-transform: uppercase; border-left: 10px solid #ff4b4b; }}
    .invoice-box {{ background-color: #f8f9fa; border: 2px solid #004a99; padding: 25px; border-radius: 10px; margin-top: 20px; }}
    .stButton>button {{ width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }}
    </style>
    """, unsafe_allow_html=True)

col_head, col_lang = st.columns([5, 1])
with col_lang:
    st.selectbox("🌐", ["Español", "English"], key='lang', label_visibility="collapsed")

# 3. CONFIGURACIÓN MAESTRA
URL_APP = "https://service-pro-mobile-dvi.streamlit.app"
TU_TELEFONO = "17134018085" 

query_params = st.query_params
es_cliente = "cliente" in query_params

def fila_inspeccion(label_es, label_en, key):
    label = t(label_es, label_en)
    col_text, col_status, col_photo = st.columns([3, 2, 2])
    with col_text: st.write(f"**{label}**")
    with col_status: estado = st.select_slider(t("Estado", "Status"), options=["🚨", "⚠️", "✅"], value="✅", key=f"status_{key}", label_visibility="collapsed")
    with col_photo:
        if st.checkbox(t("📸 Foto", "📸 Photo"), key=f"show_cam_{key}"):
            st.camera_input(f"Captura {label}", key=f"cam_{key}", label_visibility="collapsed")
    return estado

# --- VISTA DEL CLIENTE (RESUMEN 27 PUNTOS + FACTURA + APROBACIÓN) ---
if es_cliente:
    nombre_c = query_params.get("cliente", t("Cliente", "Customer"))
    labor_c = float(query_params.get("monto", 0))
    partes_c = float(query_params.get("partes", 0))
    auto_c = query_params.get("auto", t("Vehículo", "Vehicle"))
    subtotal = labor_c + partes_c
    tax = subtotal * 0.0715
    total = subtotal + tax

    st.markdown(f'<div class="main-header"><h1>{t("INSPECCIÓN Y COTIZACIÓN DIGITAL", "DIGITAL INSPECTION & QUOTE")}</h1><h3>{auto_c}</h3></div>', unsafe_allow_html=True)
    
    # Módulo de Resumen de Facturación
    st.markdown(f"""
    <div class="invoice-box">
        <h4>{t("Resumen de Factura", "Invoice Summary")}</h4>
        <hr>
        <p><b>{t("Labor", "Labor")}:</b> ${labor_c:,.2f} | <b>{t("Partes", "Parts")}:</b> ${partes_c:,.2f}</p>
        <p><b>Tax (7.15%):</b> ${tax:,.2f}</p>
        <h2 style="color:#004a99;">TOTAL: ${total:,.2f}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    
    # Módulo de Decisión
    col_a, col_r = st.columns(2)
    with col_a:
        firma = st.text_input(t("Escriba su nombre para ACEPTAR", "Type name to APPROVE"))
        if st.button(t("✅ ACEPTAR Y FIRMAR", "✅ APPROVE & SIGN")):
            if firma:
                msg = f"✅ *APPROVED*\n{firma} {t('autoriza el trabajo por', 'authorizes work for')} ${total:,.2f}."
                wa = f"https://api.whatsapp.com/send?phone={TU_TELEFONO}&text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{wa}" target="_blank"><button style="width:100%; background-color:#004a99; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">{t("Confirmar Firma", "Confirm Signature")} 📲</button></a>', unsafe_allow_html=True)
    with col_r:
        motivo = st.text_input(t("Motivo de rechazo", "Reason for decline"))
        if st.button(t("❌ RECHAZAR", "❌ DECLINE")):
            msg_r = f"❌ *DECLINED*\n{nombre_c} {t('rechazó el servicio', 'declined service')}. {t('Motivo', 'Reason')}: {motivo}"
            wa_r = f"https://api.whatsapp.com/send?phone={TU_TELEFONO}&text={urllib.parse.quote(msg_r)}"
            st.markdown(f'<a href="{wa_r}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">{t("Enviar Rechazo", "Send Decline")} 📲</button></a>', unsafe_allow_html=True)

# --- VISTA DEL TÉCNICO (REGISTRO + INSPECCIÓN 27 PUNTOS + FACTURACIÓN) ---
else:
    st.markdown(f'<div class="main-header"><h1>Service Pro Mobile - {t("Panel de Control", "Control Panel")}</h1></div>', unsafe_allow_html=True)
    
    with st.form("master_form"):
        # MÓDULO 1: REGISTRO DE CLIENTE Y VEHÍCULO
        st.markdown(f'<div class="category-header">1. {t("Información General", "General Information")}</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        nombre = c1.text_input(t("Cliente", "Customer"))
        whatsapp = c1.text_input(t("WhatsApp (1XXXXXXXXXX)", "WhatsApp"))
        vehiculo = c2.text_input(t("Vehículo", "Vehicle"))
        millaje = c2.text_input(t("Millaje", "Odometer"))
        vin = c3.text_input("VIN")

        # MÓDULO 2: INSPECCIÓN DETALLADA (27 Puntos resumidos por categorías)
        st.markdown(f'<div class="category-header">2. {t("Inspección de 27 Puntos", "27-Point Inspection")}</div>', unsafe_allow_html=True)
        # Motor
        fila_inspeccion("Aceite y Filtro", "Oil & Filter", "oil")
        fila_inspeccion("Líquidos (Coolant/Frenos/Dirección)", "Fluids", "fluids")
        # Frenos y Llantas
        fila_inspeccion("Frenos Delanteros/Traseros", "Brakes Front/Rear", "brakes")
        fila_inspeccion("Llantas (Estado/Presión)", "Tires Condition/PSI", "tires")
        # Seguridad y Eléctrico
        fila_inspeccion("Batería y Alternador", "Battery & Alternator", "electrical")
        fila_inspeccion("Luces y Limpiaparabrisas", "Lights & Wipers", "safety")
        st.text_area(t("Hallazgos de la Inspección", "Inspection Findings"), key="notes_ins")

        # MÓDULO 3: CREACIÓN DE COTIZACIÓN Y FACTURA
        st.markdown(f'<div class="category-header">3. {t("Cotización y Facturación", "Quote & Billing")}</div>', unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        m_labor = f1.number_input(t("Mano de Obra ($)", "Labor Cost ($)"), min_value=0.0)
        m_partes = f2.number_input(t("Partes/Repuestos ($)", "Parts/Materials ($)"), min_value=0.0)

        if st.form_submit_button(f"🚀 {t('GENERAR Y ENVIAR AL CLIENTE', 'GENERATE & SEND TO CUSTOMER')}"):
            if nombre and whatsapp:
                p = f"?cliente={urllib.parse.quote(nombre)}&monto={m_labor}&partes={m_partes}&auto={urllib.parse.quote(vehiculo)}"
                link = URL_APP + p
                total_w = (m_labor + m_partes) * 1.0715
                msg_w = f"🛠️ *SERVICE PRO MOBILE*\n{t('Hola', 'Hello')} {nombre}, {t('revisa el reporte y factura de tu', 'check report and invoice for')} {vehiculo}.\nTotal: ${total_w:.2f}.\n{t('Link', 'Link')}: {link}"
                wa_send = f"https://api.whatsapp.com/send?phone={whatsapp}&text={urllib.parse.quote(msg_w)}"
                st.markdown(f'<a href="{wa_send}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">📲 {t("ENVIAR AL CLIENTE", "SEND TO CUSTOMER")}</button></a>', unsafe_allow_html=True)
