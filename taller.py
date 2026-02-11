import streamlit as st
import urllib.parse

# 1. SISTEMA DE IDIOMAS Y ESTADO
if 'lang' not in st.session_state:
    st.session_state.lang = 'Español'
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'inspeccion_resultados' not in st.session_state:
    st.session_state.inspeccion_resultados = {}

def t(es, en):
    return es if st.session_state.lang == 'Español' else en

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

# 2. CONFIGURACIÓN PROFESIONAL
st.set_page_config(page_title="Service Pro Mobile - Full DVI", layout="wide", page_icon="🔧")

st.markdown(f"""
    <style>
    .main-header {{ background-color: #004a99; color: white; padding: 20px; text-align: center; border-radius: 10px; margin-bottom: 20px; }}
    .category-header {{ background-color: #004a99; color: white; padding: 10px; font-weight: bold; margin-top: 15px; border-radius: 5px; text-transform: uppercase; border-left: 8px solid #ff4b4b; }}
    .stButton>button {{ width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }}
    </style>
    """, unsafe_allow_html=True)

# Selector de idioma
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
    with col_s: 
        estado = st.select_slider(t("Estado", "Status"), options=["🚨", "⚠️", "✅"], value="✅", key=f"s_{key}", label_visibility="collapsed")
        # GUARDAR RESULTADO PARA EL REPORTE FINAL
        st.session_state.inspeccion_resultados[label] = estado
    with col_p:
        if st.checkbox(t("📸 Foto", "📸 Photo"), key=f"p_{key}"):
            st.camera_input(f"Captura {label}", key=f"cam_{key}", label_visibility="collapsed")

# --- VISTA DEL CLIENTE ---
if es_cliente:
    nombre_c = query_params.get("cliente", "Customer")
    labor_c = float(query_params.get("monto", 0))
    partes_c = float(query_params.get("partes", 0))
    auto_c = query_params.get("auto", "Vehicle")
    # Capturar hallazgos críticos del link
    hallazgos = query_params.get("obs", t("Verificado", "Verified"))
    
    subtotal = labor_c + partes_c
    tax = subtotal * 0.0715
    total = subtotal + tax

    st.markdown(f'<div class="main-header"><h1>{t("INSPECCIÓN Y FACTURA", "INSPECTION & INVOICE")}</h1></div>', unsafe_allow_html=True)
    
    st.subheader(t("🔍 Resultados de la Inspección", "🔍 Inspection Results"))
    st.info(f"{t('Notas del Técnico:', 'Technician Notes:')} {hallazgos}")
    
    st.markdown(f"""<div style="background-color:#f8f9fa; padding:20px; border-radius:10px; border:2px solid #004a99;">
    <h4>{t("Detalle de Cobro", "Billing Detail")}</h4>
    <p><b>{t("Labor", "Labor")}:</b> ${labor_c:,.2f} | <b>{t("Partes", "Parts")}:</b> ${partes_c:,.2f}</p>
    <p><b>Utah Tax (7.15%):</b> ${tax:,.2f}</p>
    <h2 style="color:#004a99;">TOTAL: ${total:,.2f}</h2></div>""", unsafe_allow_html=True)

    firma = st.text_input(t("Escriba su nombre para APROBAR", "Type name to APPROVE"))
    if st.button(t("✅ ACEPTAR Y FIRMAR", "✅ ACCEPT & SIGN")):
        if firma:
            msg = f"✅ *APPROVED*\n{firma} {t('autoriza el trabajo por', 'authorizes work for')} ${total:,.2f}."
            wa = f"https://api.whatsapp.com/send?phone={TU_TELEFONO}&text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{wa}" target="_blank"><button style="width:100%; background-color:#004a99; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">{t("Confirmar Firma", "Confirm Signature")} 📲</button></a>', unsafe_allow_html=True)

# --- VISTA DEL TÉCNICO ---
else:
    st.markdown(f'<div class="main-header"><h1>Service Pro Mobile - Workflow</h1></div>', unsafe_allow_html=True)
    
    # PASO 1: REGISTRO
    if st.session_state.step == 1:
        st.markdown(f'<div class="category-header">1. {t("Registro de Vehículo", "Vehicle Registry")}</div>', unsafe_allow_html=True)
        st.session_state.nombre = st.text_input(t("Nombre del Cliente", "Customer Name"), value=st.session_state.get('nombre', ''))
        st.session_state.wa = st.text_input(t("WhatsApp (1XXXXXXXXXX)", "WhatsApp"), value=st.session_state.get('wa', ''))
        st.session_state.veh = st.text_input(t("Vehículo", "Vehicle"), value=st.session_state.get('veh', ''))
        st.button(t("Ir a Inspección ➡️", "Go to Inspection ➡️"), on_click=next_step)

    # PASO 2: INSPECCIÓN (27 Puntos)
    elif st.session_state.step == 2:
        st.markdown(f'<div class="category-header">2. {t("Inspección de 27 Puntos", "27-Point Inspection")}</div>', unsafe_allow_html=True)
        fila_inspeccion("Aceite de Motor", "Engine Oil", "oil")
        fila_inspeccion("Frenos Delanteros", "Front Brakes", "f_br")
        fila_inspeccion("Llantas", "Tires", "tires")
        fila_inspeccion("Batería", "Battery", "batt")
        
        st.session_state.resumen_critico = st.text_area(t("Hallazgos Críticos", "Critical Findings"), placeholder=t("Ej: Frenos en 2mm, fuga de aceite...", "Ex: Brakes at 2mm, oil leak..."))
        
        c_nav1, c_nav2 = st.columns(2)
        c_nav1.button(t("⬅️ Registro", "⬅️ Registry"), on_click=prev_step)
        c_nav2.button(t("Ir a Facturación ➡️", "Go to Billing ➡️"), on_click=next_step)

    # PASO 3: FACTURACIÓN
    elif st.session_state.step == 3:
        st.markdown(f'<div class="category-header">3. {t("Factura Final", "Final Invoice")}</div>', unsafe_allow_html=True)
        st.session_state.labor = st.number_input(t("Mano de Obra", "Labor"), min_value=0.0)
        st.session_state.partes = st.number_input(t("Partes", "Parts"), min_value=0.0)
        
        total_p = (st.session_state.labor + st.session_state.partes) * 1.0715
        
        if st.button(f"🚀 {t('ENVIAR REPORTE COMPLETO', 'SEND FULL REPORT')}"):
            # INTEGRACIÓN DE INSPECCIÓN EN EL LINK
            obs = urllib.parse.quote(st.session_state.get('resumen_critico', 'N/A'))
            p = f"?cliente={urllib.parse.quote(st.session_state.nombre)}&monto={st.session_state.labor}&partes={st.session_state.partes}&auto={urllib.parse.quote(st.session_state.veh)}&obs={obs}"
            link = URL_APP + p
            
            msg = f"🛠️ *SERVICE PRO MOBILE*\n{t('Hola', 'Hello')} {st.session_state.nombre}, {t('adjunto el reporte y factura de su', 'here is the report and invoice for')} {st.session_state.veh}.\nTotal: ${total_p:.2f}.\n{t('Link', 'Link')}: {link}"
            wa_url = f"https://api.whatsapp.com/send?phone={st.session_state.wa}&text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold;">📲 {t("ENVIAR POR WHATSAPP", "SEND VIA WHATSAPP")}</button></a>', unsafe_allow_html=True)
