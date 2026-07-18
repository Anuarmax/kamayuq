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
            padding-left: 5vw !important;    
            padding-right: 5vw !important;
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
        
        /* ==========================================================
           CABECERA RESPONSIVA: GRADIENTE DESDE AZUL (95%) A DORADO (5%)
           ========================================================== */
        .main-header {
            background: linear-gradient(90deg, #013C58 0%, #013C58 85%, #00537A 95%, #F5A201 100%);
            padding: 30px 40px; 
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
            flex-wrap: wrap; /* Permite que el logo y título se acomoden en pantallas pequeñas */
        }
        
        .inca-logo {
            width: clamp(45px, 7vw, 65px); /* Ancho dinámico según la pantalla */
            height: clamp(45px, 7vw, 65px);
            fill: #FFFFFF;
            filter: drop-shadow(0px 3px 5px rgba(1, 60, 88, 0.4));
        }
        
        .main-header h1 {
            color: #FFFFFF !important; 
            margin: 0;
            font-size: clamp(2rem, 5vw, 3.5rem) !important; /* Fuente fluida protagonista */
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
            font-size: clamp(1.5rem, 3vw, 2.1rem) !important; /* Valor numérico auto-ajustable */
            color: #013C58 !important; 
            font-weight: 800;
            margin-top: 6px;
            word-wrap: break-word; /* Evita que números grandes rompan la tarjeta en celulares */
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
        
        /* MEDIA QUERIES: Ajustes específicos para pantallas de celulares */
        @media (max-width: 768px) {
            .main-header {
                padding: 20px 25px;
                background: #013C58; /* Fondo sólido en celular para mejor consistencia visual */
            }
            .deploy-label {
                position: static; /* Baja al flujo normal en pantallas chicas */
                margin-bottom: 5px;
            }
            .block-container {
                padding-left: 15px !important;
                padding-right: 15px !important;
            }
        }
        
        h2, h3 {
            color: #013C58 !important;
            font-weight: 700 !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-weight: 700;
            color: #1E293B !important; 
            padding: 8px 14px;
        }

        .stTabs [aria-selected="true"] {
            background-color: #013C58 !important;
            color: white !important;
            border-radius: 4px;
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
    oficinas = [('100', 'OFICINA DE TECNOLOGÍA DE LA INFORMACIÓN'), ('200', 'OFICINA DE ADMINISTRACIÓN Y FINANZAS'), ('300', 'OFICINA DE RECURSOS HUMANOS')]
    programas = [('0001', 'PROGRAMA DE OPTIMIZACIÓN DE SERVICIOS'), ('0068', 'REDUCCIÓN DE VULNERABILIDAD')]
    items = [('I001', 'PAPEL BOND A4 80G', '01', 'MILLAR', 4.5), ('I002', 'SERVICIO DE INTERNET FIBRA ÓPTICA', '02', 'SERVICIO', 1500.0)]
    proveedores = [('20100043841', 'INVERSIONES R & T HOYOS E.I.R.L.')]
    
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
        m_vals[np.random.choice(12)] = tot
            
        row = {
            'meta': f'{np.random.randint(1, 25):03d}', 'cod_oficina': of[0], 'desc_oficina': of[1],
            'ftefto': '1-00', 'codigo_poi': 'POI-2026', 'correlativo_poi': 1, 'cadena_pptal': '2.3.1',
            'cod_prog': prog[0], 'desc_prog': prog[1], 'cod_proproy': '3000001', 'desc_proproy': 'PRODUCTO',
            'cod_activ': '50001', 'desc_activ': 'GESTION ADMINISTRATIVA', 'cod_item': it[0], 'desc_item': it[1],
            'cod_clasificador': '23.15', 'desc_clasificador': 'BIENES', 'cod_unimed': it[2], 'desc_unimed': it[3],
            'cantidad': cant, 'pre_unitario': pre, 'enero': m_vals[0], 'febrero': m_vals[1], 'marzo': m_vals[2],
            'abril': m_vals[3], 'mayo': m_vals[4], 'junio': m_vals[5], 'julio': m_vals[6], 'agosto': m_vals[7],
            'setiembre': m_vals[8], 'octubre': m_vals[9], 'noviembre': m_vals[10], 'diciembre': m_vals[11],
            'tot_item': tot, 'ndetprior': 1, 'tipserv': 'BIEN', 'obs_estado': 'APROBADO', 'tot_cantcons': cant,
            'cant_exclu': 0, 'sol_exclu': 'NO', 'num_req': 'REQ-100', 'num_ccp': 'CCP-100', 'tipo_orden': 'O/C',
            'ocanumero': 'ORD-100', 'num_siaf': '100000', 'ruc': prov[0], 'razonsocial': prov[1], 'importe': tot
        }
        data.append(row)
    return pd.DataFrame(data)

# HEADER PRINCIPAL
st.markdown("""
    <div class="main-header">
        <div class="deploy-label">Deploy</div>
        <div class="brand-container">
            <svg class="inca-logo" viewBox="0 0 24 24">
                <path d="M12 2a10 10 0 0 0-10 10c0 4.15 2.5 7.73 6 9.3V21a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v.3c3.5-1.57 6-5.15 6-9.3A10 10 0 0 0 12 2zm0 2a2 2 0 1 1 0 4 2 2 0 0 1 0-4zm-5 8a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0zm5 7a4 4 0 0 1-4-4h8a4 4 0 0 1-4 4zm5-7a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/>
                <path d="M12 1a1 1 0 0 1 1 1v1a1 1 0 0 1-2 0V21a1 1 0 0 1 1-1zm11 11a1 1 0 0 1-1 1h-1a1 1 0 0 1 0-2h1a1 1 0 0 1 1 1zM2 12a1 1 0 0 1 1-1h1a1 1 0 0 1 0 2H3a1 1 0 0 1-1-1z"/>
            </svg>
            <h1>KAMAYUQ</h1>
        </div>
        <p>Extracción, Consolidación y Visualización de Información Presupuestal y Logística</p>
    </div>
""", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title("Configuración")
uploaded_file = st.sidebar.file_uploader("Cargar Archivo (Excel/CSV)", type=['xlsx', 'csv'])
df = generate_mock_data() if uploaded_file is not None else generate_mock_data()

# FILTROS
st.sidebar.subheader("Filtros")
selected_oficina = st.sidebar.selectbox("Oficina", options=["[ Todas ]"] + sorted(list(df['desc_oficina'].unique())))
filtered_df = df if selected_oficina == "[ Todas ]" else df[df['desc_oficina'] == selected_oficina]

# SECCIÓN 1: KPI CARDS RESPONSIVAS
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Total Consolidado</div><div class="metric-value">S/. {filtered_df["importe"].sum():,.2f}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Items Únicos</div><div class="metric-value">{filtered_df["cod_item"].nunique()}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Expedientes SIAF</div><div class="metric-value">{filtered_df["num_siaf"].nunique()}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Oficinas</div><div class="metric-value">{filtered_df["cod_oficina"].nunique()}</div></div>', unsafe_allow_html=True)

# SECCIÓN 2: PESTAÑAS
tab1, tab2 = st.tabs(["📊 Dashboard", "📋 Reporteador"])

with tab1:
    g1, g2 = st.columns([1, 1]) # En PC divide 50/50, en móvil se apila solo
    with g1:
        st.markdown('<div class="chart-container"><div class="chart-title">Gasto por Oficina</div>', unsafe_allow_html=True)
        fig = px.bar(filtered_df.groupby('desc_oficina')['importe'].sum().reset_index(), x='importe', y='desc_oficina', orientation='h', color_discrete_sequence=['#013C58'])
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=300, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    with g2:
        st.markdown('<div class="chart-container"><div class="chart-title">Órdenes</div>', unsafe_allow_html=True)
        fig2 = px.pie(filtered_df.groupby('tipo_orden')['importe'].sum().reset_index(), values='importe', names='tipo_orden', hole=0.5, color_discrete_sequence=['#013C58', '#F5A201'])
        fig2.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=300, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.dataframe(filtered_df[['meta', 'desc_oficina', 'desc_item', 'importe']], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
    <hr style="border:1px solid #CBD5E1">
    <div style="text-align: center; color: #1E293B; font-size: 0.85rem; font-weight: 600;">KAMAYUQ Core v1.7 • 2026</div>
""", unsafe_allow_html=True)
