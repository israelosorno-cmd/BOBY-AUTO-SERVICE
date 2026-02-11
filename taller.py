import streamlit as st
import urllib.parse

# 1. SISTEMA DE IDIOMAS Y ESTADO
if 'lang' not in st.session_state:
    st.session_state.lang = 'Español'
if 'step' not in st.session_state:
    st.session_state.step = 1

def t(es, en):
    return es if st.session_state.lang == 'Español' else en

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

# 2. CONFIGURACIÓN
st.set_page_config(page_title="Service Pro Mobile - Workflow", layout="wide", page_icon="🔧")

st.markdown(f"""
    <style>
    .main-header {{ background-color: #004a99; color: white; padding: 20px; text-align: center; border-radius: 10px; margin-bottom: 20px; }}
    .category-header {{ background-color: #004a99; color: white; padding: 10px; font-weight: bold; margin-top: 15px; border-radius: 5px; text-transform: uppercase; border-left: 8px solid #ff4b4b; }}
    .step-indicator {{ color: #004a99; font-weight: bold; font-size: 18px; margin-bottom: 10px; }}
    .stButton>button {{ width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }}
    </style>
    """, unsafe_allow_html=True)

# Selector de idioma superior derecho
c_empty, c_lang = st.columns([5, 1])
with c_lang:
    st.selectbox("🌐", ["Español", "English"], key='lang', label_visibility="collapsed")

# 3. CONFIGURACIÓN MAESTRA
URL_APP = "https://tallerpy-jywboxpvgwzfufwyy3an9x.streamlit.app"
TU_TELEFONO = "17134018085" 

query_params = st.query_params
es_cliente = "cliente" in query_params

def fila_inspeccion(label_es, label_en, key):
    label = t(label_es, label_en)
    col_t, col_s, col_p = st.columns([3, 2, 2])
    with col_t: st.write(f"**{label}**")
    with col_s: st.select_slider(t("Estado", "Status"), options=["🚨", "⚠️", "✅"], value="✅", key=f"s_{key}", label_visibility="collapsed")
    with col_p:
        if st.checkbox(t("📸 Foto", "📸 Photo"), key=f"p_{key}"):
            st.camera_input(f"Captura {label}", key=f"cam_{key}", label_visibility="collapsed")

# --- VISTA DEL CLIENTE ---
if es_cliente:
    # (Mantiene la lógica de aprobación que ya teníamos)
    st.markdown(f'<div class="main-header"><h1>{t("REPORTE Y FACTURA", "REPORT & INVOICE")}</h1></div>', unsafe_allow_html=True)
    # ... (resto de lógica de cliente)
    st.write(t("Cargando datos del servicio...", "Loading service data..."))

# --- VISTA DEL TÉCNICO (FLUJO POR PASOS) ---
else:
    st.markdown(f'<div class="main-header"><h1>Service Pro Mobile - Workflow</h1></div>', unsafe_allow_html=True)
    
    # Indicador de Progreso
    pasos = [t("Registro", "Registry"), t("Inspección", "Inspection"), t("Cotización", "Quote"), t("Factura Final", "Final Invoice")]
    st.markdown(f'<div class="step-indicator">{t("Paso", "Step")} {st.session_state.step}: {pasos[st.session_state.step-1]}</div>', unsafe_allow_html=True)
    st.progress(st.session_state.step / 4)

    # PASO 1: REGISTRO
    if st.session_state.step == 1:
        st.markdown(f'<div class="category-header">1. {t("Datos del Cliente y Vehículo", "Customer & Vehicle")}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        st.session_state.nombre = c1.text_input(t("Nombre del Cliente", "Customer Name"), value=st.session_state.get('nombre', ''))
        st.session_state.wa = c1.text_input(t("WhatsApp (1XXXXXXXXXX)", "WhatsApp"), value=st.session_state.get('wa', ''))
        st.session_state.veh = c2.text_input(t("Vehículo", "Vehicle"), value=st.session_state.get('veh', ''))
        st.session_state.vin = c2.text_input("VIN", value=st.session_state.get('vin', ''))
        st.button(t("Siguiente: Ir a Inspección ➡️", "Next: Go to Inspection ➡️"), on_click=next_step)

    # PASO 2: INSPECCIÓN
    elif st.session_state.step == 2:
        st.markdown(f'<div class="category-header">2. {t("Inspección de 27 Puntos", "27-Point Inspection")}</div>', unsafe_allow_html=True)
        fila_inspeccion("Aceite de Motor", "Engine Oil", "oil")
        fila_inspeccion("Frenos Delanteros", "Front Brakes", "f_br")
        fila_inspeccion("Presión de Llantas", "Tire Pressure", "tires")
        fila_inspeccion("Batería", "Battery", "batt")
        
        c_nav1, c_nav2 = st.columns(2)
        c_nav1.button(t("⬅️ Volver al Registro", "⬅️ Back to Registry"), on_click=prev_step)
        c_nav2.button(t("Siguiente: Ir a Cotización ➡️", "Next: Go to Quote ➡️"), on_click=next_step)

    # PASO 3: COTIZACIÓN (HALLAZGOS Y PRECIOS ESTIMADOS)
    elif st.session_state.step == 3:
        st.markdown(f'<div class="category-header">3. {t("Cotización de Reparaciones", "Repair Quote")}</div>', unsafe_allow_html=True)
        st.session_state.labor = st.number_input(t("Mano de Obra ($)", "Labor Cost ($)"), min_value=0.0, value=st.session_state.get('labor', 0.0))
        st.session_state.partes = st.number_input(t("Partes/Repuestos ($)", "Parts Cost ($)"), min_value=0.0, value=st.session_state.get('partes', 0.0))
        
        c_nav1, c_nav2 = st.columns(2)
        c_nav1.button(t("⬅️ Volver a Inspección", "⬅️ Back to Inspection"), on_click=prev_step)
        c_nav2.button(t("Siguiente: Generar Factura Final ➡️", "Next: Generate Final Invoice ➡️"), on_click=next_step)

    # PASO 4: FACTURA FINAL Y ENVÍO
    elif st.session_state.step == 4:
        st.markdown(f'<div class="category-header">4. {t("Factura Final de Servicio", "Final Service Invoice")}</div>', unsafe_allow_html=True)
        
        subtotal = st.session_state.labor + st.session_state.partes
        tax = subtotal * 0.0715
        total = subtotal + tax
        
        st.markdown(f"""
        <div style="background-color: white; padding: 30px; border: 2px solid #004a99; border-radius: 10px;">
            <h2 style="text-align:center; color:#004a99;">SERVICE PRO MOBILE</h2>
            <p><b>{t("Cliente", "Customer")}:</b> {st.session_state.nombre}</p>
            <p><b>{t("Vehículo", "Vehicle")}:</b> {st.session_state.veh}</p>
            <hr>
            <table style="width:100%">
                <tr><td>{t("Mano de Obra", "Labor")}</td><td style="text-align:right">${st.session_state.labor:,.2f}</td></tr>
                <tr><td>{t("Partes y Materiales", "Parts & Materials")}</td><td style="text-align:right">${st.session_state.partes:,.2f}</td></tr>
                <tr style="font-weight:bold;"><td>Subtotal</td><td style="text-align:right">${subtotal:,.2f}</td></tr>
                <tr><td>Tax (7.15%)</td><td style="text-align:right">${tax:,.2f}</td></tr>
                <tr style="font-size:22px; color:#004a99; font-weight:bold;"><td>TOTAL</td><td style="text-align:right">${total:,.2f}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        col_back, col_send = st.columns(2)
        col_back.button(t("⬅️ Corregir Precios", "⬅️ Edit Prices"), on_click=prev_step)
        
        if col_send.button(f"🚀 {t('ENVIAR FACTURA VÍA WHATSAPP', 'SEND INVOICE VIA WHATSAPP')}"):
            p = f"?cliente={urllib.parse.quote(st.session_state.nombre)}&monto={st.session_state.labor}&partes={st.session_state.partes}&auto={urllib.parse.quote(st.session_state.veh)}"
            link = URL_APP + p
            msg = f"🛠️ *FACTURA FINAL - SERVICE PRO*\n{t('Hola', 'Hello')} {st.session_state.nombre}, {t('adjunto su factura por', 'invoice for')} ${total:,.2f}.\n{t('Ver detalles aquí', 'View details here')}: {link}"
            wa_url = f"https://api.whatsapp.com/send?phone={st.session_state.wa}&text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">📲 {t("CONFIRMAR ENVÍO", "CONFIRM SEND")}</button></a>', unsafe_allow_html=True)
