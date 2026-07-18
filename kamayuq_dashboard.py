import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Configuración de la página con estilo ejecutivo
st.set_page_config(
    page_title="KAMAYUQ - Sistema Reporteador",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS de Alta Dirección con el BANNER CORREGIDO (AZUL 95% - DORADO 5%)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        /* Ajuste de barra superior nativa para alinearse al deploy del banner */
        header[data-testid="stHeader"] {
            background-color: rgba(0,0,0,0) !important; 
            height: 0rem !important; 
        }
        
        /* Eliminación de espacios en blanco en el contenedor principal */
        .block-container {
            padding-top: 1rem !important;    
            padding-bottom: 2rem !important;  
            padding-left: 3rem !important;    
            padding-right: 3rem !important;
            max-width: 98% !important;        
        }
        
        /* Fondo general de la aplicación */
        .stApp {
            background-color: #F8FAFC;
        }
        
        /* Panel Lateral (Sidebar) */
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
            transition: all 0.2s ease;
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
        
        /* Tarjetas de Métricas (KPI Cards) */
        .metric-card {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 22px;
            box-shadow: 0 4px 15px -3px rgba(1, 60, 88, 0.06);
            border-top: 4px solid #F5A201; 
            margin-bottom: 15px;
        }
        
        .metric-title {
            font-size: 0.85rem;
            color: #1E293B !important; 
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.07em;
        }
        
        .metric-value {
            font-size: 2.1rem;
            color: #013C58 !important; 
            font-weight: 800;
            margin-top: 8px;
        }
        
        /* Tarjetas para Gráficos Premium */
        .chart-container {
            background-color: #FFFFFF;
            border-radius: 14px;
            padding: 24px;
            box-shadow: 0 4px 20px -2px rgba(1, 60, 88, 0.05);
            border: 1px solid #E2E8F0;
            margin-bottom: 25px;
        }
        
        .chart-title {
            font-size: 1.1rem;
            color: #013C58;
            font-weight: 700;
            margin-bottom: 15px;
            border-left: 4px solid #F5A201;
            padding-left: 10px;
        }

        /* ==========================================================
           GRADIENTE CORREGIDO: DESDE AZUL (95%) HASTA DORADO (5%)
           ========================================================== */
        .main-header {
            /* El azul domina de forma masiva desde el inicio hasta el 95% del banner, dejando el 5% final para el destello dorado */
            background: linear-gradient(90deg, 
                #013C58 0%, 
                #013C58 80%, 
                #00537A 93%, 
                #F5A201 100%
            );
            padding: 45px 50px; 
            border-radius: 16px;
            margin-bottom: 30px;
            box-shadow: 0 12px 25px -8px rgba(1, 60, 88, 0.18);
            border: 1px solid #013C58;
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; height: 100%;
            background: linear-gradient(rgba(255,255,255,0.04), rgba(255,255,255,0));
            pointer-events: none;
        }
        
        .brand-container {
            display: flex;
            align-items: center;
            gap: 18px; 
        }
        
        .inca-logo {
            width: 65px;
            height: 65px;
            fill: #FFFFFF;
            filter: drop-shadow(0px 3px 5px rgba(1, 60, 88, 0.4));
        }
        
        .main-header h1 {
            color: #FFFFFF !important; 
            margin: 0;
            font-size: 3.5rem; 
            font-weight: 800;
            letter-spacing: 0.02em;
            text-shadow: 0 4px 8px rgba(1, 60, 88, 0.6); 
        }
        
        .main-header p {
            color: #A8E8F9 !important; /* Celeste claro de alto contraste sobre el azul masivo */
            opacity: 0.95;
            margin: 15px 0 0 0;
            font-size: 1.15rem;
            font-weight: 500;
            letter-spacing: 0.02em;
            text-shadow: 0 2px 4px rgba(1, 60, 88, 0.4);
        }
        
        .deploy-label {
            position: absolute;
            top: 15px;
            right: 25px;
            color: #FFFFFF !important; /* Blanco para garantizar lectura en la zona oscura/dorada */
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            opacity: 0.9;
        }
        /* ========================================================== */
        
        h2, h3 {
            color: #013C58 !important;
            font-weight: 700 !important;
        }
        
        /* Pestañas */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: #E2E8F0;
            border-radius: 6px 6px 0px 0px;
            padding: 10px 20px;
            font-weight: 700;
            color: #1E293B !important; 
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
            padding: 0.6rem 1.2rem !important;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #F5A201 !important;
            color: #013C58 !important;
            box-shadow: 0 4px 14px rgba(245, 162, 1, 0.3) !important;
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
        ('0090', 'LOGROS DE APRENDIZAJE DE ESTUDIANTES DE LA EDUCACIÓN BÁSICA'),
        ('9001', 'ACCIONES CENTRALES'),
        ('9002', 'ASIGNACIONES PRESUPUESTARIAS QUE NO RESULTAN EN PRODUCTOS')
    ]
    
    items = [
        ('I001', 'PAPEL BOND A4 80G', '01', 'MILLAR', 4.5),
        ('I002', 'SERVICIO DE INTERNET FIBRA ÓPTICA', '02', 'SERVICIO', 1500.0),
        ('I003', 'LAPTOP CORPORATIVA I7', '03', 'UNIDAD', 4200.0),
        ('I004', 'SERVICIO DE MANTENIMIENTO PREVENTIVO', '02', 'SERVICIO', 800.0),
        ('I005', 'TONER NEGRO COMPATIBLE', '01', 'UNIDAD', 250.0)
    ]
    
    proveedores = [
        ('20100043841', 'INVERSIONES R & T HOYOS E.I.R.L.'),
        ('20554896321', 'LATAM AIRLINES PERU S.A.'),
        ('20448975123', 'PROXUS SECURITY S.A.C.'),
        ('20331598462', 'LUZ DEL SUR S.A.A.'),
        ('20123456789', 'COMPUTER LVC SYSTEM E.I.R.L.')
    ]
    
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
        n_meses_activos = np.random.randint(1, 5)
        meses_elegidos = np.random.choice(12, n_meses_activos, replace=False)
        for m in meses_elegidos:
            m_vals[m] = round(tot / n_meses_activos, 2)
            
        row = {
            'meta': f'{np.random.randint(1, 25):03d}',
            'cod_oficina': of[0],
            'desc_oficina': of[1],
            'ftefto': np.random.choice(['1-00', '2-09', '5-18']),
            'codigo_poi': f'POI-2026-{np.random.randint(1000, 9999)}',
            'correlativo_poi': np.random.randint(1, 100),
            'cadena_pptal': f'2.3.1 5.1.{np.random.randint(1,9)}',
            'cod_prog': prog[0],
            'desc_prog': prog[1],
            'cod_proproy': '3000001' if prog[0].startswith('0') else '9999999',
            'desc_proproy': 'PRODUCTO' if prog[0].startswith('0') else 'SIN PRODUCTO',
            'cod_activ': f'5000{np.random.randint(100, 999)}',
            'desc_activ': 'GESTION ADMINISTRATIVA' if np.random.rand() > 0.5 else 'PRESTACION DE SERVICIOS TÉCNICOS',
            'cod_item': it[0],
            'desc_item': it[1],
            'cod_clasificador': f'23.15.{np.random.randint(11,19)}',
            'desc_clasificador': f'GASTOS DE BIENES Y MATERIALES DE OFICINA',
            'cod_unimed': it[2],
            'desc_unimed': it[3],
            'cantidad': cant,
            'pre_unitario': pre,
            'enero': m_vals[0], 'febrero': m_vals[1], 'marzo': m_vals[2], 'abril': m_vals[3],
            'mayo': m_vals[4], 'junio': m_vals[5], 'julio': m_vals[6], 'agosto': m_vals[7],
            'setiembre': m_vals[8], 'octubre': m_vals[9], 'noviembre': m_vals[10], 'diciembre': m_vals[11],
            'tot_item': tot,
            'ndetprior': np.random.randint(1, 3),
            'tipserv': np.random.choice(['BIEN', 'SERVICIO']),
            'obs_estado': np.random.choice(['APROBADO', 'EN REVISIÓN', 'CON REQUERIMIENTO']),
            'tot_cantcons': cant,
            'cant_exclu': 0,
            'sol_exclu': 'NO',
            'num_req': f'REQ-{np.random.randint(100,999)}-2026',
            'num_ccp': f'CCP-{np.random.randint(1000,5000)}',
            'tipo_orden': np.random.choice(['O/C', 'O/S']),
            'ocanumero': f'ORD-{np.random.randint(10000,99999)}',
            'num_siaf': f'{np.random.randint(100000,999999)}',
            'ruc': prov[0],
            'razonsocial': prov[1],
            'importe': tot
        }
        data.append(row)
    return pd.DataFrame(data)

# HEADER PRINCIPAL
st.markdown("""
    <div class="main-header">
        <div class="deploy-label">Deploy</div>
        <div class="brand-container">
            <!-- Icono Vectorial Premium de Máscara/Corona Inca Sol Inti -->
            <svg class="inca-logo" viewBox="0 0 24 24">
                <path d="M12 2a10 10 0 0 0-10 10c0 4.15 2.5 7.73 6 9.3V21a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v.3c3.5-1.57 6-5.15 6-9.3A10 10 0 0 0 12 2zm0 2a2 2 0 1 1 0 4 2 2 0 0 1 0-4zm-5 8a1.5 1.5 0 1 1 3 0 1.5 1.5 0 0 1-3 0zm5 7a4 4 0 0 1-4-4h8a4 4 0 0 1-4 4zm5-7a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/>
                <path d="M12 1a1 1 0 0 1 1 1v1a1 1 0 0 1-2 0V21a1 1 0 0 1 1-1zm11 11a1 1 0 0 1-1 1h-1a1 1 0 0 1 0-2h1a1 1 0 0 1 1 1zM2 12a1 1 0 0 1 1-1h1a1 1 0 0 1 0 2H3a1 1 0 0 1-1-1z"/>
            </svg>
            <h1>KAMAYUQ</h1>
        </div>
        <p>Extracción, Consolidación y Visualización de Información Presupuestal y Logística</p>
    </div>
""", unsafe_allow_html=True)

# SIDEBAR: Configuración y Carga
st.sidebar.image("https://img.icons8.com/external-flat-icons-incompetech/64/000000/external-dashboard-digital-marketing-flat-icons-incompetech.png", width=45)
st.sidebar.title("Configuración y Carga")

uploaded_file = st.sidebar.file_uploader("Cargar Archivo de Datos (Excel/CSV)", type=['xlsx', 'csv'])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.sidebar.success("¡Datos cargados exitosamente!")
    except Exception as e:
        st.sidebar.error(f"Error al cargar el archivo: {e}")
        df = generate_mock_data()
else:
    df = generate_mock_data()

# Validar Columnas
for col in COLUMNS_STRUCTURE:
    if col not in df.columns:
        df[col] = 0 if col in MONTHS or col in ['cantidad', 'pre_unitario', 'importe', 'tot_item'] else ''
    else:
        if col in MONTHS or col in ['cantidad', 'pre_unitario', 'importe', 'tot_item']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# FILTROS DE SELECCIÓN ÚNICA
st.sidebar.subheader("Filtros Ejecutivos")

def get_clean_options(dataframe, column_name):
    clean_series = dataframe[column_name].astype(str).str.strip().replace(['nan', 'None', ''], np.nan).dropna()
    return sorted(list(clean_series.unique()))

options_oficina = ["[ Todas las Oficinas ]"] + get_clean_options(df, 'desc_oficina')
selected_oficina = st.sidebar.selectbox("Oficina / Unidad Orgánica", options=options_oficina, index=0)

options_programa = ["[ Todos los Programas ]"] + get_clean_options(df, 'desc_prog')
selected_programa = st.sidebar.selectbox("Programa Presupuestal", options=options_programa, index=0)

options_meta = ["[ Todas las Metas ]"] + get_clean_options(df, 'meta')
selected_meta = st.sidebar.selectbox("Meta Presupuestaria", options=options_meta)

options_estado = ["[ Todos los Estados ]"] + get_clean_options(df, 'obs_estado')
selected_estado = st.sidebar.selectbox("Estado de Obligación", options=options_estado)

# Lógica del Filtrado
filtered_df = df.copy()
if selected_oficina != "[ Todas las Oficinas ]":
    filtered_df = filtered_df[filtered_df['desc_oficina'].astype(str).str.strip() == selected_oficina]
if selected_programa != "[ Todos los Programas ]":
    filtered_df = filtered_df[filtered_df['desc_prog'].astype(str).str.strip() == selected_programa]
if selected_meta != "[ Todas las Metas ]":
    filtered_df = filtered_df[filtered_df['meta'].astype(str).str.strip() == selected_meta]
if selected_estado != "[ Todos los Estados ]":
    filtered_df = filtered_df[filtered_df['obs_estado'].astype(str).str.strip() == selected_estado]

# SECCIÓN 1: KPI CARDS
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="metric-card" style="border-top-color: #013C58;">
            <div class="metric-title">Importe Total Consolidado</div>
            <div class="metric-value">S/. {filtered_df['importe'].sum():,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card" style="border-top-color: #00537A;">
            <div class="metric-title">Items Únicos Gestionados</div>
            <div class="metric-value">{filtered_df['cod_item'].nunique()}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card" style="border-top-color: #F5A201;">
            <div class="metric-title">Expedientes SIAF</div>
            <div class="metric-value">{filtered_df['num_siaf'].nunique()}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card" style="border-top-color: #FFBA42;">
            <div class="metric-title">Oficinas Reportando</div>
            <div class="metric-value">{filtered_df['cod_oficina'].nunique()}</div>
        </div>
    """, unsafe_allow_html=True)

# SECCIÓN 2: PESTAÑAS DE ANÁLISIS INTERACTIVO
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard Ejecutivo", "📅 Programación Mensual", "🏢 Oficinas y Metas", "📋 Reporteador Completo"])

with tab1:
    st.subheader("Análisis de Distribución Gasto Financiero")
    g1, g2 = st.columns(2)
    
    with g1:
        st.markdown('<div class="chart-container"><div class="chart-title">Ejecución Financiera por Oficina</div>', unsafe_allow_html=True)
        oficina_df_clean = filtered_df.copy()
        oficina_df_clean['desc_oficina'] = oficina_df_clean['desc_oficina'].astype(str)
        
        if not oficina_df_clean.empty and oficina_df_clean['importe'].sum() > 0:
            oficina_gasto = oficina_df_clean.groupby('desc_oficina')['importe'].sum().reset_index().sort_values(by='importe', ascending=False).head(8)
            fig_oficina = px.bar(
                oficina_gasto, 
                x='importe', 
                y='desc_oficina', 
                orientation='h',
                labels={'importe': 'Importe (S/.)', 'desc_oficina': 'Oficina'},
                color='importe',
                color_continuous_scale=['#A8E8F9', '#00537A', '#013C58'] 
            )
            fig_oficina.update_traces(marker_line_color='rgba(255,255,255,0.6)', marker_line_width=1.5, opacity=0.95)
            fig_oficina.update_layout(
                yaxis={'categoryorder':'total ascending', 'title': None}, 
                xaxis={'title': None, 'tickformat': ",.0f"}, 
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False, margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False
            )
            st.plotly_chart(fig_oficina, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No hay registros financieros para la combinación de filtros seleccionada.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with g2:
        st.markdown('<div class="chart-container"><div class="chart-title">Distribución por Tipo de Orden (O/C vs O/S)</div>', unsafe_allow_html=True)
        ordenes_df_clean = filtered_df.copy()
        ordenes_df_clean['tipo_orden'] = ordenes_df_clean['tipo_orden'].astype(str)
        
        if not ordenes_df_clean.empty and ordenes_df_clean['importe'].sum() > 0:
            ordenes_dist = ordenes_df_clean.groupby('tipo_orden')['importe'].sum().reset_index()
            fig_ordenes = px.pie(
                ordenes_dist, 
                values='importe', 
                names='tipo_orden', 
                hole=0.6,
                color_discrete_sequence=['#013C58', '#F5A201'] 
            )
            fig_ordenes.update_traces(textposition='outside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=3)))
            fig_ordenes.update_layout(paper_bgcolor='rgba(0,0,0,0)', showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_ordenes, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("No hay registros de órdenes para mostrar.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-container"><div class="chart-title">Top 5 Proveedores Estratégicos por Gasto Adjudicado</div>', unsafe_allow_html=True)
    prov_df_clean = filtered_df.copy()
    prov_df_clean['razonsocial'] = prov_df_clean['razonsocial'].astype(str)
    
    if not prov_df_clean.empty and prov_df_clean['importe'].sum() > 0:
        prov_df = prov_df_clean.groupby(['ruc', 'razonsocial'])['importe'].sum().reset_index().sort_values(by='importe', ascending=False).head(5)
        fig_prov = px.bar(
            prov_df,
            x='razonsocial',
            y='importe',
            color='importe',
            color_continuous_scale=['#FFBA42', '#F5A201'] 
        )
        fig_prov.update_traces(marker_line_width=0, opacity=0.9)
        fig_prov.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis={'title': None}, yaxis={'title': None, 'tickformat': ",.0f"},
            margin=dict(l=10, r=10, t=10, b=10), coloraxis_showscale=False
        )
        st.plotly_chart(fig_prov, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Sin datos de proveedores para mostrar.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Cronograma de Gasto Mensualizado")
    st.markdown('<div class="chart-container"><div class="chart-title">Evolución del Flujo Presupuestal Mensual</div>', unsafe_allow_html=True)
    
    if not filtered_df.empty:
        monthly_sums = filtered_df[MONTHS].sum().reset_index()
        monthly_sums.columns = ['Mes', 'Monto']
        
        fig_monthly = go.Figure()
        fig_monthly.add_trace(go.Scatter(
            x=monthly_sums['Mes'], 
            y=monthly_sums['Monto'],
            mode='lines+markers',
            line=dict(color='#00537A', width=3.5, shape='spline'), 
            marker=dict(size=8, color='#F5A201', line=dict(color='#FFFFFF', width=2)),
            fill='tozeroy',
            fillcolor='rgba(168, 232, 249, 0.15)' 
        ))
        fig_monthly.update_layout(
            xaxis_title=None, 
            yaxis_title=None, 
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            margin=dict(l=10, r=10, t=10, b=10)
        )
        fig_monthly.update_xaxes(showgrid=False)
        fig_monthly.update_yaxes(showgrid=True, gridcolor='#E2E8F0', tickformat=",.0f")
        st.plotly_chart(fig_monthly, use_container_width=True, config={'displayModeBar': False})
        st.dataframe(monthly_sums.set_index('Mes').T, use_container_width=True)
    else:
        st.info("No hay flujos mensuales correspondientes a los filtros aplicados.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.subheader("Estructura de Metas y Programas Presupuestales")
    st.markdown('<div class="chart-container"><div class="chart-title">Jerarquía de Distribución de Metas Críticas</div>', unsafe_allow_html=True)
    
    tab3_df = filtered_df.copy()
    tab3_df['desc_prog'] = tab3_df['desc_prog'].astype(str)
    tab3_df['meta'] = tab3_df['meta'].astype(str)
    
    if not tab3_df.empty and tab3_df['importe'].sum() > 0:
        prog_meta = tab3_df.groupby(['desc_prog', 'meta'])['importe'].sum().reset_index()
        prog_meta = prog_meta.sort_values(by='importe', ascending=False)
        
        top_n = st.slider("Mostrar el Top de elementos en pantalla", min_value=5, max_value=20, value=10)
        prog_meta_top = prog_meta.head(top_n)
        
        fig_bar_exec = px.bar(
            prog_meta_top,
            x='importe',
            y='meta',
            color='desc_prog',
            orientation='h',
            color_discrete_sequence=['#013C58', '#00537A', '#A8E8F9', '#FFBA42']
        )
        fig_bar_exec.update_traces(marker_line_width=1, marker_line_color='rgba(255,255,255,0.8)')
        fig_bar_exec.update_layout(
            yaxis={'categoryorder': 'total ascending', 'type': 'category', 'title': None},
            xaxis={'title': None, 'tickformat': ",.0f"},
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=-0.4, xanchor="left", x=0),
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_bar_exec, use_container_width=True, config={'displayModeBar': False})
        
        with st.expander("🔍 Ver Matriz Detallada de Datos"):
            st.dataframe(prog_meta.style.format({'importe': 'S/. {:,.2f}'}), use_container_width=True)
    else:
        st.info("Sin registros jerárquicos para esta combinación de filtros.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.subheader("Extractor y Consolidador de Información")
    st.write(f"Registros filtrados: {filtered_df.shape[0]} de {df.shape[0]}.")
    
    visible_cols = st.multiselect("Seleccionar Columnas para el Reporte Customizado", options=COLUMNS_STRUCTURE, default=['meta', 'desc_oficina', 'desc_prog', 'desc_item', 'cantidad', 'pre_unitario', 'importe', 'obs_estado', 'num_siaf'])
    
    if visible_cols:
        st.dataframe(filtered_df[visible_cols], use_container_width=True)
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                filtered_df[visible_cols].to_excel(writer, index=False, sheet_name='Reporte KAMAYUQ')
            processed_data = output.getvalue()
            st.download_button(label="📥 Descargar Reporte en Excel (.xlsx)", data=processed_data, file_name='reporte_kamayuq_consolidado.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            
        with col_exp2:
            csv_data = filtered_df[visible_cols].to_csv(index=False).encode('utf-8')
            st.download_button(label="📄 Descargar Reporte en CSV", data=csv_data, file_name='reporte_kamayuq_consolidado.csv', mime='text/csv')
    else:
        st.warning("Seleccione al menos una columna para mostrar el reporte.")

# Pie de página con firma de desarrollo de alta dirección
st.markdown("""
    <hr style="border:1px solid #CBD5E1">
    <div style="text-align: center; color: #1E293B; font-size: 0.85rem; font-weight: 600; margin-bottom: 5px;">
        KAMAYUQ Reporteador Core v1.6 • Inteligencia de Negocios de Alta Dirección • 2026
    </div>
    <div style="text-align: center; color: #64748B; font-size: 0.75rem; font-weight: 400; letter-spacing: 0.05em;">
        © All Rights Reserved • Desarrollado por <strong>Digitalia-Max</strong>
    </div>
""", unsafe_allow_html=True)