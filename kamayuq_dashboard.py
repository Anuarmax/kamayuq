import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Configuración de la página con estilo ejecutivo y diseño expandido responsivo
st.set_page_config(
    page_title="KAMAYUQ v2.0 - Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Avanzados contra Desbordamientos (100% Responsivo y Fluido)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Plus Jakarta Sans', sans-serif;
            box-sizing: border-box;
        }
        
        header[data-testid="stHeader"] {
            background-color: rgba(0,0,0,0) !important; 
            height: 0rem !important; 
        }
        
        .block-container {
            padding-top: 1rem !important;    
            padding-bottom: 2rem !important;  
            padding-left: 2vw !important;    
            padding-right: 2vw !important;
            max-width: 100% !important;        
            overflow-x: hidden !important;
        }
        
        .stApp {
            background-color: #F8FAFC;
        }
        
        /* Panel Lateral */
        [data-testid="stSidebar"] {
            background-color: #013C58;
            color: #FFFFFF;
        }
        
        [data-testid="stSidebar"] p {
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }
        
        /* Contenedores de Filtro */
        div[data-baseweb="select"] {
            background-color: #FFFFFF !important; 
            border-radius: 8px !important;
            border: 2px solid #A8E8F9 !important;
            max-width: 100% !important;
        }
        
        div[data-baseweb="select"]:hover {
            border-color: #F5A201 !important;
        }
        
        div[data-baseweb="select"] div {
            color: #013C58 !important;
            font-weight: 600 !important;
        }
        
        /* BANNER EN GRADIENTE FLUIDO RESPONSIVO */
        .main-header {
            background: linear-gradient(90deg, #013C58 0%, #013C58 80%, #00537A 93%, #F5A201 100%);
            padding: clamp(20px, 4vw, 35px) clamp(20px, 4vw, 40px); 
            border-radius: 16px;
            margin-bottom: 25px;
            box-shadow: 0 12px 25px -8px rgba(1, 60, 88, 0.18);
            border: 1px solid #013C58;
            display: flex;
            flex-direction: column;
            gap: 10px;
            width: 100%;
            max-width: 100%;
        }
        
        .brand-container {
            display: flex;
            align-items: center;
            gap: 15px; 
            flex-wrap: wrap; 
        }
        
        .inca-logo {
            width: clamp(40px, 6vw, 65px); 
            height: clamp(40px, 6vw, 65px);
            fill: #FFFFFF;
        }
        
        .main-header h1 {
            color: #FFFFFF !important; 
            margin: 0;
            font-size: clamp(1.8rem, 4vw, 3.2rem) !important; 
            font-weight: 800;
            letter-spacing: 0.02em;
            line-height: 1.1;
        }
        
        .main-header p {
            color: #A8E8F9 !important; 
            opacity: 0.95;
            margin: 0;
            font-size: clamp(0.85rem, 1.8vw, 1.15rem) !important;
            font-weight: 500;
        }
        
        /* Tarjetas Métricas con Control Anti-Desbordamiento */
        .metric-card {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: clamp(15px, 3vw, 20px);
            box-shadow: 0 4px 15px -3px rgba(1, 60, 88, 0.06);
            border-top: 4px solid #CBD5E1; 
            margin-bottom: 15px;
            width: 100%;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 110px;
            overflow: hidden;
        }
        
        .metric-title {
            font-size: clamp(0.7rem, 1.2vw, 0.8rem);
            color: #475569 !important; 
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }
        
        .metric-value {
            font-size: clamp(1.3rem, 2.2vw, 1.9rem) !important; 
            color: #013C58 !important; 
            font-weight: 800;
            line-height: 1.2;
            word-wrap: break-word;
            word-break: break-word;
            white-space: normal;
        }
        
        /* Badges Adaptables de Semáforos */
        .semaforo-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 3px 8px;
            border-radius: 20px;
            font-size: clamp(0.6rem, 1vw, 0.7rem);
            font-weight: 700;
            text-transform: uppercase;
            text-align: center;
        }
        .badge-rojo { background-color: #FEE2E2; color: #991B1B; }
        .badge-amarillo { background-color: #FEF3C7; color: #92400E; }
        .badge-verde { background-color: #D1FAE5; color: #065F46; }
        
        /* Contenedores de Gráficos Responsivos */
        .chart-container {
            background-color: #FFFFFF;
            border-radius: 14px;
            padding: clamp(15px, 2.5vw, 20px);
            box-shadow: 0 4px 20px -2px rgba(1, 60, 88, 0.05);
            border: 1px solid #E2E8F0;
            margin-bottom: 20px;
            width: 100%;
            max-width: 100%;
            overflow-x: auto;
        }
        
        .chart-title {
            font-size: clamp(0.85rem, 1.5vw, 1rem);
            color: #013C58;
            font-weight: 700;
            margin-bottom: 12px;
            border-left: 4px solid #F5A201;
            padding-left: 10px;
        }
        
        /* Ajustes de Pestañas y Elementos Nativos de Streamlit */
        .stTabs [data-baseweb="tab-list"] { 
            gap: 4px; 
            flex-wrap: wrap !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-weight: 700; 
            color: #1E293B !important; 
            padding: 8px 14px; 
            background-color: #E2E8F0; 
            border-radius: 6px 6px 0px 0px;
            font-size: clamp(0.8rem, 1.3vw, 0.95rem);
        }
        .stTabs [aria-selected="true"] { 
            background-color: #013C58 !important; 
            color: white !important; 
        }
        
        .stButton>button {
            background-color: #00537A !important; 
            color: white !important;
            border-radius: 8px !important; 
            font-weight: 600 !important; 
            width: 100%;
        }
        .stButton>button:hover { 
            background-color: #F5A201 !important; 
            color: #013C58 !important; 
        }
        
        /* Forzar tablas responsivas nativas */
        div[data-testid="stDataFrame"] {
            width: 100% !important;
            max-width: 100% !important;
            overflow-x: auto !important;
        }
    </style>
""", unsafe_allow_html=True)

# Listado oficial de columnas según la estructura de KAMAYUQ
COLUMNS_STRUCTURE = [
    'meta', 'cod_oficina', 'desc_oficina', 'ftefto', 'codigo_poi', 'correlativo_poi',
    'cadena_pptal', 'cod_prog', 'desc_prog', 'cod_proproy', 'desc_proproy',
    'cod_activ', 'desc_activ', 'cod_item', 'desc_item', 'cod_clasificador',
    'desc_clasificador', 'cod_unimed', 'desc_unimed', 'cantidad', 'pre_unitario',
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
    'setiembre', 'octubre', 'noviembre', 'diciembre', 'tot_item', 'ndetprior',
    'tipserv', 'obs_estado', 'tot_cantcons', 'cant_exclu', 'sol_exclu', 'num_req',
    'num_ccp', 'tipo_orden', 'ocanumero', 'num_siaf', 'ruc', 'razonsocial', 'importe'
]
MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'setiembre', 'octubre', 'noviembre', 'diciembre']

@st.cache_data
def generate_mock_data():
    np.random.seed(42)
    n_rows = 30
    oficinas = [('100', 'OFICINA DE TECNOLOGÍA DE LA INFORMACIÓN RESPALDO'), ('200', 'OFICINA DE ADMINISTRACIÓN Y FINANZAS RESPALDO')]
    data = []
    for i in range(n_rows):
        of = oficinas[np.random.choice(len(oficinas))]
        cant = np.random.randint(5, 15)
        pre = 100.0
        tot = cant * pre
        m_vals = np.zeros(12)
        m_vals[3] = tot
        row = {
            'meta': '001', 'cod_oficina': of[0], 'desc_oficina': of[1],
            'ftefto': '1-00', 'codigo_poi': 'POI-2026', 'correlativo_poi': 1, 'cadena_pptal': '2.3.1',
            'cod_prog': '9001', 'desc_prog': 'ACCIONES CENTRALES', 'cod_proproy': '3000001', 'desc_proproy': 'PRODUCTO',
            'cod_activ': '50001', 'desc_activ': 'GESTION', 'cod_item': f'I{i}', 'desc_item': 'RESPALDO POR DEFECTO',
            'cod_clasificador': '23.15', 'desc_clasificador': 'GASTOS', 'cod_unimed': 'UND', 'desc_unimed': 'UNIDAD',
            'cantidad': cant, 'pre_unitario': pre, 'enero': m_vals[0], 'febrero': m_vals[1], 'marzo': m_vals[2],
            'abril': m_vals[3], 'mayo': m_vals[4], 'junio': m_vals[5], 'julio': m_vals[6], 'agosto': m_vals[7],
            'setiembre': m_vals[8], 'octubre': m_vals[9], 'noviembre': m_vals[10], 'diciembre': m_vals[11],
            'tot_item': tot, 'ndetprior': 1, 'tipserv': 'BIEN', 'obs_estado': 'APROBADO', 
            'tot_cantcons': cant, 'cant_exclu': 0, 'sol_exclu': 'NO', 'num_req': 'REQ-100', 'num_ccp': 'CCP-100', 'tipo_orden': 'O/C',
            'ocanumero': 'ORD-100', 'num_siaf': '123456', 'ruc': '20100043841', 'razonsocial': 'EMPRESA DEMO S.A.', 'importe': tot
        }
        data.append(row)
    return pd.DataFrame(data)

# CABECERA INSTITUCIONAL RESPONSIVA
st.markdown("""
    <div class="main-header">
        <div class="brand-container">
            <svg class="inca-logo" viewBox="0 0 24 24">
                <path d="M12 2a10 10 0 0 0-10 10c0 4.15 2.5 7.73 6 9.3V21a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v.3c3.5-1.57 6-5.15 6-9.3A10 10 0 0 0 12 2zm0 2a2 2 0 1 1 0 4 2 2 0 0 1 0-4zm-5 8a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0zm5 7a4 4 0 0 1-4-4h8a4 4 0 0 1-4 4zm5-7a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/>
            </svg>
            <h1>KAMAYUQ v2.0</h1>
        </div>
        <p>Plataforma de Inteligencia de Negocios y Simulación Presupuestal Estratégica</p>
    </div>
""", unsafe_allow_html=True)

# CONFIGURACIÓN DEL PANEL LATERAL Y CARGA EN CASCO ESTRICTO
st.sidebar.title("Configuración y Carga")
uploaded_file = st.sidebar.file_uploader("Cargar Archivo de Datos (Excel/CSV)", type=['xlsx', 'csv'])

if uploaded_file is not None:
    try:
        df_raw = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    except:
        df_raw = generate_mock_data()
else:
    try:
        df_raw = pd.read_excel('datos_institucionales.xlsx')
    except:
        df_raw = generate_mock_data()

# Sanitizar columnas numéricas y de control estructural
for col in COLUMNS_STRUCTURE:
    if col not in df_raw.columns:
        df_raw[col] = 0 if col in MONTHS or col in ['cantidad', 'pre_unitario', 'importe', 'tot_item'] else ''

# Forzar conversión de importes a numéricos limpios a nivel global
df_raw['importe'] = pd.to_numeric(df_raw['importe'], errors='coerce').fillna(0)
df_raw['tot_item'] = pd.to_numeric(df_raw['tot_item'], errors='coerce').fillna(0)
for m in MONTHS:
    df_raw[m] = pd.to_numeric(df_raw[m], errors='coerce').fillna(0)

# ==========================================================
# FILTROS EN CASCADA INTELIGENTES (CORREGIDOS CONTRA NULOS)
# ==========================================================
st.sidebar.subheader("Filtros en Cascada (BI)")

oficinas_limpias = sorted([str(x) for x in df_raw['desc_oficina'].dropna().unique() if str(x).strip() != ''])
oficinas_disponibles = ["[ Todas las Oficinas ]"] + oficinas_limpias
selected_oficina = st.sidebar.selectbox("1. Filtrar por Oficina Orgánica", oficinas_disponibles)

df_step1 = df_raw.copy()
if selected_oficina != "[ Todas las Oficinas ]":
    df_step1 = df_step1[df_step1['desc_oficina'].astype(str) == selected_oficina]

programas_limpios = sorted([str(x) for x in df_step1['desc_prog'].dropna().unique() if str(x).strip() != ''])
programas_disponibles = ["[ Todos los Programas ]"] + programas_limpios
selected_programa = st.sidebar.selectbox("2. Programa Presupuestal (Filtrado)", programas_disponibles)

df_step2 = df_step1.copy()
if selected_programa != "[ Todos los Programas ]":
    df_step2 = df_step2[df_step2['desc_prog'].astype(str) == selected_programa]

metas_limpias = sorted([str(x) for x in df_step2['meta'].dropna().unique() if str(x).strip() != ''])
metas_disponibles = ["[ Todas las Metas ]"] + metas_limpias
selected_meta = st.sidebar.selectbox("3. Meta Presupuestaria (Filtrada)", metas_disponibles)

filtered_df = df_step2.copy()
if selected_meta != "[ Todas las Metas ]":
    filtered_df = filtered_df[filtered_df['meta'].astype(str) == selected_meta]

# ==========================================================
# SEMÁFOROS DE ALERTA TEMPRANA
# ==========================================================
monto_total_asignado = filtered_df['tot_item'].sum()
monto_total_ejecutado = filtered_df[MONTHS[:7]].sum().sum() # Hasta Julio de 2026
ratio_ejecucion = (monto_total_ejecutado / monto_total_asignado) if monto_total_asignado > 0 else 0

badge_html = ""
card_style = ""
if ratio_ejecucion > 0.85:
    badge_html = '<span class="semaforo-badge badge-rojo">⚠️ Gasto Acelerado</span>'
    card_style = "border-top: 4px solid #EF4444;"
elif ratio_ejecucion < 0.40:
    badge_html = '<span class="semaforo-badge badge-amarillo">📉 Subejecución</span>'
    card_style = "border-top: 4px solid #F5A201;"
else:
    badge_html = '<span class="semaforo-badge badge-verde">✅ Gasto Óptimo</span>'
    card_style = "border-top: 4px solid #10B981;"

# PANEL DE KPI CARDS EJECUTIVAS (Distribución Grid nativa responsiva)
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    st.markdown(f'<div class="metric-card" style="{card_style}"><div class="metric-title">Velocidad Ejecución</div><div class="metric-value">{ratio_ejecucion*100:.1f}%</div>{badge_html}</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card" style="border-top:4px solid #013C58;"><div class="metric-title">Techo Programado</div><div class="metric-value">S/. {monto_total_asignado:,.2f}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card" style="border-top:4px solid #00537A;"><div class="metric-title">Girado Ejecutado</div><div class="metric-value">S/. {monto_total_ejecutado:,.2f}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card" style="border-top:4px solid #FFBA42;"><div class="metric-title">SIAF Identificados</div><div class="metric-value">{filtered_df["num_siaf"].astype(str).dropna().nunique()}</div></div>', unsafe_allow_html=True)

# PESTAÑAS DE ANÁLISIS ESTRATÉGICO
tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ejecutivo v2.0", "🎛️ Planificador Simulador 'What-If'", "📋 Reporteador y Descargas"])

with tab1:
    st.subheader("Visualización del Gasto Institucional")
    g1, g2 = st.columns([1, 1])
    with g1:
        st.markdown('<div class="chart-container"><div class="chart-title">Distribución por Unidad Orgánica</div>', unsafe_allow_html=True)
        of_sum = filtered_df.groupby('desc_oficina')['importe'].sum().reset_index()
        fig_of = px.bar(of_sum, x='importe', y='desc_oficina', orientation='h', color_discrete_sequence=['#013C58'])
        fig_of.update_layout(autosize=True, height=280, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis={'title': None}, xaxis={'title': None})
        st.plotly_chart(fig_of, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    with g2:
        st.markdown('<div class="chart-container"><div class="chart-title">Cronograma y Curva de Ejecución</div>', unsafe_allow_html=True)
        m_sums = filtered_df[MONTHS].sum().reset_index()
        m_sums.columns = ['Mes', 'Monto']
        fig_m = go.Figure(go.Scatter(x=m_sums['Mes'], y=m_sums['Monto'], mode='lines+markers', line=dict(color='#F5A201', width=3), fill='tozeroy', fillcolor='rgba(245, 162, 1, 0.05)'))
        fig_m.update_layout(autosize=True, height=280, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_m, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# SIMULADOR ESTRATÉGICO "WHAT-IF"
# ==========================================================
with tab2:
    st.subheader("Sala de Simulación Presupuestaria y Austeridad")
    st.info("Modifique las barras de asignación táctica para medir el impacto de cambios presupuestales inmediatos.")
    
    col_s1, col_s2 = st.columns([1, 1])
    with col_s1:
        f_ti = st.slider("Variación TI (%)", -50, 50, 0, 5)
        f_adm = st.slider("Variación Administración (%)", -50, 50, 0, 5)
    with col_s2:
        f_ops = st.slider("Variación Operaciones (%)", -50, 50, 0, 5)
        f_plan = st.slider("Variación Planeamiento (%)", -50, 50, 0, 5)
        
    sim_df = filtered_df.copy()
    
    def aplicar_sim(row):
        oficina_str = str(row['desc_oficina']).upper()
        if 'TECNOLOGÍA' in oficina_str or 'TI' in oficina_str: return row['importe'] * (1 + f_ti / 100)
        if 'ADMINISTRACIÓN' in oficina_str: return row['importe'] * (1 + f_adm / 100)
        if 'OPERACIONES' in oficina_str: return row['importe'] * (1 + f_ops / 100)
        if 'PLANEAMIENTO' in oficina_str: return row['importe'] * (1 + f_plan / 100)
        return row['importe']
        
    sim_df['importe_simulado'] = sim_df.apply(aplicar_sim, axis=1)
    
    st.markdown('<div class="chart-container"><div class="chart-title">Impacto Técnico: Presupuesto Real vs Presupuesto Simulado</div>', unsafe_allow_html=True)
    comp_df = sim_df.groupby('desc_oficina')[['importe', 'importe_simulado']].sum().reset_index()
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(name='Presupuesto Original', x=comp_df['desc_oficina'], y=comp_df['importe'], marker_color='#013C58'))
    fig_comp.add_trace(go.Bar(name='Escenario Simulado', x=comp_df['desc_oficina'], y=comp_df['importe_simulado'], marker_color='#F5A201'))
    fig_comp.update_layout(barmode='group', autosize=True, height=280, margin=dict(l=10, r=10, t=15, b=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_comp, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.subheader("Extractor Avanzado de Reportes")
    cols_seleccionadas = st.multiselect("Columnas de Salida", options=COLUMNS_STRUCTURE, default=['meta', 'desc_oficina', 'desc_prog', 'importe', 'num_siaf'])
    if cols_seleccionadas:
        st.dataframe(filtered_df[cols_seleccionadas], use_container_width=True)
        c1, c2 = st.columns([1, 1])
        with c1:
            out = BytesIO()
            with pd.ExcelWriter(out, engine='openpyxl') as writer:
                filtered_df[cols_seleccionadas].to_excel(writer, index=False, sheet_name='KAMAYUQ_BI')
            st.download_button(label="📥 Descargar Excel Customizado", data=out.getvalue(), file_name='reporte_kamayuq_bi.xlsx')
        with c2:
            st.download_button(label="📄 Descargar CSV", data=filtered_df[cols_seleccionadas].to_csv(index=False).encode('utf-8'), file_name='reporte_kamayuq_bi.csv')

st.markdown("""
    <hr style="border:1px solid #CBD5E1">
    <div style="text-align: center; color: #1E293B; font-size: 0.85rem; font-weight: 600;">KAMAYUQ Business Intelligence Intel Core v2.0 • 2026</div>
""", unsafe_allow_html=True)
