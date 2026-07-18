import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Configuración de la página con estilo ejecutivo y diseño expandido responsivo
st.set_page_config(
    page_title="KAMAYUQ - Sistema Reporteador",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Avanzados y Responsivos con Media Queries (Adaptable a PC, Tablet y Celular)
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
        
        /* Contenedor principal adaptable */
        .block-container {
            padding-top: 1rem !important;    
            padding-bottom: 2rem !important;  
            padding-left: 4vw !important;    
            padding-right: 4vw !important;
            max-width: 100% !important;        
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
        }
        
        div[data-baseweb="select"]:hover {
            border-color: #F5A201 !important;
        }
        
        div[data-baseweb="select"] div {
            color: #013C58 !important;
            font-weight: 600 !important;
        }
        
        div[data-baseweb="select"] svg {
            fill: #013C58 !important;
        }
        
        /* ==========================================================
           CABECERA RESPONSIVA: GRADIENTE DESDE AZUL (95%) A DORADO (5%)
           ========================================================== */
        .main-header {
            background: linear-gradient(90deg, #013C58 0%, #013C58 80%, #00537A 93%, #F5A201 100%);
            padding: 35px 40px; 
            border-radius: 16px;
            margin-bottom: 25px;
            box-shadow: 0 12px 25px -8px rgba(1, 60, 88, 0.18);
            border: 1px solid #013C58;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .brand-container {
            display: flex;
            align-items: center;
            gap: 15px; 
            flex-wrap: wrap; 
        }
        
        .inca-logo {
            width: clamp(45px, 7vw, 65px); 
            height: clamp(45px, 7vw, 65px);
            fill: #FFFFFF;
            filter: drop-shadow(0px 3px 5px rgba(1, 60, 88, 0.4));
        }
        
        .main-header h1 {
            color: #FFFFFF !important; 
            margin: 0;
            font-size: clamp(2.2rem, 5vw, 3.5rem) !important; 
            font-weight: 800;
            letter-spacing: 0.02em;
            text-shadow: 0 4px 8px rgba(1, 60, 88, 0.6); 
        }
        
        .main-header p {
            color: #A8E8F9 !important; 
            opacity: 0.95;
            margin: 0;
            font-size: clamp(0.95rem, 2vw, 1.15rem) !important;
            font-weight: 500;
            letter-spacing: 0.02em;
        }
        
        .deploy-label {
            position: absolute;
            top: 15px;
            right: 25px;
            color: #FFFFFF !important; 
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            opacity: 0.9;
        }
        
        /* ==========================================================
           TARJETAS DE MÉTRICAS (KPI) Y GRÁFICOS RESPONSIVOS
           ========================================================== */
        .metric-card {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px -3px rgba(1, 60, 88, 0.06);
            border-top: 4px solid #F5A201; 
            margin-bottom: 15px;
            width: 100%;
        }
        
        .metric-title {
            font-size: 0.8rem;
            color: #1E293B !important; 
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.05em;
        }
        
        .metric-value {
            font-size: clamp(1.6rem, 3vw, 2.1rem) !important; 
            color: #013C58 !important; 
            font-weight: 800;
            margin-top: 6px;
            word-wrap: break-word; 
        }
        
        .chart-container {
            background-color: #FFFFFF;
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 4px 20px -2px rgba(1, 60, 88, 0.05);
            border: 1px solid #E2E8F0;
            margin-bottom: 20px;
            width: 100%;
        }
        
        .chart-title {
            font-size: 1rem;
            color: #013C58;
            font-weight: 700;
            margin-bottom: 12px;
            border-left: 4px solid #F5A201;
            padding-left: 10px;
        }
        
        /* MEDIA QUERIES: Ajustes para pantallas móviles */
        @media (max-width: 768px) {
            .main-header {
                padding: 20px 25px;
            }
            .deploy-label {
                position: static; 
                margin-bottom: 5px;
            }
            .block-container {
                padding-left: 12px !important;
                padding-right: 12px !important;
            }
        }
        
        h2, h3 {
            color: #013C58 !important;
            font-weight: 700 !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-weight: 700;
            color: #1E293B !important; 
            padding: 10px 16px;
            background-color: #E2E8F0;
            border-radius: 6px 6px 0px 0px;
            margin-right: 2px;
        }

        .stTabs [aria-selected="true"] {
            background-color: #013C58 !important;
            color: white !important;
        }
        
        /* Botones de Descarga */
        .stButton>button {
            background-color: #00537A !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            border: none !important;
            width: 100%;
            padding: 0.6rem 1.2rem !important;
        }
        .stButton>button:hover {
            background-color: #F5A201 !important;
            color: #013C58 !important;
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
    n_rows = 150
    oficinas = [
        ('100', 'OFICINA DE TECNOLOGÍA DE LA INFORMACIÓN'),
        ('200', 'OFICINA DE ADMINISTRACIÓN Y FINANZAS'),
        ('300', 'OFICINA DE RECURSOS HUMANOS'),
        ('400', 'GERENCIA DE PLANEAMIENTO Y PRESUPUESTO'),
        ('500', 'DIRECCIÓN DE OPERACIONES')
    ]
    programas = [
        ('0001', 'PROGRAMA DE OPTIMIZACIÓN DE SERVICIOS'),
        ('0068', 'REDUCCIÓN DE VULNERABILIDAD Y ATENCIÓN DE EMERGENCIAS'),
        ('9001', 'ACCIONES CENTRALES')
    ]
    items = [
        ('I001', 'PAPEL BOND A4 80G', '01', 'MILLAR', 4.5),
        ('I002', 'SERVICIO DE INTERNET FIBRA ÓPTICA', '02', 'SERVICIO', 1500.0),
        ('I003', 'LAPTOP CORPORATIVA I7', '03', 'UNIDAD', 4200.0)
    ]
    proveedores = [('20100043841', 'INVERSIONES R & T HOYOS E.I.R.L.'), ('20554896321', 'LATAM AIRLINES PERU S.A.')]
    
    data = []
    for i in range(n_rows):
        of = oficinas[np.random.choice(len(oficinas))]
        prog = programas[np.random.choice(len(programas))]
        it = items[np.random.choice(len(items))]
        prov = proveedores[np.random.choice(len(proveedores))]
        cant = np.random.randint(1, 50)
        pre = it[4]
        tot = cant * pre
        m_vals = np.zeros(12)
        m_vals[np.random.choice(12, 3, replace=False)] = round(tot / 3, 2)
            
        row = {
            'meta': f'{np.random.randint(1, 25):03d}', 'cod_oficina': of[0], 'desc_oficina': of[1],
            'ftefto': '1-00', 'codigo_poi': 'POI-2026', 'correlativo_poi': 1, 'cadena_pptal': '2.3.1',
            'cod_prog': prog[0], 'desc_prog': prog[1], 'cod_proproy': '3000001', 'desc_proproy': 'PRODUCTO',
            'cod_activ': '50001', 'desc_activ': 'GESTION ADMINISTRATIVA', 'cod_item': it[0], 'desc_item': it[1],
            'cod_clasificador': '23.15', 'desc_clasificador': 'BIENES', 'cod_unimed': it[2], 'desc_unimed': it[3],
            'cantidad': cant, 'pre_unitario': pre, 'enero': m_vals[0], 'febrero': m_vals[1], 'marzo': m_vals[2],
            'abril': m_vals[3], 'mayo': m_vals[4], 'junio': m_vals[5], 'julio': m_vals[6], 'agosto': m_vals[7],
            'setiembre': m_vals[8], 'octubre': m_vals[9], 'noviembre': m_vals[10], 'diciembre': m_vals[11],
            'tot_item': tot, 'ndetprior': 1, 'tipserv': 'BIEN', 'obs_estado': np.random.choice(['APROBADO', 'EN REVISIÓN']), 
            'tot_cantcons': cant, 'cant_exclu': 0, 'sol_exclu': 'NO', 'num_req': 'REQ-100', 'num_ccp': 'CCP-100', 'tipo_orden': np.random.choice(['O/C', 'O/S']),
            'ocanumero': 'ORD-100', 'num_siaf': f'{np.random.randint(100000, 999999)}', 'ruc': prov[0], 'razonsocial': prov[1], 'importe': tot
        }
        data.append(row)
    return pd.DataFrame(data)

# CARGA DE DATOS Y SIDEBAR
st.sidebar.title("Configuración y Carga")
uploaded_file = st.sidebar.file_uploader("Cargar Archivo de Datos (Excel/CSV)", type=['xlsx', 'csv'])
df = generate_mock_data() # Inicializador robusto

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    except:
        pass

# Saneamiento de columnas
for col in COLUMNS_STRUCTURE:
    if col not in df.columns:
        df[col] = 0 if col in MONTHS or col in ['cantidad', 'pre_unitario', 'importe', 'tot_item'] else ''

# FILTROS AVANZADOS DE ALTA DIRECCIÓN
st.sidebar.subheader("Filtros Ejecutivos")
options_oficina = ["[ Todas las Oficinas ]"] + sorted(list(df['desc_oficina'].astype(str).unique()))
selected_oficina = st.sidebar.selectbox("Oficina / Unidad Orgánica", options=options_oficina)

options_programa = ["[ Todos los Programas ]"] + sorted(list(df['desc_prog'].astype(str).unique()))
selected_programa = st.sidebar.selectbox("Programa Presupuestal", options=options_programa)

options_meta = ["[ Todas las Metas ]"] + sorted(list(df['meta'].astype(str).unique()))
selected_meta = st.sidebar.selectbox("Meta Presupuestaria", options=options_meta)

options_estado = ["[ Todos los Estados ]"] + sorted(list(df['obs_estado'].astype(str).unique()))
selected_estado = st.sidebar.selectbox("Estado de Obligación", options=options_estado)

# Aplicación del Filtrado
filtered_df = df.copy()
if selected_oficina != "[ Todas las Oficinas ]":
    filtered_df = filtered_df[filtered_df['desc_oficina'].astype(str) == selected_oficina]
if selected_programa != "[ Todos los Programas ]":
    filtered_df = filtered_df[filtered_df['desc_prog'].astype(str) == selected_programa]
if selected_meta != "[ Todas las Metas ]":
    filtered_df = filtered_df[filtered_df['meta'].astype(str) == selected_meta]
if selected_estado != "[ Todos los Estados ]":
    filtered_df = filtered_df[filtered_df['obs_estado'].astype(str) == selected_estado]

# KPI CARDS RESPONSIVAS
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Importe Consolidado</div><div class="metric-value">S/. {filtered_df["importe"].sum():,.2f}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card" style="border-top-color:#00537A;"><div class="metric-title">Items Únicos</div><div class="metric-value">{filtered_df["cod_item"].nunique()}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Expedientes SIAF</div><div class="metric-value">{filtered_df["num_siaf"].nunique()}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card" style="border-top-color:#FFBA42;"><div class="metric-title">Oficinas</div><div class="metric-value">{filtered_df["cod_oficina"].nunique()}</div></div>', unsafe_allow_html=True)

# LAS 4 PESTAÑAS TRADICIONALES RECUPERADAS
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard Ejecutivo", "📅 Programación Mensual", "🏢 Oficinas y Metas", "📋 Reporteador Completo"])

with tab1:
    st.subheader("Análisis de Distribución Gasto Financiero")
    g1, g2 = st.columns([1, 1])
    with g1:
        st.markdown('<div class="chart-container"><div class="chart-title">Ejecución Financiera por Oficina</div>', unsafe_allow_html=True)
        of_data = filtered_df.groupby('desc_oficina')['importe'].sum().reset_index().sort_values(by='importe', ascending=True).head(8)
        fig_oficina = px.bar(of_data, x='importe', y='desc_oficina', orientation='h', color='importe', color_continuous_scale=['#A8E8F9', '#013C58'])
        fig_oficina.update_layout(autosize=True, height=320, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False, yaxis={'title': None}, xaxis={'title': None})
        st.plotly_chart(fig_oficina, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    with g2:
        st.markdown('<div class="chart-container"><div class="chart-title">Distribución por Tipo de Orden</div>', unsafe_allow_html=True)
        ord_data = filtered_df.groupby('tipo_orden')['importe'].sum().reset_index()
        fig_ordenes = px.pie(ord_data, values='importe', names='tipo_orden', hole=0.5, color_discrete_sequence=['#013C58', '#F5A201'])
        fig_ordenes.update_layout(autosize=True, height=320, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        st.plotly_chart(fig_ordenes, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Cronograma de Gasto Mensualizado")
    st.markdown('<div class="chart-container"><div class="chart-title">Evolución del Flujo Presupuestal Mensual</div>', unsafe_allow_html=True)
    monthly_sums = filtered_df[MONTHS].sum().reset_index()
    monthly_sums.columns = ['Mes', 'Monto']
    fig_monthly = go.Figure(go.Scatter(x=monthly_sums['Mes'], y=monthly_sums['Monto'], mode='lines+markers', line=dict(color='#00537A', width=3, shape='spline'), fill='tozeroy', fillcolor='rgba(168, 232, 249, 0.1)'))
    fig_monthly.update_layout(autosize=True, height=300, margin=dict(l=10, r=10, t=15, b=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    fig_monthly.update_yaxes(gridcolor='#E2E8F0', tickformat=",.0f")
    st.plotly_chart(fig_monthly, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.subheader("Estructura de Metas y Programas")
    st.markdown('<div class="chart-container"><div class="chart-title">Jerarquía de Distribución de Metas Críticas</div>', unsafe_allow_html=True)
    prog_meta = filtered_df.groupby(['desc_prog', 'meta'])['importe'].sum().reset_index().sort_values(by='importe', ascending=False).head(10)
    fig_bar_exec = px.bar(prog_meta, x='importe', y='meta', color='desc_prog', orientation='h', color_discrete_sequence=['#013C58', '#00537A', '#FFBA42'])
    fig_bar_exec.update_layout(autosize=True, height=350, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5), yaxis={'type': 'category'})
    st.plotly_chart(fig_bar_exec, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.subheader("Extractor y Consolidador de Información")
    visible_cols = st.multiselect("Columnas del Reporte Customizado", options=COLUMNS_STRUCTURE, default=['meta', 'desc_oficina', 'desc_item', 'cantidad', 'importe', 'num_siaf'])
    if visible_cols:
        st.dataframe(filtered_df[visible_cols], use_container_width=True)
        c_down1, c_down2 = st.columns(2)
        with c_down1:
            out_excel = BytesIO()
            with pd.ExcelWriter(out_excel, engine='openpyxl') as writer:
                filtered_df[visible_cols].to_excel(writer, index=False, sheet_name='KAMAYUQ')
            st.download_button(label="📥 Descargar Excel (.xlsx)", data=out_excel.getvalue(), file_name='reporte_kamayuq.xlsx')
        with c_down2:
            st.download_button(label="📄 Descargar CSV", data=filtered_df[visible_cols].to_csv(index=False).encode('utf-8'), file_name='reporte_kamayuq.csv')

st.markdown("""
    <hr style="border:1px solid #CBD5E1">
    <div style="text-align: center; color: #1E293B; font-size: 0.85rem; font-weight: 600; margin-bottom: 5px;">KAMAYUQ Reporteador Core v1.8 • Inteligencia de Negocios de Alta Dirección • 2026</div>
""", unsafe_allow_html=True)
