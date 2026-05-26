import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# 1. SILENCIAR ADVERTENCIAS DE VERSIONES (Terminal Limpia)
warnings.filterwarnings("ignore")

# 2. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Spotify Strategic Analytics 2025", layout="wide")

# 3. CARGA DE DATOS OPTIMIZADA
@st.cache_data
def load_data():
    # Asegúrate de que el archivo 'spotify_light.parquet' esté en la misma carpeta
    df = pd.read_parquet("spotify_light.parquet")
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error crítico al cargar la base de datos: {e}")
    st.stop()

# 4. ESTILOS CSS PERSONALIZADOS (Blanco puro y Buscador de Impacto)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    
    /* Métricas con borde verde y texto blanco */
    [data-testid="stMetric"] {
        background-color: #1e2129;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #1DB954;
    }
    [data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; opacity: 1; }

    /* Buscador con estilo Spotify */
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

# 5. BARRA LATERAL (Sidebar)
st.sidebar.image("https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_CMYK_Green.png", width=200)
st.sidebar.markdown("---")
st.sidebar.info("""
**Equipo:**
* **Carlos Hidalgo**
* **Salvador Garcia**
* **Sergio Bárcena**
""")
st.sidebar.write("**Proyecto:** Humanidades Digitales")
st.sidebar.write("**Fecha:** Mayo 2026")

# --- SECCIÓN 1: INTRODUCCIÓN ---
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
    st.success(f"""
    **Estatus del Ecosistema:**
    * **Muestra:** Optimizada para Análisis Estratégico
    * **Arquitectura:** Parquet High-Performance
    * **Contexto:** Julio 2025
    """)

st.divider()

# --- SECCIÓN 2: INDICADORES CLAVE ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Pistas Analizadas", f"{len(df):,}")
with col2:
    st.metric("Popularidad Promedio", f"{df['track_popularity'].mean():.2f} pts")
with col3:
    st.metric("% Contenido Explícito", f"{(df['explicit'].mean() * 100):.2f}%")

st.divider()

# --- SECCIÓN 3: GÉNEROS DOMINANTES ---
st.header("Análisis de Géneros Dominantes")
top_generos_data = df.groupby('artist_genres')['track_popularity'].mean().sort_values(ascending=False).head(10)
top_generos_data.index = [g[:30] + '...' if len(str(g)) > 30 else g for g in top_generos_data.index]

fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(x=top_generos_data.values, y=top_generos_data.index, color="#1DB954", ax=ax1)
ax1.set_title("Top 10 Géneros por Impacto Acumulado (Promedio)", fontsize=16, fontweight='bold', color='white')
ax1.tick_params(colors='white')
fig1.patch.set_facecolor('#0e1117')
ax1.set_facecolor('#0e1117')
st.pyplot(fig1)

st.markdown("### Dominio del Mercado")
st.write("""
El gráfico revela un liderazgo claro de los géneros urbanos y regionales. Es notable cómo el **West Coast Hip Hop** mantiene la hegemonía comercial, seguido de cerca por movimientos culturales como el **Afropop** y el **Urbano Latino**.

**Interpretación Estratégica:** La inversión en mercados emergentes está rindiendo frutos. Esto demuestra que Spotify "abre la puerta" a ritmos globales que cumplen con estándares de producción optimizados para el streaming.
""")

st.divider()

# --- SECCIÓN 4: ÉTICA Y CUMPLIMIENTO ---
st.header("Gobernanza de Contenido: ¿Filtro o Bloqueo?")
col_eth1, col_eth2 = st.columns([1, 2])

with col_eth1:
    st.subheader("Ética y Cumplimiento")
    st.write("""
    Spotify utiliza la etiqueta de **Contenido Explícito** como uno de sus principales mecanismos de control. 
    Este filtro puede actuar como una barrera de entrada para ciertas playlists comerciales, limitando la "luz verde" para artistas con líricas transgresoras.
    
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

# --- SECCIÓN 5: ADN DEL ÉXITO (HEATMAP) ---
st.header("El ADN del Éxito Musical")

with st.expander("Diccionario de Atributos (Glosario)"):
    st.write("""
    * **Danceability:** Estabilidad del ritmo y fuerza del pulso.
    * **Energy:** Intensidad y actividad perceptiva.
    * **Valence:** Positividad (Alta = Alegre / Baja = Triste).
    * **Popularity:** Éxito basado en reproducciones recientes.
    """)

col_graf1, col_txt1 = st.columns([2.5, 1])
with col_graf1:
    cols_analisis = ['track_popularity', 'danceability', 'energy', 'valence', 'tempo']
    corr = df[cols_analisis].corr()
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='RdYlGn', center=0, ax=ax4)
    fig4.patch.set_alpha(0) # Elimina recuadro negro
    ax4.set_facecolor("none")
    plt.xticks(rotation=45, color='white')
    plt.yticks(color='white')
    st.pyplot(fig4)

with col_txt1:
    st.subheader("¿Qué hace a un Hit?")
    st.write("""
    **Interpretación Estratégica:**
    * **La Dictadura del Ritmo:** La alta correlación entre **Energy** y **Popularity** sugiere que el algoritmo favorece ritmos intensos.
    * **Bailabilidad:** Si la música no induce al movimiento, el sistema de recomendación podría estar limitando el alcance orgánico.
    * **Neutralidad del Sentimiento:** El éxito no depende de si la canción es alegre o triste (*Valence*), sino de su energía.
    """)

st.divider()

# --- SECCIÓN 6: AUDITORÍA (BUSCADOR DESTACADO) ---
st.header("Auditoría de Mercado e Inteligencia")
st.write("""
**Análisis de Interacción:** Utiliza esta herramienta para profundizar en artistas específicos y validar cómo el algoritmo los posiciona. 
Aquí es donde comprobamos si la plataforma **da entrada o bloquea** a un exponente específico basándose en su data.
""")

busqueda = st.text_input("Ingresa el nombre de un artista o canción para auditar su desempeño:", placeholder="Ej. Peso Pluma, Bad Bunny, Queen...")

if busqueda:
    resultados = df[df['artist_name'].str.contains(busqueda, case=False, na=False) | 
                    df['track_name'].str.contains(busqueda, case=False, na=False)]
    if not resultados.empty:
        st.success(f"Se detectaron {len(resultados)} registros:")
        st.dataframe(resultados[['artist_name', 'track_name', 'track_popularity', 'artist_genres']], width=None)
    else:
        st.error(f"El artista o canción '{busqueda}' no figura en la muestra auditada.")

st.divider()

# --- SECCIÓN 7: LÍDERES DE AUDIENCIA ---
st.header("Oligopolio Creativo: Líderes de Audiencia")
c_art1, c_art2 = st.columns([1, 2])

with c_art1:
    st.write("""
    **Concentración de Éxito:** En la industria de 2025, el éxito no es democrático. 
    Existe un efecto donde los 15 artistas principales absorben la mayoría de la tracción. 
    
    Esto confirma un mercado de **Oligopolio Creativo**, donde la entrada de nuevos talentos está estrictamente filtrada por los patrones que el algoritmo premia.
    """)

with c_art2:
    # Usamos PROMEDIO para ver quién tiene el nivel de éxito más alto por canción
    top_artistas = df.groupby('artist_name')['track_popularity'].mean().sort_values(ascending=False).head(15)
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_artistas.values, y=top_artistas.index, hue=top_artistas.index, palette="flare", legend=False, ax=ax6)
    ax6.set_title("Top 15 Artistas por Popularidad Promedio", color='white')
    ax6.tick_params(colors='white')
    fig6.patch.set_facecolor('#0e1117')
    ax6.set_facecolor('#0e1117')
    # Etiquetas de valor en las barras
    for i, v in enumerate(top_artistas.values):
        ax6.text(v + 1, i, f'{v:.1f}', color='white', va='center', fontweight='bold')
    st.pyplot(fig6)

st.divider()

# --- SECCIÓN 8: CONCLUSIONES ---
st.header("Conclusiones y Recomendaciones Estratégicas")
c_final1, c_final2 = st.columns(2)

with c_final1:
    st.info("### Hallazgos de Gobernanza")
    st.markdown("""
    1. **Estandarización:** Spotify premia la *Energy* y *Danceability*, creando un molde técnico para el éxito.
    2. **Filtros Éticos:** La paridad entre contenido 'Clean' y 'Explicit' muestra una segmentación por nichos, no moral.
    3. **Hegemonía 2025:** El Urbano Latino y el Regional dominan la fotografía actual del consumo global.
    """)

with c_final2:
    st.success("### Recomendación Consultiva")
    st.markdown("""
    * **Para Sellos:** Priorizar el cumplimiento del "ADN del Hit" (Alta Energía) para asegurar la entrada a playlists.
    * **Para el Análisis:** Monitorear cómo el algoritmo "bloquea" géneros que se alejan de estos patrones rítmicos.
    """)

st.markdown("---")
st.caption("Dashboard Estratégico | Humanidades Digitales 2026")