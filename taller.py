import streamlit as st
import urllib.parse

# --- 1. ESTADO DE LA SESIÓN (PARA QUE NADA SE BORRE) ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'lang' not in st.session_state: st.session_state.lang = 'Español'
if 'data' not in st.session_state: st.session_state.data = {}

def t(es, en): return es if st.session_state.lang == 'Español' else en

# --- 2. CONFIGURACIÓN Y ESTILOS ---
st.set_page_config(page_title="Service Pro Mobile - Sistema Integral", layout="wide")
st.markdown(f"""
    <style>
    .main-header {{ background-color: #004a99; color: white; padding: 20px; text-align: center; border-radius: 10px; margin-bottom: 20px; }}
    .category-header {{ background-color: #004a99; color: white; padding: 10px; font-weight: bold; margin-top: 20px; border-radius: 5px; text-transform: uppercase; border-left: 8px solid #ff4b4b; }}
    .stButton>button {{ width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }}
    </style>
    """, unsafe_allow_html=True)

# Idioma superior derecha
c_head, c_lang = st.columns([5, 1])
with c_lang: st.selectbox("🌐", ["Español", "English"], key='lang', label_visibility="collapsed")

# VARIABLES MAESTRAS
URL_APP = "https://service-pro-mobile-dvi.streamlit.app"
TU_TELEFONO = "17134018085"
query_params = st.query_params

# --- 3. FUNCIONES DE AYUDA ---
def fila_inspeccion(label_es, label_en, key):
    label = t(label_es, label_en)
    st.write(f"**{label}**")
    col_s, col_p = st.columns([1, 1])
    estado = col_s.select_slider(t("Estado", "Status"), options=["🚨", "⚠️", "✅"], value="✅", key=f"s_{key}")
    if col_p.checkbox(t("📸 Foto", "📸 Photo"), key=f"p_{key}"):
        st.camera_input(t("Captura", "Capture"), key=f"cam_{key}")
    st.session_state.data[key] = estado

# --- VISTA DEL CLIENTE ---
if "cliente" in query_params:
    st.markdown(f'<div class="main-header"><h1>{t("REPORTE Y FACTURA DIGITAL", "DIGITAL REPORT & INVOICE")}</h1></div>', unsafe_allow_html=True)
    nombre_c = query_params.get("cliente", "Customer")
    labor_c = float(query_params.get("monto", 0))
    partes_c = float(query_params.get("partes", 0))
    sub = labor_c + partes_c
    tax = sub * 0.0715
    total = sub + tax

    st.write(f"### {t('Hola', 'Hello')} {nombre_c}, {t('este es el resumen de su servicio:', 'here is your service summary:')}")
    st.info(f"**{t('Notas del Técnico:', 'Technician Notes:')}** {query_params.get('obs', 'N/A')}")
    
    st.markdown(f"""<div style="background-color:white; border:2px solid #004a99; padding:20px; border-radius:10px;">
    <h3>TOTAL: ${total:,.2f}</h3><p>Labor: ${labor_c:,.2f} | Parts: ${partes_c:,.2f} | Tax (7.15%): ${tax:,.2f}</p></div>""", unsafe_allow_html=True)

    firma = st.text_input(t("Escriba su nombre para FIRMAR", "Type name to SIGN"))
    if st.button(t("✅ APROBAR", "✅ APPROVE")):
        if firma:
            msg = f"✅ *APPROVED*\n{firma} autoriza trabajo por ${total:,.2f}."
            st.markdown(f'<a href="https://api.whatsapp.com/send?phone={TU_TELEFONO}&text={urllib.parse.quote(msg)}" target="_blank"><button style="width:100%; background-color:#004a99; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">Confirmar Firma 📲</button></a>', unsafe_allow_html=True)

# --- VISTA DEL TÉCNICO (MODULOS SEPARADOS POR PASOS) ---
else:
    st.markdown(f'<div class="main-header"><h1>Service Pro Mobile - Panel</h1></div>', unsafe_allow_html=True)
    
    if st.session_state.step == 1: # REGISTRO
        st.markdown(f'<div class="category-header">1. {t("Registro", "Registry")}</div>', unsafe_allow_html=True)
        st.session_state.data['nom'] = st.text_input(t("Cliente", "Customer"), value=st.session_state.data.get('nom', ''))
        st.session_state.data['wa'] = st.text_input(t("WhatsApp (1XXXXXXXXXX)", "WhatsApp"), value=st.session_state.data.get('wa', ''))
        st.session_state.data['veh'] = st.text_input(t("Vehículo", "Vehicle"), value=st.session_state.data.get('veh', ''))
        st.button(t("Siguiente: Inspección ➡️", "Next: Inspection ➡️"), on_click=lambda: st.session_state.update(step=2))

    elif st.session_state.step == 2: # INSPECCIÓN 27 PTS
        st.markdown(f'<div class="category-header">2. {t("Inspección 27 Puntos", "27-Point Inspection")}</div>', unsafe_allow_html=True)
        fila_inspeccion("Aceite de Motor", "Engine Oil", "oil")
        fila_inspeccion("Frenos Delanteros", "Front Brakes", "f_br")
        fila_inspeccion("Presión de Llantas", "Tire Pressure", "tires")
        st.session_state.data['obs'] = st.text_area(t("Observaciones", "Observations"), value=st.session_state.data.get('obs', ''))
        
        c_p, c_n = st.columns(2)
        c_p.button(t("⬅️ Registro", "⬅️ Registry"), on_click=lambda: st.session_state.update(step=1))
        c_n.button(t("Siguiente: Cotización ➡️", "Next: Quote ➡️"), on_click=lambda: st.session_state.update(step=3))

    elif st.session_state.step == 3: # COTIZACIÓN Y FACTURA
        st.markdown(f'<div class="category-header">3. {t("Facturación", "Billing")}</div>', unsafe_allow_html=True)
        st.session_state.data['lab'] = st.number_input(t("Mano de Obra", "Labor"), value=st.session_state.data.get('lab', 0.0))
        st.session_state.data['par'] = st.number_input(t("Partes", "Parts"), value=st.session_state.data.get('par', 0.0))
        
        tot = (st.session_state.data['lab'] + st.session_state.data['par']) * 1.0715
        st.write(f"### Total (inc. Tax 7.15%): ${tot:,.2f}")

        c_p2, c_n2 = st.columns(2)
        c_p2.button(t("⬅️ Inspección", "⬅️ Inspection"), on_click=lambda: st.session_state.update(step=2))
        if c_n2.button(t("🚀 ENVIAR TODO AL CLIENTE", "🚀 SEND ALL TO CUSTOMER")):
            d = st.session_state.data
            p = f"?cliente={urllib.parse.quote(d['nom'])}&monto={d['lab']}&partes={d['par']}&auto={urllib.parse.quote(d['veh'])}&obs={urllib.parse.quote(d['obs'])}"
            msg = f"🛠️ *SERVICE PRO*\nHola {d['nom']}, adjunto reporte y factura de su {d['veh']}. Total: ${tot:,.2f}. Link: {URL_APP+p}"
            st.markdown(f'<a href="https://api.whatsapp.com/send?phone={d["wa"]}&text={urllib.parse.quote(msg)}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">📲 CONFIRMAR ENVÍO</button></a>', unsafe_allow_html=True)
