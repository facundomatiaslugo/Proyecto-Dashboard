import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Argentina en los Mundiales", layout="wide", page_icon="🇦🇷")

# --- ESTILOS CSS---
st.markdown("""
<style>
    /* Fondo con gradiente celeste y oscuro */
    .stApp {
        background: linear-gradient(135deg, #0a1a33 0%, #1e3a5f 50%, #0a1a33 100%);
        color: #ffffff;
    }
    
    /* Títulos con el celeste de Argentina */
    h1 {
        color: #75AADB !important;
        font-weight: 900;
        text-align: center;
        text-shadow: 0 0 20px rgba(117, 170, 219, 0.5);
        font-size: 3rem !important;
        margin-bottom: 0;
    }
    h2, h3 { color: #A5C8E8 !important; font-weight: 700; }
    
    /* Subtítulo con efecto */
    .subtitle {
        text-align: center;
        color: #ffffff;
        font-size: 1.2rem;
        margin-bottom: 30px;
        opacity: 0.8;
    }
    
    /* Tarjetas de métricas con efecto glassmorphism celeste */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(117, 170, 219, 0.2) 0%, rgba(30, 58, 95, 0.6) 100%);
        border: 1px solid rgba(117, 170, 219, 0.5);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(117, 170, 219, 0.2);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(117, 170, 219, 0.4);
    }
    div[data-testid="stMetricValue"] {
        color: #75AADB !important;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-size: 0.9rem !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    /* Pestañas estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(117, 170, 219, 0.1);
        border-radius: 10px;
        color: #A5C8E8;
        padding: 12px 24px;
        font-weight: 600;
        border: 1px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #75AADB 0%, #1e3a5f 100%) !important;
        color: #ffffff !important;
        border: 1px solid #75AADB !important;
    }
    
    /* Tablas */
    div[data-testid="stDataFrame"] {
        border: 1px solid #75AADB;
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Info boxes */
    div[data-testid="stAlert"] {
        background-color: rgba(117, 170, 219, 0.15);
        border-left: 4px solid #75AADB;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def cargar_datos():
    partidos = pd.read_csv("datos_limpios/partidos_argentina.csv", parse_dates=["Date"])
    resumen = pd.read_csv("datos_limpios/resumen_argentina.csv")
    return partidos, resumen

# Asociá cada partido con su imagen: (año, rival) -> ruta
IMAGENES_PARTIDOS = {
    (2026, "Inglaterra"): "imagenes/MalvinasArgentinas.jpg",
}

@st.dialog("📸 Recuerdo del partido", width="small")
def mostrar_imagen(ruta, titulo):
    st.subheader(titulo)
    if os.path.exists(ruta):
        st.image(ruta, width=400)
    else:
        st.warning(f"No se encontró la imagen en: {ruta}")

try:
    partidos, resumen = cargar_datos()
except FileNotFoundError:
    st.error("⚠️ Ejecutá primero 'python scripts/limpieza.py' para generar los datos.")
    st.stop()
except Exception as e:
    st.error(f"⚠️ Error al leer los datos: {e}")
    st.stop()

# --- HEADER ---
st.title("🇦🇷 La Albiceleste en los Mundiales")
st.markdown('<p class="subtitle">Un recorrido por la historia de la Selección Argentina desde 1930 hasta hoy</p>', unsafe_allow_html=True)

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🏆 Resumen", "⚽ Goles y Goleadores", "📊 Partido a Partido"])

# --- PESTAÑA 1: RESUMEN ---
with tab1:
    st.header("📊 El Camino de la Albiceleste")
    
    # Tomar los totales desde el resumen oficial para incluir el torneo 2026 completo
    total_partidos = int(resumen["Partidos_Jugados"].sum())
    total_goles = int(resumen["Goles_Arg"].sum())
    titulos = resumen[resumen["Instancia"] == "🏆 Campeón"].shape[0]
    subcampeonatos = resumen[resumen["Instancia"] == "🥈 Subcampeón"].shape[0]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏆 Copas del Mundo", titulos)
    col2.metric("🥈 Subcampeonatos", subcampeonatos)
    col3.metric("⚽ Partidos Jugados", total_partidos) # Ahora dirá 96
    col4.metric("🎯 Goles Convertidos", total_goles)    # Ahora dirá 171
    
    st.markdown("---")
    st.subheader("🏅 Participaciones por Mundial")
    
    resumen_display = resumen.copy()
    resumen_display["Año"] = resumen_display["Año"].astype(int)
    
    st.dataframe(
        resumen_display[["Año", "Instancia", "Partidos_Jugados", "Goles_Arg", "Goles_Rival", "Goleador_Arg"]],
        width="stretch", hide_index=True
    )
    
    # Gráfico de evolución de goles
    st.subheader("📈 Evolución de Goles por Mundial")
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=resumen["Año"], y=resumen["Goles_Arg"],
        mode='lines+markers',
        line=dict(color='#75AADB', width=4),
        marker=dict(size=12, color='#ffffff', line=dict(color='#75AADB', width=3)),
        fill='tozeroy', fillcolor='rgba(117, 170, 219, 0.2)',
        name='Goles'
    ))
    fig_line.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ffffff", xaxis_title="Año", yaxis_title="Goles",
        hovermode='x unified'
    )
    st.plotly_chart(fig_line, width="stretch")

# --- PESTAÑA 2: GOLEADORES ---
with tab2:
    st.header("⚽ Ranking Histórico de Goleadores")
    
    # Diccionario con el Top 10 de goleadores históricos de Argentina en Mundiales
    TOP_GOLEADORES = {
        "Lionel Messi": 21,
        "Gabriel Batistuta": 10,
        "Diego Maradona": 8,
        "Guillermo Stábile": 8,
        "Mario Kempes": 6,
        "Gonzalo Higuaín": 5,
        "Julian Alvarez": 5,
        "Hernán Crespo": 4,
        "Jorge Valdano": 4,
        "Claudio Caniggia": 4,
    }
    
    # Convertimos el diccionario a un DataFrame para graficar
    df_goleadores = pd.DataFrame(list(TOP_GOLEADORES.items()), columns=["Jugador", "Goles"])
    df_goleadores = df_goleadores.sort_values(by="Goles", ascending=True) # Orden ascendente para el gráfico horizontal

    # Gráfico de barras horizontales (Top Goleadores)
    fig_top = px.bar(
        df_goleadores, 
        x="Goles", 
        y="Jugador",
        orientation='h', # Horizontal para que se lean bien los nombres
        text="Goles",
        title="Top 10: Máximos Goleadores Históricos de Argentina",
        color="Goles",
        color_continuous_scale=["#1e3a5f", "#75AADB", "#ffffff"]
    )
    
    fig_top.update_traces(textposition='outside', textfont_size=14, textfont_color="#ffffff")
    fig_top.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ffffff", 
        coloraxis_showscale=False,
        title_font_size=20,
        height=500
    )
    st.plotly_chart(fig_top, width="stretch")
    
    st.markdown("---")
    st.subheader("🏅Top 3 Goleadores")
    
    # Mostramos el Top 3 destacado
    col1, col2, col3 = st.columns(3)
    col1.metric("🥇 Máximo Goleador", "Lionel Messi", "21 Goles")
    col2.metric("🥈 Segundo", "Gabriel Batistuta", "10 Goles")
    col3.metric("🥉 Tercero", "Diego Maradona", "8 Goles")

# --- PESTAÑA 3: PARTIDOS ---
with tab3:
    st.header("📊 Explorador de Partidos Históricos")
    
    años_disponibles = sorted(partidos["Year"].unique(), reverse=True)
    año_seleccionado = st.selectbox("🗓️ Seleccioná un Mundial:", años_disponibles)
    
    df_filtrado = partidos[partidos["Year"] == año_seleccionado].copy()
    
    # Validación de fecha
    if not pd.api.types.is_datetime64_any_dtype(df_filtrado["Date"]):
        df_filtrado["Date"] = pd.to_datetime(df_filtrado["Date"], errors="coerce")
    
    df_filtrado["Fecha_Str"] = df_filtrado["Date"].dt.strftime('%d/%m/%Y').fillna("Sin fecha")
    
    # KPIs del mundial seleccionado
    victorias = (df_filtrado["Resultado"] == "Victoria").sum()
    empates = (df_filtrado["Resultado"] == "Empate").sum()
    derrotas = (df_filtrado["Resultado"] == "Derrota").sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Victorias", int(victorias))
    col2.metric("➖ Empates", int(empates))
    col3.metric("❌ Derrotas", int(derrotas))
    
    st.markdown("---")
    
    tabla = df_filtrado[["Fecha_Str", "Rival", "Goles_Arg", "Goles_Rival", "Resultado", "Round"]].rename(
        columns={"Fecha_Str": "Fecha", "Goles_Arg": "GF", "Goles_Rival": "GC", "Round": "Fase"}
    ).reset_index(drop=True)

    # Tabla armada con columnas: el botón vive dentro de la celda "Resultado"
    # y solo aparece en los partidos que tienen imagen asignada
    anchos = [1.2, 1.6, 0.6, 0.6, 1.4, 2.0]
    linea = "<hr style='margin:4px 0; border:none; border-top:1px solid rgba(117,170,219,0.35);'>"

    for col, nombre in zip(st.columns(anchos), ["Fecha", "Rival", "GF", "GC", "Resultado", "Fase"]):
        col.markdown(f"**{nombre}**")
    st.markdown(linea, unsafe_allow_html=True)

    for _, fila in tabla.iterrows():
        c = st.columns(anchos, vertical_alignment="center")
        c[0].write(fila["Fecha"])
        c[1].write(fila["Rival"])
        c[2].write(int(fila["GF"]))
        c[3].write(int(fila["GC"]))

        ruta = IMAGENES_PARTIDOS.get((int(año_seleccionado), fila["Rival"]))
        if ruta:
            if c[4].button(f"📸 {fila['Resultado']}", key=f"img_{año_seleccionado}_{fila['Rival']}"):
                mostrar_imagen(ruta, f"Argentina {fila['GF']} - {fila['GC']} {fila['Rival']}")
        else:
            c[4].write(fila["Resultado"])

        c[5].write(fila["Fase"])
        st.markdown(linea, unsafe_allow_html=True)
    
    # Gráfico de resultados
    fig_res = px.pie(
        df_filtrado, names="Resultado",
        title=f"Distribución de Resultados en {año_seleccionado}",
        color="Resultado",
        color_discrete_map={"Victoria": "#75AADB", "Derrota": "#ff4b4b", "Empate": "#A5C8E8"},
        hole=0.5
    )
    fig_res.update_traces(textfont_size=14, textposition='outside')
    fig_res.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", font_color="#ffffff",
        title_font_size=18
    )
    st.plotly_chart(fig_res, width="stretch")

# --- FOOTER ---
st.markdown("---")
st.markdown(
    '<p style="text-align:center; color:#75AADB; opacity:0.7;">🇦🇷 Proyecto de Análisis y Exploración de Datos — Selección Argentina en los Mundiales</p>',
    unsafe_allow_html=True
)
