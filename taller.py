import streamlit as st
import urllib.parse

# 1. CONFIGURACIÓN DE IDIOMAS Y ESTILOS
if 'lang' not in st.session_state:
    st.session_state.lang = 'Español'

def t(es, en):
    return es if st.session_state.lang == 'Español' else en

st.set_page_config(page_title="Service Pro Mobile - DVI", layout="wide", page_icon="🔧")

st.markdown(f"""
    <style>
    .main-header {{ background-color: #004a99; color: white; padding: 20px; text-align: center; border-radius: 10px; margin-bottom: 20px; }}
    .category-header {{ background-color: #004a99; color: white; padding: 10px; font-weight: bold; margin-top: 15px; border-radius: 5px; text-transform: uppercase; border-left: 8px solid #ff4b4b; }}
    .invoice-box {{ background-color: #f8f9fa; border: 2px solid #004a99; padding: 20px; border-radius: 10px; }}
    .stButton>button {{ width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }}
    </style>
    """, unsafe_allow_html=True)

# Selector de idioma superior derecho
c_empty, c_lang = st.columns([5, 1])
with c_lang:
    st.selectbox("🌐", ["Español", "English"], key='lang', label_visibility="collapsed")

# 2. CONFIGURACIÓN MAESTRA
URL_APP = "https://service-pro-mobile-dvi.streamlit.app"
TU_TELEFONO = "17134018085" 

query_params = st.query_params
es_cliente = "cliente" in query_params

def fila_inspeccion(label_es, label_en, key):
    label = t(label_es, label_en)
    col_t, col_s, col_p = st.columns([3, 2, 2])
    with col_t: st.write(f"**{label}**")
    with col_s: estado = st.select_slider(t("Estado", "Status"), options=["🚨", "⚠️", "✅"], value="✅", key=f"s_{key}", label_visibility="collapsed")
    with col_p:
        if st.checkbox(t("📸 Foto", "📸 Photo"), key=f"p_{key}"):
            st.camera_input(f"Captura {label}", key=f"cam_{key}", label_visibility="collapsed")
    return estado

# --- SECCIÓN A: VISTA DEL CLIENTE (FACTURA + APROBACIÓN) ---
if es_cliente:
    nombre_c = query_params.get("cliente", t("Cliente", "Customer"))
    labor_c = float(query_params.get("monto", 0))
    partes_c = float(query_params.get("partes", 0))
    auto_c = query_params.get("auto", t("Vehículo", "Vehicle"))
    subtotal = labor_c + partes_c
    tax = subtotal * 0.0715
    total = subtotal + tax

    st.markdown(f'<div class="main-header"><h1>{t("INSPECCIÓN Y COTIZACIÓN", "INSPECTION & QUOTE")}</h1><h3>{auto_c}</h3></div>', unsafe_allow_html=True)
    
    st.markdown(f"""<div class="invoice-box"><h4>{t("Resumen de Factura", "Invoice Summary")}</h4><hr>
    <p><b>{t("Labor", "Labor")}:</b> ${labor_c:,.2f} | <b>{t("Partes", "Parts")}:</b> ${partes_c:,.2f}</p>
    <p><b>Tax (7.15%):</b> ${tax:,.2f}</p><h2 style="color:#004a99;">TOTAL: ${total:,.2f}</h2></div>""", unsafe_allow_html=True)

    st.divider()
    cA, cR = st.columns(2)
    with cA:
        f = st.text_input(t("Nombre para FIRMAR", "Name to SIGN"))
        if st.button(t("✅ APROBAR", "✅ APPROVE")):
            if f:
                msg = f"✅ *APPROVED*\n{f} {t('autoriza el trabajo por', 'authorizes work for')} ${total:,.2f}."
                wa = f"https://api.whatsapp.com/send?phone={TU_TELEFONO}&text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{wa}" target="_blank"><button style="width:100%; background-color:#004a99; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">{t("Confirmar Firma", "Confirm Signature")} 📲</button></a>', unsafe_allow_html=True)
    with cR:
        m = st.text_input(t("Motivo de rechazo", "Decline reason"))
        if st.button(t("❌ RECHAZAR", "❌ DECLINE")):
            msg_r = f"❌ *DECLINED*\n{nombre_c} {t('rechazó el servicio', 'declined service')}. {t('Motivo', 'Reason')}: {m}"
            wa_r = f"https://api.whatsapp.com/send?phone={TU_TELEFONO}&text={urllib.parse.quote(msg_r)}"
            st.markdown(f'<a href="{wa_r}" target="_blank"><button style="width:100%; background-color:#ff4b4b; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">{t("Enviar Rechazo", "Send Decline")} 📲</button></a>', unsafe_allow_html=True)

# --- SECCIÓN B: VISTA DEL TÉCNICO (MODULAR) ---
else:
    st.markdown(f'<div class="main-header"><h1>Service Pro Mobile - {t("Panel Técnico", "Technician Panel")}</h1></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([t("📝 Registro", "📝 Registration"), t("📋 Inspección 27 pts", "📋 27-pt Inspection"), t("💰 Facturación", "💰 Billing")])
    
    with tab1:
        st.markdown(f'<div class="category-header">1. {t("Datos del Cliente y Vehículo", "Customer & Vehicle Data")}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        nombre = c1.text_input(t("Nombre del Cliente", "Customer Name"), key="reg_nom")
        whatsapp = c1.text_input(t("WhatsApp (1XXXXXXXXXX)", "WhatsApp"), key="reg_wa")
        vehiculo = c2.text_input(t("Vehículo (Año/Modelo)", "Vehicle (Year/Model)"), key="reg_veh")
        millaje = c2.text_input(t("Millaje (Odometer)", "Odometer"), key="reg_mil")
        vin = st.text_input("VIN", key="reg_vin")

    with tab2:
        st.markdown(f'<div class="category-header">2. {t("Inspección Detallada", "Detailed Inspection")}</div>', unsafe_allow_html=True)
        st.subheader(t("Bajo el Capó", "Under the Hood"))
        fila_inspeccion("Aceite de Motor", "Engine Oil", "oil")
        fila_inspeccion("Anticongelante", "Coolant", "cool")
        fila_inspeccion("Líquido de Frenos", "Brake Fluid", "br_f")
        
        st.subheader(t("Frenos y Llantas", "Brakes & Tires"))
        fila_inspeccion("Pastillas Delanteras", "Front Pads", "f_p")
        fila_inspeccion("Presión de Llantas", "Tire Pressure", "t_p")
        
        st.subheader(t("Seguridad y Luces", "Safety & Lights"))
        fila_inspeccion("Batería", "Battery", "batt")
        fila_inspeccion("Luces Exteriores", "Exterior Lights", "lights")
        st.text_area(t("Notas de la Inspección", "Inspection Notes"), key="ins_notes")

    with tab3:
        st.markdown(f'<div class="category-header">3. {t("Cotización Final", "Final Quote")}</div>', unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        m_labor = f1.number_input(t("Mano de Obra ($)", "Labor ($)"), min_value=0.0, key="bill_lab")
        m_partes = f2.number_input(t("Partes/Materiales ($)", "Parts ($)"), min_value=0.0, key="bill_par")
        
        total_previo = (m_labor + m_partes) * 1.0715
        st.write(f"### {t('Total Estimado (inc. Tax):', 'Estimated Total (inc. Tax):')} ${total_previo:,.2f}")

        if st.button(f"🚀 {t('GENERAR Y ENVIAR AL CLIENTE', 'GENERATE & SEND TO CUSTOMER')}"):
            if nombre and whatsapp:
                p = f"?cliente={urllib.parse.quote(nombre)}&monto={m_labor}&partes={m_partes}&auto={urllib.parse.quote(vehiculo)}"
                link = URL_APP + p
                msg_w = f"🛠️ *SERVICE PRO MOBILE*\n{t('Hola', 'Hello')} {nombre}, {t('revisa el reporte y factura de tu', 'check report and invoice for')} {vehiculo}.\nTotal: ${total_previo:.2f}.\nLink: {link}"
                wa_send = f"https://api.whatsapp.com/send?phone={whatsapp}&text={urllib.parse.quote(msg_w)}"
                st.markdown(f'<a href="{wa_send}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">📲 {t("ENVIAR POR WHATSAPP", "SEND VIA WHATSAPP")}</button></a>', unsafe_allow_html=True)
            else:
                st.error(t("Faltan datos del cliente o teléfono.", "Missing customer data or phone number."))
