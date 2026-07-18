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

# Estilos CSS de Alta Dirección (Responsivo, Azul 95% - Dorado 5%, Tarjetas con Semáforos)
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
        
        /* BANNER EN GRADIENTE FLUIDO (AZUL 95% - DORADO 5%) */
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
        
        /* Tarjetas con Semáforos */
        .metric-card {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px -3px rgba(1, 60, 88, 0.06);
            border-top: 4px solid #CBD5E1; 
            margin-bottom: 15px;
            width: 100%;
            position: relative;
        }
        
        .metric-title {
            font-size: 0.8rem;
            color: #475569 !important; 
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.05em;
        }
        
        .metric-value {
            font-size: clamp(1.5rem, 2.5vw, 2rem) !important; 
            color: #013C58 !important; 
            font-weight: 800;
            margin-top: 6px;
            word-wrap: break-word; 
        }
        
        /* Badges de Semáforos */
        .semaforo-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
        }
        .badge-rojo { background-color: #FEE2E2; color: #991B1B; }
        .badge-amarillo { background-color: #FEF3C7; color: #92400E; }
        .badge-verde { background-color: #D1FAE5; color: #065F46; }
        
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
        
        .stTabs [data-baseweb="tab-list"] { gap: 4px; }
        .stTabs [data-baseweb="tab"] {
            font-weight: 700; color: #1E293B !important; 
            padding: 10px 16px; background-color: #E2E8F0; border-radius: 6px 6px 0px 0px;
        }
        .stTabs [aria-selected="true"] { background-color: #013C58 !important; color: white !important; }
        
        .stButton>button {
            background-color: #00537A !important; color: white !important;
            border-radius: 8px !important; font-weight: 600 !important; width: 100%;
        }
        .stButton>button:hover { background-color: #F5A201 !important; color: #013C58 !important; }
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
    n_rows = 200
    oficinas = [
        ('100', 'OFICINA DE TECNOLOGÍA DE LA INFORMACIÓN'),
        ('200', 'OFICINA DE ADMINISTRACIÓN Y FINANZAS'),
        ('300', 'OFICINA DE RECURSOS HUMANOS'),
        ('400', 'GERENCIA DE PLANEAMIENTO Y PRESUPUESTO'),
        ('500', 'DIRECCIÓN DE OPERACIONES')
    ]
    programas = {
        'OFICINA DE TECNOLOGÍA DE LA INFORMACIÓN': [('0001', 'OPTIMIZACIÓN TI'), ('9001', 'ACCIONES CENTRALES TI')],
        'OFICINA DE ADMINISTRACIÓN Y FINANZAS': [('0068', 'REDUCCIÓN DE VULNERABILIDAD AF'), ('9001', 'ACCIONES CENTRALES AF')],
        'OFICINA DE RECURSOS HUMANOS': [('9001', 'ACCIONES CENTRALES RRHH')],
        'GERENCIA DE PLANEAMIENTO Y PRESUPUESTO': [('0001', 'PLANEAMIENTO ESTRATÉGICO')],
        'DIRECCIÓN DE OPERACIONES': [('0090', 'LOGROS DE APRENDIZAJE'), ('0068', 'EMERGENCIAS')]
    }
    
    data = []
    for i in range(n_rows):
        of = oficinas[np.random.choice(len(oficinas))]
        progs = programas[of[1]]
        prog = progs[np.random.choice(len(progs))]
        meta = f'{np.random.randint(1, 5):03d}' if of[0]=='100' else f'{np.random.randint(6, 12):03d}'
        
        cant = np.random.randint(5, 40)
        pre = np.random.choice([12.5, 45.0, 120.0, 2500.0])
        tot = cant * pre
        
        m_vals = np.zeros(12)
        # Simular distribución hasta julio de 2026 (mes actual)
        for m in range(7): 
            if np.random.rand() > 0.3:
                m_vals[m] = round((tot * np.random.rand()) / 4, 2)
        
        row = {
            'meta': meta, 'cod_oficina': of[0], 'desc_oficina': of[1],
            'ftefto': '1-00', 'codigo_poi': 'POI-2026', 'correlativo_poi': 1, 'cadena_pptal': '2.3.1',
            'cod_prog': prog[0], 'desc_prog': prog[1], 'cod_proproy': '3000001', 'desc_proproy': 'PRODUCTO',
            'cod_activ': '50001', 'desc_activ': 'GESTION', 'cod_item': f'I{i}', 'desc_item': 'BIEN O SERVICIO INSTITUCIONAL',
            'cod_clasificador': '23.15', 'desc_clasificador': 'GASTOS', 'cod_unimed': 'UND', 'desc_unimed': 'UNIDAD',
            'cantidad': cant, 'pre_unitario': pre, 'enero': m_vals[0], 'febrero': m_vals[1], 'marzo': m_vals[2],
            'abril': m_vals[3], 'mayo': m_vals[4], 'junio': m_vals[5], 'julio': m_vals[6], 'agosto': m_vals[7],
            'setiembre': m_vals[8], 'octubre': m_vals[9], 'noviembre': m_vals[10], 'diciembre': m_vals[11],
            'tot_item': tot, 'ndetprior': 1, 'tipserv': 'BIEN', 'obs_estado': np.random.choice(['APROBADO', 'EN REVISIÓN']), 
            'tot_cantcons': cant, 'cant_exclu': 0, 'sol_exclu': 'NO', 'num_req': 'REQ-2026', 'num_ccp': 'CCP-2026', 'tipo_orden': np.random.choice(['O/C', 'O/S']),
            'ocanumero': 'ORD-2026', 'num_siaf': f'{np.random.randint(100000, 999999)}', 'ruc': '20100043841', 'razonsocial': 'PROVEEDOR CENTRAL S.A.', 'importe': tot
        }
        data.append(row)
    return pd.DataFrame(data)

# CABECERA INSTITUCIONAL
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

df_raw = generate_mock_data()

# ==========================================================
# PUNTO 3: IMPLEMENTACIÓN DE FILTROS EN CASCADA (ENCADENADOS)
# ==========================================================
st.sidebar.title("Filtros en Cascada (BI)")

# 1. Filtro Maestro: Oficina
oficinas_disponibles = ["[ Todas las Oficinas ]"] + sorted(list(df_raw['desc_oficina'].unique()))
selected_oficina = st.sidebar.selectbox("1. Filtrar por Oficina Orgánica", oficinas_disponibles)

# Filtrado intermedio para el segundo nivel
df_step1 = df_raw.copy()
if selected_oficina != "[ Todas las Oficinas ]":
    df_step1 = df_step1[df_step1['desc_oficina'] == selected_oficina]

# 2. Segundo Filtro: Programas correspondientes a la oficina seleccionada
programas_disponibles = ["[ Todos los Programas ]"] + sorted(list(df_step1['desc_prog'].unique()))
selected_programa = st.sidebar.selectbox("2. Programa Presupuestal (Filtrado)", programas_disponibles)

df_step2 = df_step1.copy()
if selected_programa != "[ Todos los Programas ]":
    df_step2 = df_step2[df_step2['desc_prog'] == selected_programa]

# 3. Tercer Filtro: Metas correspondientes a las selecciones anteriores
metas_disponibles = ["[ Todas las Metas ]"] + sorted(list(df_step2['meta'].unique()))
selected_meta = st.sidebar.selectbox("3. Meta Presupuestaria (Filtrada)", metas_disponibles)

# Filtro final consolidado
filtered_df = df_step2.copy()
if selected_meta != "[ Todas las Metas ]":
    filtered_df = filtered_df[filtered_df['meta'] == selected_meta]

# ==========================================================
# PUNTO 2: SEMÁFOROS DE ALERTA TEMPRANA (Grasas e Ineficiencias)
# ==========================================================
# Calculamos velocidad teórica de gasto a Julio (mes 7 de 12 = ~58.3% esperado)
monto_total_asignado = filtered_df['tot_item'].sum()
monto_total_ejecutado = filtered_df[MONTHS[:7]].sum().sum() # Ejecución acumulada real
ratio_ejecucion = (monto_total_ejecutado / monto_total_asignado) if monto_total_asignado > 0 else 0

badge_html = ""
card_style = ""
if ratio_ejecucion > 0.85:
    badge_html = '<span class="semaforo-badge badge-rojo">⚠️ Alerta: Gasto Acelerado</span>'
    card_style = "border-top: 4px solid #EF4444;"
elif ratio_ejecucion < 0.40:
    badge_html = '<span class="semaforo-badge badge-amarillo">📉 Alerta: Subejecución</span>'
    card_style = "border-top: 4px solid #F5A201;"
else:
    badge_html = '<span class="semaforo-badge badge-verde">✅ Gasto Óptimo</span>'
    card_style = "border-top: 4px solid #10B981;"

# PANEL DE KPI CARDS CON NAVEGACIÓN DE ESTADOS
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
        <div class="metric-card" style="{card_style}">
            <div class="metric-title">Salud Presupuestal Presunta</div>
            <div class="metric-value">{ratio_ejecucion*100:.1f}%</div>
            {badge_html}
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid #013C58;">
            <div class="metric-title">Techo Programado Activo</div>
            <div class="metric-value">S/. {monto_total_asignado:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid #00537A;">
            <div class="metric-title">Girado / Devengado Real</div>
            <div class="metric-value">S/. {monto_total_ejecutado:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
        <div class="metric-card" style="border-top: 4px solid #FFBA42;">
            <div class="metric-title">SIAF Registrados</div>
            <div class="metric-value">{filtered_df['num_siaf'].nunique()}</div>
        </div>
    """, unsafe_allow_html=True)

# PESTAÑAS DE ANÁLISIS ESTRATÉGICO
tab1, tab2, tab3 = st.tabs(["📊 Dashboard Ejecutivo v2.0", "🎛️ Planificador Simulador 'What-If'", "📋 Reporteador y Descargas"])

with tab1:
    st.subheader("Visualización del Modelo de Gasto Institucional")
    g1, g2 = st.columns(2)
    with g1:
        st.markdown('<div class="chart-container"><div class="chart-title">Distribución y Desempeño por Unidad Orgánica</div>', unsafe_allow_html=True)
        of_sum = filtered_df.groupby('desc_oficina')['importe'].sum().reset_index()
        fig_of = px.bar(of_sum, x='importe', y='desc_oficina', orientation='h', color_discrete_sequence=['#013C58'])
        fig_of.update_layout(autosize=True, height=280, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis={'title': None}, xaxis={'title': None})
        st.plotly_chart(fig_of, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    with g2:
        st.markdown('<div class="chart-container"><div class="chart-title">Cronograma y Curva de Ejecución Física</div>', unsafe_allow_html=True)
        m_sums = filtered_df[MONTHS].sum().reset_index()
        m_sums.columns = ['Mes', 'Monto']
        fig_m = go.Figure(go.Scatter(x=m_sums['Mes'], y=m_sums['Monto'], mode='lines+markers', line=dict(color='#F5A201', width=3), fill='tozeroy', fillcolor='rgba(245, 162, 1, 0.05)'))
        fig_m.update_layout(autosize=True, height=280, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_m, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# PUNTO 4: SIMULADOR ESTRATÉGICO PRESUPUESTAL ("WHAT-IF")
# ==========================================================
with tab2:
    st.subheader("Sala de Simulación Presupuestaria y Redistribución")
    st.info("Ajuste los multiplicadores tácticos para simular escenarios de austeridad o inyección presupuestaria sin afectar los archivos base.")
    
    # Sliders para simular variaciones porcentuales
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        factor_ti = st.slider("Variación Presupuestal TI (%)", min_value=-50, max_value=50, value=0, step=5)
        factor_adm = st.slider("Variación Presupuestal Administración (%)", min_value=-50, max_value=50, value=0, step=5)
    with col_s2:
        factor_ops = st.slider("Variación Presupuestal Operaciones (%)", min_value=-50, max_value=50, value=0, step=5)
        factor_plan = st.slider("Variación Presupuestal Planeamiento (%)", min_value=-50, max_value=50, value=0, step=5)
        
    # Aplicar simulación matemática en memoria
    sim_df = filtered_df.copy()
    
    def aplicar_simulacion(row):
        if 'TECNOLOGÍA' in str(row['desc_oficina']): return row['importe'] * (1 + factor_ti / 100)
        if 'ADMINISTRACIÓN' in str(row['desc_oficina']): return row['importe'] * (1 + factor_adm / 100)
        if 'OPERACIONES' in str(row['desc_oficina']): return row['importe'] * (1 + factor_ops / 100)
        if 'PLANEAMIENTO' in str(row['desc_oficina']): return row['importe'] * (1 + factor_plan / 100)
        return row['importe']
        
    sim_df['importe_simulado'] = sim_df.apply(aplicar_simulacion, axis=1)
    
    # Gráfico comparativo de impacto
    st.markdown('<div class="chart-container"><div class="chart-title">Impacto Técnico: Presupuesto Real vs Presupuesto Simulado</div>', unsafe_allow_html=True)
    comp_df = sim_df.groupby('desc_oficina')[['importe', 'importe_simulado']].sum().reset_index()
    
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(name='Presupuesto Original', x=comp_df['desc_oficina'], y=comp_df['importe'], marker_color='#013C58'))
    fig_comp.add_trace(go.Bar(name='Escenario Simulado', x=comp_df['desc_oficina'], y=comp_df['importe_simulado'], marker_color='#F5A201'))
    fig_comp.update_layout(barmode='group', autosize=True, height=300, margin=dict(l=10, r=10, t=15, b=10), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_comp, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.subheader("Extractor Avanzado de Reportes Customizados")
    cols_seleccionadas = st.multiselect("Columnas de Salida", options=COLUMNS_STRUCTURE, default=['meta', 'desc_oficina', 'desc_prog', 'importe', 'num_siaf'])
    if cols_seleccionadas:
        st.dataframe(filtered_df[cols_seleccionadas], use_container_width=True)
        
        # Botones de descarga directos
        c1, c2 = st.columns(2)
        with c1:
            out = BytesIO()
            with pd.ExcelWriter(out, engine='openpyxl') as writer:
                filtered_df[cols_seleccionadas].to_excel(writer, index=False, sheet_name='KAMAYUQ_BI')
            st.download_button(label="📥 Descargar Escenario Corporativo (Excel)", data=out.getvalue(), file_name='kamayuq_bi_report.xlsx')
        with c2:
            st.download_button(label="📄 Descargar Data Cruda (CSV)", data=filtered_df[cols_seleccionadas].to_csv(index=False).encode('utf-8'), file_name='kamayuq_bi_report.csv')

st.markdown("""
    <hr style="border:1px solid #CBD5E1">
    <div style="text-align: center; color: #1E293B; font-size: 0.85rem; font-weight: 600;">KAMAYUQ Business Intelligence Intel Core v2.0 • 2026</div>
""", unsafe_allow_html=True)
