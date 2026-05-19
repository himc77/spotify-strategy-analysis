import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Configuración de la página 
st.set_page_config(page_title="Spotify Insights 2025", layout="wide")

# 2. Carga de datos con "Cache" para que sea veloz
@st.cache_data
def load_data():
    df = pd.read_parquet("spotify_light.parquet")
    return df

df = load_data()

# --- DISEÑO DE LA PÁGINA ---

# --- CONFIGURACIÓN DE LA BARRA LATERAL (SIDEBAR) ---
st.sidebar.image("https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_CMYK_Green.png", width=200)
st.sidebar.markdown("---")
st.sidebar.info("""
**Analistas Senior:**
* 👤 **Carlos Hidalgo**
* 👤 **Salvador Garcia**
* 👤 **Sergio Bárcena**
""")

st.sidebar.markdown("---")
st.sidebar.write("🎓 **Proyecto:** Humanidades Digitales")
st.sidebar.write("📅 **Fecha:** Mayo 2026")

# --- ENCABEZADO ---
st.set_page_config(page_title="Spotify Strategic Analytics", layout="wide")

st.title(" Spotify Market Intelligence Dashboard")
st.markdown(f"**Strategic Insight Engine**")


col_header1, col_header2 = st.columns([2, 1])

with col_header1:
    st.write("""
    ### Transformando Datos en Decisiones Musicales
    Este ecosistema analítico procesa millones de registros, que al final quedaron en miles para poder hacerlo público y rápido. Lo que sigue fue lograr identificar los **patrones de éxito** que definen la industria actual. 
    A través de minería de datos avanzada, exploramos la intersección entre la creatividad artística y la viabilidad comercial.
    """)

with col_header2:
    st.success(f"""
    **Estatus del Sistema:**
    *  **Corte:** Mayo 2026
    *  **Volumen:** Miles de Datapoints
    * **Arquitectura:** Parquet Optimized
    """)

st.divider()

# 3. MÉTRICAS CLAVE 
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Volumen de Datos", f"{len(df):,} pistas")
with col2:
    pop_avg = df['track_popularity'].mean()
    st.metric("Popularidad Promedio", f"{pop_avg:.2f} pts")
with col3:
    explicitas = (df['explicit'].mean() * 100)
    st.metric("% Contenido Explícito", f"{explicitas:.2f}%")

st.divider()

# 4. SECCIÓN DE GRÁFICAS CON EXPLICACIÓN

# --- GRÁFICA 1: GÉNEROS ---
c1, c2 = st.columns([2, 1]) # La gráfica ocupa más espacio que el texto

with c1:
    top_generos = df.groupby('artist_genres')['track_popularity'].mean().sort_values(ascending=False).head(10)

# --- GRÁFICA 1: TOP GÉNEROS  ---
st.header("Análisis de Géneros Dominantes")

# 1. Calculamos los datos
top_generos_data = df.groupby('artist_genres')['track_popularity'].mean().sort_values(ascending=False).head(10)
top_generos_data.index = [g[:30] + '...' if len(str(g)) > 30 else g for g in top_generos_data.index]

# 2. La gráfica solita 
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(x=top_generos_data.values, y=top_generos_data.index, color="#1DB954", ax=ax1)

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_title("Top 10 Géneros por Impacto Acumulado", fontsize=16, fontweight='bold')
plt.subplots_adjust(left=0.3) 

st.pyplot(fig1)

# 3. EL TEXTO 
st.markdown("### Dominio del Mercado")
st.write("""
El gráfico revela un liderazgo claro de los géneros urbanos y regionales. Es notable cómo el **West Coast Hip Hop** mantiene la hegemonía comercial, seguido de cerca por movimientos culturales como el **Afropop** y el **Urbano Latino**.

La inversión en mercados emergentes está rindiendo frutos, con popularidades promedio que superan los **70 puntos**.
""")

st.divider()

# --- GRÁFICA 2: EXPLÍCITO ---
c3, c4 = st.columns([1, 2])

with c3:
    st.subheader("Ética y Consumo")
    st.write("""
    **Análisis de Cumplimiento (Compliance):**  
    Uno de los hallazgos más relevantes es la paridad en el éxito comercial 
    independientemente de la etiqueta de contenido.
    
    **Conclusión:**  
    El contenido "Clean" (limpio) es igual de rentable que el "Explicit". 
    Esto permite a las marcas colaborar con artistas sin comprometer sus 
    políticas de responsabilidad social o integridad de marca.
    """)

with c4:
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.barplot(x='explicit', y='track_popularity', data=df, palette='viridis', ax=ax2)
    ax2.set_title("Popularidad: Contenido Limpio vs Explícito")
    ax2.set_xticklabels(['Limpia (Clean)', 'Explícita (Explicit)'])
    st.pyplot(fig2)

st.divider()


# --- ANÁLISIS DE ATRIBUTOS (MAPA DE CALOR) ---
st.header(" Correlación de Atributos Musicales")
col_graf1, col_txt1 = st.columns([2, 1])

with col_graf1:
    # variables numéricas para el Heatmap
    cols_analisis = ['track_popularity', 'danceability', 'energy', 'valence', 'tempo']
    corr = df[cols_analisis].corr()
    
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr, annot=True, cmap='RdYlGn', center=0, ax=ax4)
    st.pyplot(fig4)

with col_txt1:
    st.subheader("¿Qué hace a un Hit?")
    st.write("""
    **Interpretación Estratégica:** Este mapa de calor muestra la relación entre las características técnicas de la música. 
    * Una correlación alta (cercana a 1) entre **Energy** y **Popularity** sugiere que el mercado actual demanda ritmos intensos.
    * Si el **Valence** (felicidad) es bajo pero la popularidad alta, estamos ante una tendencia de música melancólica o "lo-fi".
    """)

st.divider()

# --- DISTRIBUCIÓN DE ÉXITO ---
st.header(" La Curva del Éxito")
fig5, ax5 = plt.subplots(figsize=(10, 4))
sns.histplot(df['track_popularity'], kde=True, color="green", ax=ax5)
ax5.set_title("Distribución de Popularidad en la Base de Datos")
st.pyplot(fig5)

st.info("**Nota Técnica:** La mayoría de las canciones se concentran en rangos bajos. Lograr una popularidad > 80 coloca a un artista en el top 1% de la industria.")

st.divider()
st.header(" Dominancia de Mercado por Artista")
c7, c8 = st.columns([1, 2])

with c7:
    st.write("""
    **Concentración de Éxito:** En la industria musical, el éxito no se reparte equitativamente. Esta gráfica identifica a los 'Market Leaders'.
    
    *Insight:* Si un puñado de artistas domina más del 20% de la popularidad total, estamos ante un mercado de **Oligopolio Creativo**.
    """)

with c8:
    top_artistas = df.groupby('artist_name')['track_popularity'].sum().sort_values(ascending=False).head(20)
    fig6, ax6 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_artistas.values, y=top_artistas.index, palette="flare", ax=ax6)
    ax6.set_title("Top 20 Artistas por Impacto Acumulado")
    st.pyplot(fig6)

    st.divider()

st.header(" Segmentación: ¿Energía o Ritmo?")

fig7, ax7 = plt.subplots(figsize=(12, 7))


df_sample = df.sample(min(1500, len(df))) 


sns.scatterplot(
    data=df_sample, 
    x='danceability', 
    y='energy', 
    hue='explicit', 
    size='track_popularity', 
    palette='viridis', 
    alpha=0.5, # Puntos semi-transparentes
    edgecolor=None, # Quita el borde blanco de los puntos para que no se vean encimados
    ax=ax7
)

ax7.xaxis.set_major_locator(plt.MaxNLocator(10)) 
ax7.yaxis.set_major_locator(plt.MaxNLocator(10))

ax7.set_title("Relación entre Energía y Bailabilidad (Muestra Optimizada)")
ax7.set_xlabel("Bailabilidad (Danceability)")
ax7.set_ylabel("Energía (Energy)")


ax7.legend(title="Explícita / Popularidad", bbox_to_anchor=(1.05, 1), loc='upper left')

st.pyplot(fig7)
st.caption("Nota: Se aplicó un filtro de densidad y transparencia para mejorar la legibilidad del análisis.")

# 5. BUSCADOR INTELIGENTE
st.divider()
st.subheader("Buscador de Canciones e Intérpretes")

# 1. Entrada de texto del usuario
busqueda = st.text_input("Escribe el nombre del artista o canción:", "")

if busqueda:
    # 2. Filtramos ignorando mayúsculas/minúsculas y buscando coincidencias parciales
    # Esto buscará "Peso Pluma" aunque escribas solo "pluma" o "PESO"
    resultados = df[
        df['artist_name'].str.contains(busqueda, case=False, na=False) | 
        df['track_name'].str.contains(busqueda, case=False, na=False)
    ]
    
    if not resultados.empty:
        st.write(f"Se encontraron {len(resultados)} coincidencias:")
        # Mostramos las columnas principales
        st.dataframe(resultados[['artist_name', 'track_name', 'track_popularity', 'artist_genres']])
    else:
        st.warning(f"No se encontraron resultados para: '{busqueda}'")
else:
    st.info("Ingresa un término para comenzar la búsqueda.")

# --- CONCLUSIONES DEL CONSULTOR ---
st.header("Conclusiones y Recomendaciones Estratégicas")

c_final1, c_final2 = st.columns(2)

with c_final1:
    st.info("### Hallazgos Clave")
    st.markdown("""
    1. **Estandarización del Éxito:** La alta correlación entre *Energy* y *Danceability* confirma que la audiencia actual prioriza el ritmo sobre la lírica compleja.
    2. **Mitigación de Riesgos:** El análisis de contenido explícito demuestra que la rentabilidad no está sujeta a la censura, permitiendo estrategias de marca más flexibles.
    3. **Concentración de Mercado:** Existe un efecto de 'Winner-Take-All', donde los 20 artistas principales absorben la mayoría de la tracción orgánica de la plataforma.
    """)

with c_final2:
    st.success("### Próximos Pasos Sugeridos")
    st.markdown("""
    * **Optimización de Portafolio:** Priorizar artistas con un 'Valence' superior a 0.5 para campañas de verano.
    * **Expansión de Datos:** Integrar datos de redes sociales (TikTok/IG) para predecir picos de popularidad antes de que ocurran en Spotify.
    * **Gobernanza:** Mantener la arquitectura en **Parquet** para asegurar que el crecimiento de la base de datos no comprometa la velocidad de respuesta del negocio.
    """)

# Pie de página final
st.markdown("---")
st.markdown("<center><b>Este reporte fue generado automáticamente mediante una infraestructura de Ciencia de Datos escalable.</b></center>", unsafe_allow_html=True)
# Pie de página
st.markdown("---")
st.caption("Dashboard desarrollado por Carlos Hidalgo, Salvador Garcia y Sergio Bárcena  | Humanidades Digitales")

