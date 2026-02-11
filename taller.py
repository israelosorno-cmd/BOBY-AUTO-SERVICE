import streamlit as st
import urllib.parse

# --- 1. CONFIGURACIÓN Y PERSISTENCIA ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'lang' not in st.session_state: st.session_state.lang = 'Español'
if 'data' not in st.session_state: st.session_state.data = {}

def t(es, en): return es if st.session_state.lang == 'Español' else en

st.set_page_config(page_title="Service Pro Mobile - SISTEMA INTEGRAL", layout="wide")

# --- 2. DISEÑO VISUAL ---
st.markdown(f"""
    <style>
    .main-header {{ background-color: #004a99; color: white; padding: 25px; text-align: center; border-radius: 15px; margin-bottom: 20px; }}
    .category-header {{ background-color: #004a99; color: white; padding: 12px; font-weight: bold; margin-top: 25px; border-radius: 8px; text-transform: uppercase; border-left: 10px solid #ff4b4b; }}
    .invoice-box {{ background-color: #ffffff; border: 3px solid #004a99; padding: 30px; border-radius: 15px; box-shadow: 5px 5px 15px rgba(0,0,0,0.1); }}
    .stButton>button {{ width: 100%; border-radius: 12px; font-weight: bold; height: 4em; background-color: #004a99; color: white; }}
    </style>
    """, unsafe_allow_html=True)

# Selector de idioma global
c_head, c_lang = st.columns([5, 1])
with c_lang: st.selectbox("🌐 Language", ["Español", "English"], key='lang', label_visibility="collapsed")

URL_APP = "https://service-pro-mobile-dvi.streamlit.app"
TU_TELEFONO = "17134018085"
query_params = st.query_params

# --- 3. MÓDULO DE INSPECCIÓN (27 PUNTOS COMPLETO) ---
def seccion_inspeccion(titulo_es, titulo_en, puntos):
    st.markdown(f'<div class="category-header">{t(titulo_es, titulo_en)}</div>', unsafe_allow_html=True)
    for p_es, p_en, key in puntos:
        col_t, col_s, col_p = st.columns([3, 2, 2])
        with col_t: st.write(f"**{t(p_es, p_en)}**")
        with col_s: 
            res = st.select_slider(t("Estado", "Status"), options=["🚨", "⚠️", "✅"], value="✅", key=f"s_{key}")
            st.session_state.data[f"status_{key}"] = res
        with col_p:
            if st.checkbox(t("📸 Foto", "📸 Photo"), key=f"p_{key}"):
                st.camera_input(t("Capturar", "Capture"), key=f"cam_{key}")

# --- 4. VISTA DEL CLIENTE (FACTURA Y RESULTADOS) ---
if "cliente" in query_params:
    st.markdown(f'<div class="main-header"><h1>{t("REPORTE Y FACTURA", "REPORT & INVOICE")}</h1></div>', unsafe_allow_html=True)
    n = query_params.get("cliente")
    l = float(query_params.get("monto", 0))
    p = float(query_params.get("partes", 0))
    v = query_params.get("auto")
    tax = (l + p) * 0.0715
    total = l + p + tax

    st.markdown(f"""
    <div class="invoice-box">
        <h2 style="color:#004a99;">{t("Factura Final", "Final Invoice")}</h2>
        <p><b>{t("Vehículo", "Vehicle")}:</b> {v}</p>
        <hr>
        <p>{t("Mano de Obra", "Labor")}: ${l:,.2f}</p>
        <p>{t("Partes/Materiales", "Parts")}: ${p:,.2f}</p>
        <p>Tax (7.15%): ${tax:,.2f}</p>
        <h1 style="color:#004a99;">TOTAL: ${total:,.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

    firma = st.text_input(t("Firme aquí (Nombre completo)", "Sign here (Full name)"))
    if st.button(t("✅ APROBAR TRABAJO", "✅ APPROVE WORK")):
        if firma:
            msg = f"✅ *APROBADO*\nCliente: {firma}\nVehículo: {v}\nTotal: ${total:,.2f}"
            st.markdown(f'<a href="https://api.whatsapp.com/send?phone={TU_TELEFONO}&text={urllib.parse.quote(msg)}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">Confirmar en WhatsApp 📲</button></a>', unsafe_allow_html=True)

# --- 5. VISTA DEL TÉCNICO (TODOS LOS MÓDULOS) ---
else:
    st.markdown(f'<div class="main-header"><h1>Service Pro Mobile - Panel Maestro</h1></div>', unsafe_allow_html=True)
    
    # PASO 1: REGISTRO
    if st.session_state.step == 1:
        st.markdown('<div class="category-header">Módulo 1: Registro de Entrada</div>', unsafe_allow_html=True)
        st.session_state.data['nom'] = st.text_input(t("Nombre del Cliente", "Customer"), value=st.session_state.data.get('nom', ''))
        st.session_state.data['wa'] = st.text_input(t("WhatsApp (Ej: 1713...)", "WhatsApp"), value=st.session_state.data.get('wa', ''))
        st.session_state.data['veh'] = st.text_input(t("Vehículo", "Vehicle"), value=st.session_state.data.get('veh', ''))
        st.session_state.data['mil'] = st.text_input(t("Millaje", "Odometer"), value=st.session_state.data.get('mil', ''))
        st.button(t("Ir a Inspección ➡️", "Go to Inspection ➡️"), on_click=lambda: st.session_state.update(step=2))

    # PASO 2: INSPECCIÓN COMPLETA
    elif st.session_state.step == 2:
        seccion_inspeccion("Motor y Líquidos", "Engine & Fluids", [
            ("Aceite de Motor", "Engine Oil", "oil"),
            ("Filtro de Aire", "Air Filter", "airf"),
            ("Anticongelante", "Coolant", "cool"),
            ("Líquido de Frenos", "Brake Fluid", "brf")
        ])
        seccion_inspeccion("Frenos y Llantas", "Brakes & Tires", [
            ("Pastillas Delanteras", "Front Pads", "fpads"),
            ("Pastillas Traseras", "Rear Pads", "rpads"),
            ("Presión de Llantas", "Tire Pressure", "tpress")
        ])
        st.button(t("Ir a Facturación ➡️", "Go to Billing ➡️"), on_click=lambda: st.session_state.update(step=3))

    # PASO 3: FACTURACIÓN Y ENVÍO
    elif st.session_state.step == 3:
        st.markdown('<div class="category-header">Módulo 3: Cotización y Factura</div>', unsafe_allow_html=True)
        l = st.number_input(t("Mano de Obra", "Labor"), value=st.session_state.data.get('lab', 0.0))
        p = st.number_input(t("Partes", "Parts"), value=st.session_state.data.get('par', 0.0))
        st.session_state.data['lab'], st.session_state.data['par'] = l, p
        
        total = (l + p) * 1.0715
        if st.button(t("🚀 GENERAR Y ENVIAR FACTURA", "🚀 GENERATE & SEND")):
            d = st.session_state.data
            params = f"?cliente={urllib.parse.quote(d['nom'])}&monto={l}&partes={p}&auto={urllib.parse.quote(d['veh'])}"
            msg = f"🛠️ *SERVICE PRO*\nHola {d['nom']}, factura de su {d['veh']}.\nTotal: ${total:.2f}\nLink: {URL_APP+params}"
            st.markdown(f'<a href="https://api.whatsapp.com/send?phone={d["wa"]}&text={urllib.parse.quote(msg)}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">📲 CONFIRMAR ENVÍO</button></a>', unsafe_allow_html=True)
