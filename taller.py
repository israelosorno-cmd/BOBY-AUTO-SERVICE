import streamlit as st
import urllib.parse

# 1. SISTEMA DE IDIOMAS
if 'lang' not in st.session_state:
    st.session_state.lang = 'Español'

def t(es, en):
    return es if st.session_state.lang == 'Español' else en

# 2. CONFIGURACIÓN Y ESTILOS
st.set_page_config(page_title="Service Pro Mobile - Facturación", layout="wide", page_icon="💰")

st.markdown(f"""
    <style>
    .main-header {{ background-color: #004a99; color: white; padding: 20px; text-align: center; border-radius: 10px; margin-bottom: 20px; }}
    .invoice-box {{ background-color: white; border: 2px solid #eee; padding: 25px; border-radius: 10px; margin-top: 20px; }}
    .category-header {{ background-color: #004a99; color: white; padding: 10px; font-weight: bold; margin-top: 25px; border-radius: 5px; text-transform: uppercase; border-left: 10px solid #ff4b4b; }}
    .stButton>button {{ width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }}
    </style>
    """, unsafe_allow_html=True)

# Selector de idioma superior derecho
col_head, col_lang = st.columns([5, 1])
with col_lang:
    st.selectbox("🌐", ["Español", "English"], key='lang', label_visibility="collapsed")

# 3. CONFIGURACIÓN MAESTRA
URL_APP = "https://service-pro-mobile-dvi.streamlit.app"
TU_TELEFONO = "17134018085" 

query_params = st.query_params
es_cliente = "cliente" in query_params

# --- VISTA DEL CLIENTE (FACTURA Y APROBACIÓN) ---
if es_cliente:
    nombre_c = query_params.get("cliente", t("Cliente", "Customer"))
    base_c = float(query_params.get("monto", 0))
    partes_c = float(query_params.get("partes", 0))
    auto_c = query_params.get("auto", t("Vehículo", "Vehicle"))
    
    subtotal = base_c + partes_c
    tax_total = subtotal * 0.0715
    total_final = subtotal + tax_total

    st.markdown(f'<div class="main-header"><h1>{t("FACTURA DE SERVICIO DIGITAL", "DIGITAL SERVICE INVOICE")}</h1></div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown(f"""
        <div class="invoice-box">
            <h3>{t("Resumen de Facturación", "Billing Summary")}</h3>
            <hr>
            <p><b>{t("Cliente", "Customer")}:</b> {nombre_c} | <b>{t("Vehículo", "Vehicle")}:</b> {auto_c}</p>
            <table style="width:100%">
                <tr><td>{t("Mano de Obra", "Labor")}</td><td style="text-align:right">${base_c:,.2f}</td></tr>
                <tr><td>{t("Partes y Repuestos", "Parts & Materials")}</td><td style="text-align:right">${partes_c:,.2f}</td></tr>
                <tr><td><br></td><td></td></tr>
                <tr><td><b>Subtotal</b></td><td style="text-align:right"><b>${subtotal:,.2f}</b></td></tr>
                <tr><td>Tax (7.15%)</td><td style="text-align:right">${tax_total:,.2f}</td></tr>
                <tr style="font-size: 20px; color: #004a99;"><td><b>TOTAL</b></td><td style="text-align:right"><b>${total_final:,.2f}</b></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    col_aprobar, col_rechazar = st.columns(2)
    with col_aprobar:
        firma = st.text_input(t("Firma (Escriba su nombre)", "Sign (Type your name)"))
        if st.button(t("✅ APROBAR Y PAGAR", "✅ APPROVE & PAY")):
            if firma:
                msg = f"✅ *INVOICE APPROVED*\n{t('Yo', 'I')}, {firma}, {t('autorizo el pago de', 'authorize payment of')} ${total_final:,.2f} {t('por el servicio de mi', 'for the service of my')} {auto_c}."
                wa_api = f"https://api.whatsapp.com/send?phone={TU_TELEFONO}&text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{wa_api}" target="_blank"><button style="width:100%; background-color:#004a99; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">{t("Confirmar y Enviar Pago", "Confirm & Send Payment")} 📲</button></a>', unsafe_allow_html=True)

# --- VISTA DEL TÉCNICO (GENERADOR DE FACTURAS) ---
else:
    st.markdown(f'<div class="main-header"><h1>Service Pro Mobile - {t("Generador de Facturas", "Invoice Generator")}</h1></div>', unsafe_allow_html=True)
    
    with st.form("invoice_form"):
        c1, c2 = st.columns(2)
        nombre = c1.text_input(t("Nombre del Cliente", "Customer Name"))
        whatsapp = c1.text_input(t("WhatsApp (1XXXXXXXXXX)", "WhatsApp"))
        vehiculo = c2.text_input(t("Vehículo", "Vehicle"))
        
        st.markdown(f'<div class="category-header">{t("Costos del Servicio", "Service Costs")}</div>', unsafe_allow_html=True)
        monto_labor = st.number_input(t("Mano de Obra ($)", "Labor Cost ($)"), min_value=0.0)
        monto_partes = st.number_input(t("Costo de Partes/Repuestos ($)", "Parts Cost ($)"), min_value=0.0)
        
        if st.form_submit_button(f"🚀 {t('GENERAR FACTURA Y ENVIAR', 'GENERATE & SEND INVOICE')}"):
            if nombre and whatsapp:
                params = f"?cliente={urllib.parse.quote(nombre)}&monto={monto_labor}&partes={monto_partes}&auto={urllib.parse.quote(vehiculo)}"
                link_f = URL_APP + params
                total_w = (monto_labor + monto_partes) * 1.0715
                msg_w = f"🛠️ *FACTURA SERVICE PRO MOBILE*\n{t('Hola', 'Hello')} {nombre}, {t('adjunto la factura de su', 'here is the invoice for your')} {vehiculo}.\nTotal: ${total_w:.2f}.\n{t('Revise y pague aquí', 'Review and pay here')}: {link_f}"
                wa_send = f"https://api.whatsapp.com/send?phone={whatsapp}&text={urllib.parse.quote(msg_w)}"
                st.markdown(f'<a href="{wa_send}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">📲 {t("ENVIAR FACTURA", "SEND INVOICE")}</button></a>', unsafe_allow_html=True)
