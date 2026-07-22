import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="KAMAYUQ v2.0 - Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILOS OESTE SATINADO CON ENFOQUE EN MÁXIMO PROTAGONISMO DE GRÁFICOS
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
            padding-top: 0.8rem !important;    
            padding-bottom: 1.5rem !important;  
            padding-left: clamp(1vw, 2vw, 2vw) !important;    
            padding-right: clamp(1vw, 2vw, 2vw) !important;
            max-width: 100% !important;        
            overflow-x: hidden !important;
        }
        
        /* Fondo General Arena Seda */
        .stApp {
            background: #F8F6F0;
            color: #264653;
        }
        
        /* Panel Lateral Cuero Obscuro */
        [data-testid="stSidebar"] {
            background-color: #121E30;
            color: #FFFFFF;
        }
        
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
            color: #E2E8F0 !important;
            font-weight: 600 !important;
        }
        
        /* Contenedores de Filtro */
        div[data-baseweb="select"] {
            background-color: #FFFFFF !important; 
            border-radius: 10px !important;
            border: 1.5px solid #E5E0D8 !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
            max-width: 100% !important;
        }
        
        div[data-baseweb="select"]:hover {
            border-color: #D65A31 !important;
        }
        
        div[data-baseweb="select"] div {
            color: #264653 !important;
            font-weight: 700 !important;
        }
        
        /* BANNER SLIM EXECUTIVE (ALTURA REDUCIDA) */
        .main-header {
            background: linear-gradient(135deg, #1D3557 0%, #121E30 100%) !important;
            padding: 12px 24px !important; 
            border-radius: 12px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 6px 18px -4px rgba(29, 53, 87, 0.2) !important;
            border-left: 5px solid #D65A31 !important;
            border-top: 1px solid rgba(233, 196, 106, 0.2) !important;
            border-right: 1px solid rgba(229, 224, 216, 0.3) !important;
            border-bottom: 1px solid rgba(229, 224, 216, 0.3) !important;
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            justify-content: space-between !important;
            width: 100% !important;
        }
        
        .brand-container {
            display: flex;
            align-items: center;
            gap: 14px; 
            flex-wrap: wrap; 
        }
        
        .inca-logo {
            width: 32px; 
            height: 32px;
            fill: #E9C46A;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
        }
        
        .main-header h1 {
            color: #FFFFFF !important; 
            margin: 0;
            font-size: 1.45rem !important; 
            font-weight: 800;
            letter-spacing: -0.01em;
            line-height: 1.1;
        }
        
        .main-header p {
            color: #E9C46A !important; 
            opacity: 0.95;
            margin: 0;
            font-size: 0.82rem !important;
            font-weight: 600;
        }
        
        /* GRID DE KPIS COMPACTAS (AORRO VERTICAL) */
        .kpi-responsive-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 10px;
            width: 100%;
            margin-bottom: 12px;
        }

        @media (max-width: 1200px) {
            .kpi-responsive-grid {
                grid-template-columns: repeat(4, 1fr);
            }
        }
        @media (max-width: 768px) {
            .kpi-responsive-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        @media (max-width: 480px) {
            .kpi-responsive-grid {
                grid-template-columns: 1fr;
            }
        }
        
        /* Tarjetas Métricas Slim */
        .metric-card {
            background: #FFFFFF;
            border-radius: 12px;
            padding: 8px 12px;
            box-shadow: 0 4px 12px -2px rgba(38, 70, 83, 0.05);
            border: 1px solid #E5E0D8;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 72px;
            width: 100%;
            overflow: hidden;
            word-break: break-word;
        }
        
        .metric-title {
            font-size: 0.62rem;
            color: #6C757D !important; 
            text-transform: uppercase;
            font-weight: 800;
            letter-spacing: 0.04em;
            margin-bottom: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .metric-value {
            font-size: clamp(0.9rem, 1.2vw, 1.25rem) !important; 
            color: #1D3557 !important; 
            font-weight: 800;
            line-height: 1.1;
            white-space: nowrap;
        }
        
        /* Badges de Semáforo Satin Slim */
        .semaforo-badge {
            position: absolute;
            top: 6px;
            right: 6px;
            padding: 2px 6px;
            border-radius: 12px;
            font-size: 0.52rem;
            font-weight: 800;
            text-transform: uppercase;
        }
        .badge-rojo { background-color: #F8D7DA; color: #D65A31; }
        .badge-amarillo { background-color: #FFF3CD; color: #B5838D; }
        .badge-verde { background-color: #D1E7DD; color: #2A9D8F; }
        
        /* CONTENEDORES DE GRÁFICOS MAXIMIZADOS */
        .chart-container {
            background: #FFFFFF;
            border-radius: 18px;
            padding: 16px 18px 10px 18px;
            box-shadow: 0 10px 25px -4px rgba(38, 70, 83, 0.06);
            border: 1px solid #E5E0D8;
            margin-bottom: 16px;
            width: 100%;
            max-width: 100%;
            overflow-x: auto;
        }
        
        .chart-title {
            font-size: 0.95rem;
            color: #1D3557;
            font-weight: 800;
            margin-bottom: 8px;
            border-left: 4px solid #D65A31;
            padding-left: 10px;
        }
        
        .stTabs [data-baseweb="tab-list"] { 
            gap: 6px; 
            flex-wrap: wrap !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-weight: 800; 
            color: #6C757D !important; 
            padding: 6px 16px; 
            background-color: #E5E0D8; 
            border-radius: 8px 8px 0px 0px;
            font-size: 0.82rem;
        }
        .stTabs [aria-selected="true"] { 
            background: #1D3557 !important; 
            color: #FFFFFF !important; 
        }
        
        /* ENCABEZADOS DE TABLA EN MAYÚSCULA Y NEGRITA */
        div[data-testid="stDataFrame"] {
            width: 100% !important;
            max-width: 100% !important;
            overflow-x: auto !important;
            border-radius: 12px !important;
            background-color: #FFFFFF !important;
            border: 1px solid #E5E0D8;
        }

        div[data-testid="stDataFrame"] th {
            font-weight: 800 !important;
            text-transform: uppercase !important;
            color: #1D3557 !important;
            letter-spacing: 0.03em !important;
            font-size: clamp(0.65rem, 0.9vw, 0.8rem) !important;
        }
    </style>
""", unsafe_allow_html=True)

# Columnas
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

DEFAULT_REPORT_COLUMNS = [
    'cod_oficina', 'desc_oficina', 'meta', 'cod_item', 'desc_item',
    'cod_clasificador', 'cod_unimed', 'cantidad', 'pre_unitario',
    'tipserv', 'num_req', 'num_ccp', 'ocanumero', 'num_siaf',
    'ruc', 'razonsocial', 'importe'
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

# Banner Principal Slim
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

# Panel Lateral
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

for col in COLUMNS_STRUCTURE:
    if col not in df_raw.columns:
        df_raw[col] = 0 if col in MONTHS or col in ['cantidad', 'pre_unitario', 'importe', 'tot_item', 'tot_cantcons', 'cant_exclu'] else ''

df_raw['importe'] = pd.to_numeric(df_raw['importe'], errors='coerce').fillna(0)
df_raw['tot_item'] = pd.to_numeric(df_raw['tot_item'], errors='coerce').fillna(0)
df_raw['cantidad'] = pd.to_numeric(df_raw['cantidad'], errors='coerce').fillna(0)
df_raw['tot_cantcons'] = pd.to_numeric(df_raw['tot_cantcons'], errors='coerce').fillna(0)
df_raw['cant_exclu'] = pd.to_numeric(df_raw['cant_exclu'], errors='coerce').fillna(0)

for m in MONTHS:
    df_raw[m] = pd.to_numeric(df_raw[m], errors='coerce').fillna(0)

# Filtros
st.sidebar.subheader("Filtros en Cascada (BI)")

oficinas_limpias = sorted([str(x) for x in df_raw['desc_oficina'].dropna().unique() if str(x).strip() != ''])
oficinas_disponibles = ["[ Todas las Oficinas ]"] + oficinas_limpias
selected_oficina = st.sidebar.selectbox("1. Filtrar por Oficina Orgánica / Área", oficinas_disponibles)

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

filtered_df = df_step2.copy().reset_index(drop=True)
if selected_meta != "[ Todas las Metas ]":
    filtered_df = filtered_df[filtered_df['meta'].astype(str) == selected_meta].reset_index(drop=True)

# Cálculos
monto_total_asignado = filtered_df['tot_item'].sum()
monto_total_ejecutado = filtered_df[MONTHS[:7]].sum().sum()
ratio_ejecucion = (monto_total_ejecutado / monto_total_asignado) if monto_total_asignado > 0 else 0

filtered_df['ejecutado_acum_row'] = filtered_df[MONTHS[:7]].sum(axis=1).fillna(0)

filtered_df['cant_programada'] = np.where(filtered_df['tot_cantcons'] > 0, filtered_df['tot_cantcons'], filtered_df['cantidad'])
filtered_df['cant_excluida'] = filtered_df['cant_exclu']
filtered_df['cant_incluida'] = (filtered_df['cant_programada'] - filtered_df['cant_excluida']).clip(lower=0)

ratio_row = np.where(filtered_df['importe'] > 0, filtered_df['ejecutado_acum_row'] / filtered_df['importe'], 0)
ratio_row = np.clip(ratio_row, 0, 1)

filtered_df['cant_atendida'] = np.round(filtered_df['cant_incluida'] * ratio_row, 2)
filtered_df['cant_disponible'] = np.round(filtered_df['cant_incluida'] * (1 - ratio_row), 2)

badge_html = ""
card_style = ""
if ratio_ejecucion > 0.85:
    badge_html = '<span class="semaforo-badge badge-rojo">⚠️ Acelerado</span>'
    card_style = "border-top: 3.5px solid #D65A31;"
elif ratio_ejecucion < 0.40:
    badge_html = '<span class="semaforo-badge badge-amarillo">📉 Subejec.</span>'
    card_style = "border-top: 3.5px solid #E9C46A;"
else:
    badge_html = '<span class="semaforo-badge badge-verde">✅ Óptimo</span>'
    card_style = "border-top: 3.5px solid #2A9D8F;"

tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ejecutivo v2.0", "🎛️ Planificador Simulador 'What-If'", "📋 Reporteador y Descargas"])

# PESTAÑA 1
with tab1:
    col_mapping = {
        'cod_oficina': 'COD. OFICINA',
        'meta': 'META',
        'cod_item': 'COD. ÍTEM',
        'desc_item': 'DESCRIPCIÓN DEL ÍTEM',
        'cant_programada': 'CANT. PROGRAMADA',
        'cant_atendida': 'CANT. ATENDIDA',
        'cant_excluida': 'CANT. EXCLUIDA',
        'cant_disponible': 'CANT. DISPONIBLE',
        'pre_unitario': 'PRECIO UNITARIO',
        'importe': 'IMPORTE TOTAL',
        'num_siaf': 'N° SIAF'
    }
    df_display = filtered_df[list(col_mapping.keys())].rename(columns=col_mapping)
    
    if 'selected_item_idx' not in st.session_state:
        st.session_state.selected_item_idx = None

    if st.session_state.selected_item_idx is not None and st.session_state.selected_item_idx < len(filtered_df):
        item_row = filtered_df.iloc[st.session_state.selected_item_idx]
        val_cant_prog = item_row['cant_programada']
        val_cant_atend = item_row['cant_atendida']
        val_cant_excl = item_row['cant_excluida']
        val_cant_disp = item_row['cant_disponible']
    else:
        val_cant_prog = filtered_df['cant_programada'].sum()
        val_cant_atend = filtered_df['cant_atendida'].sum()
        val_cant_excl = filtered_df['cant_excluida'].sum()
        val_cant_disp = filtered_df['cant_disponible'].sum()

    # TARJETAS EN GRID COMPACTAS
    st.markdown(f"""
        <div class="kpi-responsive-grid">
            <div class="metric-card" style="{card_style}">
                <div class="metric-title">Velocidad Ejecución</div>
                <div class="metric-value">{ratio_ejecucion*100:.1f}%</div>
                {badge_html}
            </div>
            <div class="metric-card" style="border-top:3.5px solid #1D3557;">
                <div class="metric-title">Techo Programado</div>
                <div class="metric-value">S/. {monto_total_asignado:,.2f}</div>
            </div>
            <div class="metric-card" style="border-top:3.5px solid #264653;">
                <div class="metric-title">Girado Ejecutado</div>
                <div class="metric-value">S/. {monto_total_ejecutado:,.2f}</div>
            </div>
            <div class="metric-card" style="border-top:3.5px solid #2A9D8F;">
                <div class="metric-title">Cant. Programada</div>
                <div class="metric-value">{val_cant_prog:,.0f}</div>
            </div>
            <div class="metric-card" style="border-top:3.5px solid #457B9D;">
                <div class="metric-title">Cant. Atendida</div>
                <div class="metric-value">{val_cant_atend:,.0f}</div>
            </div>
            <div class="metric-card" style="border-top:3.5px solid #D65A31;">
                <div class="metric-title">Cant. Excluida</div>
                <div class="metric-value">{val_cant_excl:,.0f}</div>
            </div>
            <div class="metric-card" style="border-top:3.5px solid #E9C46A;">
                <div class="metric-title">Ítems Disponibles</div>
                <div class="metric-value">{val_cant_disp:,.0f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ------------------------------------------------------
    # GRÁFICOS MÁXIMO PROTAGONISMO (ALTURA 370px)
    # ------------------------------------------------------
    st.subheader("Centro de Control y Balance de Impacto")
    v1, v2, v3 = st.columns([1, 1.25, 1])
    
    # 1. ANILLO PRESUPUESTAL AMPLIADO
    with v1:
        st.markdown('<div class="chart-container"><div class="chart-title">Avance Presupuestal Consolidado</div>', unsafe_allow_html=True)
        monto_disp = max(0, monto_total_asignado - monto_total_ejecutado)
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=['Ejecutado (Girado)', 'Saldo Disponible'],
            values=[monto_total_ejecutado, monto_disp],
            hole=.65,
            marker=dict(colors=['#1D3557', '#E9C46A'], line=dict(color='#FFFFFF', width=2.5)),
            textinfo='percent',
            textfont=dict(family="Plus Jakarta Sans", size=13, color="#FFFFFF", weight="bold"),
            hoverinfo='label+value'
        )])
        fig_donut.update_layout(
            annotations=[dict(text=f"<b>{ratio_ejecucion*100:.1f}%</b><br><span style='font-size:11px; color:#6C757D;'>Avance</span>", x=0.5, y=0.5, font_size=26, showarrow=False, font_color="#1D3557", font_family="Plus Jakarta Sans")],
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
            autosize=True,
            height=370,
            margin=dict(l=10, r=10, t=10, b=25),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. BARRAS COMPARATIVAS DUAL AMPLIADAS
    with v2:
        st.markdown('<div class="chart-container"><div class="chart-title">Desempeño Comparativo: Financiero vs. Físico</div>', unsafe_allow_html=True)
        
        pct_fisico = (val_cant_atend / val_cant_prog * 100) if val_cant_prog > 0 else 0
        pct_financiero = ratio_ejecucion * 100
        
        fig_bar_dual = go.Figure()
        fig_bar_dual.add_trace(go.Bar(
            y=['Avance Financiero', 'Atención Física'],
            x=[pct_financiero, pct_fisico],
            orientation='h',
            marker=dict(color=['#1D3557', '#2A9D8F'], line=dict(color='#FFFFFF', width=2)),
            text=[f"{pct_financiero:.1f}%", f"{pct_fisico:.1f}%"],
            textposition='outside',
            textfont=dict(family='Plus Jakarta Sans', size=13, color='#1D3557', weight="bold")
        ))
        
        fig_bar_dual.update_layout(
            autosize=True,
            height=370,
            margin=dict(l=10, r=45, t=25, b=10),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(range=[0, 118], showgrid=True, gridcolor='#E5E0D8', title="% de Cumplimiento"),
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_bar_dual, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. DONUT OPERATIVO TRIPLE AMPLIADO
    with v3:
        st.markdown('<div class="chart-container"><div class="chart-title">Distribución de Carga Operativa</div>', unsafe_allow_html=True)
        
        fig_radial_ring = go.Figure(data=[go.Pie(
            labels=['Atendidos', 'Disponibles', 'Excluidos'],
            values=[val_cant_atend, val_cant_disp, val_cant_excl],
            hole=.60,
            marker=dict(colors=['#2A9D8F', '#E9C46A', '#D65A31'], line=dict(color='#FFFFFF', width=2.5)),
            textinfo='label+percent',
            textfont=dict(family='Plus Jakarta Sans', size=12, color='#1D3557', weight="bold"),
            hoverinfo='label+value'
        )])
        
        fig_radial_ring.update_layout(
            annotations=[dict(
                text=f"<b>{val_cant_prog:,.0f}</b><br><span style='font-size:11px; color:#6C757D;'>Ítems Total</span>",
                x=0.5, y=0.5, font_size=22, showarrow=False, font_color="#1D3557", font_family="Plus Jakarta Sans"
            )],
            showlegend=False,
            autosize=True,
            height=370,
            margin=dict(l=15, r=15, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_radial_ring, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    # Relación de Ítems (Tabla)
    st.markdown('<div class="chart-container"><div class="chart-title">Relación Detallada de Ítem(s) (Haga clic en una fila para medirla en tiempo real)</div>', unsafe_allow_html=True)
    
    event_selection = st.dataframe(
        df_display, 
        use_container_width=True,
        height=280,
        on_select="rerun",
        selection_mode="single-row"
    )
    
    if event_selection and hasattr(event_selection, "selection"):
        selected_rows = event_selection.selection.rows
        if len(selected_rows) > 0:
            if st.session_state.selected_item_idx != selected_rows[0]:
                st.session_state.selected_item_idx = selected_rows[0]
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# PESTAÑA 2: SIMULADOR
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
    fig_comp.add_trace(go.Bar(name='Presupuesto Original', x=comp_df['desc_oficina'], y=comp_df['importe'], marker_color='#1D3557'))
    fig_comp.add_trace(go.Bar(name='Escenario Simulado', x=comp_df['desc_oficina'], y=comp_df['importe_simulado'], marker_color='#E9C46A'))
    fig_comp.update_layout(barmode='group', autosize=True, height=320, margin=dict(l=10, r=10, t=15, b=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#1D3557'))
    st.plotly_chart(fig_comp, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

# PESTAÑA 3: REPORTEADOR
with tab3:
    st.subheader("Extractor Avanzado de Reportes")
    
    cols_seleccionadas = st.multiselect(
        "Columnas de Salida", 
        options=COLUMNS_STRUCTURE, 
        default=DEFAULT_REPORT_COLUMNS
    )
    
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
    <hr style="border:1px solid #E5E0D8">
    <div style="text-align: center; color: #6C757D; font-size: 0.85rem; font-weight: 600;">KAMAYUQ Business Intelligence Intel Core v2.0 • 2026</div>
""", unsafe_allow_html=True)
