import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Ignorar avisos de versiones en la terminal
warnings.filterwarnings("ignore")

# 1. Configuración de la página
st.set_page_config(page_title="Spotify Strategic Analytics 2025", layout="wide")

# 2. Carga de datos con "Cache"
@st.cache_data
def load_data():
    df = pd.read_parquet("spotify_light.parquet")
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error al cargar la base de datos: {e}")
    st.stop()

# --- ESTILOS PERSONALIZADOS (MODO BLANCO Y BUSCADOR) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetric"] {
        background-color: #1e2129;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #1DB954;
    }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; opacity: 1; }
    
    /* Buscador verde */
    div[data-testid="stTextInput"] > div > div > input {
        background-color: #262730;
        color: #1DB954; 
        border: 2px solid #1DB954;
        font-size: 20px;
        height: 60px;
    }
    div[data-testid="stTextInput"] label {
        color: #FFFFFF !important;
        font-size: 1.2rem !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image("https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_CMYK_Green.png", width=200)
st.sidebar.markdown("---")
st.sidebar.info("""
**Analistas Senior (Maestría):**
* 👤 **Carlos Hidalgo**
* 👤 **Salvador Garcia**
* 👤 **Sergio Bárcena**
""")
st.sidebar.write("**Proyecto:** Humanidades Digitales")
st.sidebar.write("**Fecha:** Mayo 2026")

# --- BLOQUE 1: INTRODUCCIÓN Y CONTEXTO ---
st.title("Market Intelligence: El Ecosistema Spotify 2025")

st.markdown(f"""
> **Nota Metodológica:** Esta base de datos representa una **fotografía del ecosistema de Spotify capturada en julio de 2025**. 
> Las medidas de popularidad reflejan el estado de circulación y visibilidad observable en ese momento específico.
""")

col_intro1, col_intro2 = st.columns([2, 1])
with col_intro1:
    st.write("""
    ### El Algoritmo como Curador Global
    En esta investigación exploramos cómo Spotify mide el éxito y por qué la plataforma, en su rol de curadora, 
    **bloquea o da entrada** a ciertos artistas y géneros. No estamos ante un mercado neutral, sino ante un 
    sistema de gobernanza algorítmica que moldea el consumo cultural global.
    
    A través de esta narrativa de datos, identificamos los **patrones de éxito** y las barreras de entrada 
    que definen la industria musical contemporánea.
    """)
with col_intro2:
    st.success(f"**Estatus:** Corte Temporal Julio 2025 | Muestra Optimizada")

st.divider()

# --- MÉTRICAS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Pistas Analizadas", f"{len(df):,}")
with col2:
    pop_avg = df['track_popularity'].mean()
    st.metric("Popularidad Promedio", f"{pop_avg:.2f} pts")
with col3:
    explicitas = (df['explicit'].mean() * 100)
    st.metric("% Contenido Explícito", f"{explicitas:.2f}%")

st.divider()

# --- GRÁFICA 1: GÉNEROS CON TEXTO ---
st.header("Análisis de Géneros Dominantes")
top_generos_data = df.groupby('artist_genres')['track_popularity'].mean().sort_values(ascending=False).head(10)
top_generos_data.index = [g[:30] + '...' if len(str(g)) > 30 else g for g in top_generos_data.index]

fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(x=top_generos_data.values, y=top_generos_data.index, color="#1DB954", ax=ax1)
ax1.set_title("Top 10 Géneros por Impacto Acumulado", color='white', fontsize=16)
ax1.tick_params(colors='white')
fig1.patch.set_facecolor('#0e1117')
ax1.set_facecolor('#0e1117')
st.pyplot(fig1)

st.markdown("### Dominio del Mercado")
st.write("""
El gráfico revela un liderazgo claro de los géneros urbanos y regionales. Es notable cómo el **West Coast Hip Hop** mantiene la hegemonía comercial, seguido de cerca por movimientos culturales como el **Afropop** y el **Urbano Latino**.

**Interpretación Estratégica:** La inversión en mercados emergentes está rindiendo frutos, con popularidades 
promedio que superan los **70 puntos**. Esto demuestra que Spotify "abre la puerta" a ritmos globales que 
cumplen con estándares de producción optimizados para el streaming.
""")

st.divider()

# --- GRÁFICA 2: ÉTICA Y CUMPLIMIENTO CON TEXTO ---
st.header("Gobernanza de Contenido: ¿Filtro o Bloqueo?")
col_eth1, col_eth2 = st.columns([1, 2])

with col_eth1:
    st.subheader("Ética y Cumplimiento")
    st.write("""
    Spotify utiliza la etiqueta de **Contenido Explícito** como uno de sus principales mecanismos de control. 
    Este filtro puede actuar como una barrera de entrada para ciertas playlists comerciales o 
    familiares, limitando la "luz verde" para artistas con líricas transgresoras.
    
    Sin embargo, nuestro análisis de **Compliance** revela que la rentabilidad es paritaria: 
    el contenido "Clean" es tan capaz de generar tracción masiva como el "Explicit".
    """)

with col_eth2:
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.barplot(x='explicit', y='track_popularity', data=df, hue='explicit', palette='viridis', legend=False, ax=ax2)
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(['Limpia (Clean)', 'Explícita (Explicit)'], color='white')
    ax2.tick_params(colors='white')
    fig2.patch.set_facecolor('#0e1117')
    ax2.set_facecolor('#0e1117')
    st.pyplot(fig2)

st.divider()

# --- GRÁFICA 3: HEATMAP CON TEXTO ---
st.header("El ADN del Éxito Musical")
col_graf1, col_txt1 = st.columns([2.5, 1])

with col_graf1:
    cols_analisis = ['track_popularity', 'danceability', 'energy', 'valence', 'tempo']
    corr = df[cols_analisis].corr()
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='RdYlGn', center=0, ax=ax4)
    fig4.patch.set_alpha(0) 
    ax4.set_facecolor("none")
    plt.xticks(rotation=45, color='white')
    plt.yticks(color='white')
    st.pyplot(fig4)

with col_txt1:
    st.subheader("¿Qué hace a un Hit?")
    st.write("""
    **Interpretación Estratégica:**
    * Una correlación alta entre **Energy** y **Popularity** sugiere que el mercado demanda ritmos intensos.
    * Si el **Valence** (felicidad) es bajo pero la popularidad alta, estamos ante una tendencia de música melancólica.
    * Spotify mide la "bailabilidad"; si una canción no induce al movimiento, el sistema de recomendación podría estar limitando su alcance.
    """)

st.divider()

# --- BLOQUE 4: BUSCADOR DESTACADO ---
st.header("🔍 Auditoría de Mercado e Inteligencia")
st.markdown("### Explora tu propio Segmento de Mercado")
st.write("Utiliza esta herramienta para profundizar en artistas específicos y validar cómo el algoritmo los posiciona.")

busqueda = st.text_input("Ingresa el nombre de un artista o canción:", placeholder="Ej. Peso Pluma, Bad Bunny...")

if busqueda:
    resultados = df[df['artist_name'].str.contains(busqueda, case=False, na=False) | 
                    df['track_name'].str.contains(busqueda, case=False, na=False)]
    if not resultados.empty:
        st.success(f"Se detectaron {len(resultados)} registros:")
        st.dataframe(resultados[['artist_name', 'track_name', 'track_popularity', 'artist_genres']], width=None)
    else:
        st.error(f"El artista o canción '{busqueda}' no se encuentra en la muestra de julio 2025.")

st.divider()

# --- GRÁFICA 4: LÍDERES CON TEXTO ---
st.header("Oligopolio Creativo: Líderes de Audiencia")
c_art1, c_art2 = st.columns([1, 2])

with c_art1:
    st.write("""
    **Concentración de Éxito:** En la industria musical de 2025, el éxito no es democrático.
    Existe un efecto donde los pocos artistas con mayor inversión y visibilidad concentran la audiencia.
    """)

with c_art2:
    top_artistas = (
        df.groupby('artist_name')['track_popularity']
          .mean()
          .sort_values(ascending=False)
          .head(10)
    )
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_artistas.values, y=top_artistas.index, color="#1DB954", ax=ax5)
    ax5.set_title("Top 10 Artistas por Popularidad Promedio", color='white', fontsize=16)
    ax5.tick_params(colors='white')
    fig5.patch.set_facecolor('#0e1117')
    ax5.set_facecolor('#0e1117')
    st.pyplot(fig5)
