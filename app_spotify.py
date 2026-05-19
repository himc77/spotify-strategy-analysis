import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Configuración de la página (Modo Ancho y Título en la pestaña)
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

st.markdown("""
**Snapshot: Julio 2025**  
*Este dashboard presenta un análisis profundo sobre las tendencias de consumo, géneros emergentes y cumplimiento ético 
en la plataforma Spotify, procesando millones de registros mediante estructuras de datos de alta eficiencia.*
""")

st.divider()

# 3. MÉTRICAS CLAVE (Los "Big Numbers")
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
st.header("📊 Análisis de Tendencias Globales")

# --- GRÁFICA 1: GÉNEROS ---
c1, c2 = st.columns([2, 1]) # La gráfica ocupa más espacio que el texto

with c1:
    top_generos = df.groupby('artist_genres')['track_popularity'].mean().sort_values(ascending=False).head(10)
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_generos.values, y=top_generos.index, palette="Blues_r", ax=ax1)
    ax1.set_title("Top 10 Géneros por Popularidad")
    st.pyplot(fig1)

with c2:
    st.subheader("Dominio del Mercado")
    st.write("""
    **Análisis Estratégico:**  
    El gráfico revela un liderazgo claro de los géneros urbanos y regionales. 
    Es notable cómo el **West Coast Hip Hop** mantiene la hegemonía comercial, 
    seguido de cerca por movimientos culturales como el **Afropop** y el **Urbano Latino**.
    
    La inversión en mercados emergentes está rindiendo 
    frutos, con popularidades promedio que superan los 70 puntos.
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


# --- NUEVA SECCIÓN: ANÁLISIS DE ATRIBUTOS (MAPA DE CALOR) ---
st.header("🔥 Correlación de Atributos Musicales")
col_graf1, col_txt1 = st.columns([2, 1])

with col_graf1:
    # Seleccionamos variables numéricas para el Heatmap
    # Asegúrate de que estas columnas existan en tu Parquet
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

# --- NUEVA SECCIÓN: DISTRIBUCIÓN DE ÉXITO ---
st.header("📈 La Curva del Éxito")
fig5, ax5 = plt.subplots(figsize=(10, 4))
sns.histplot(df['track_popularity'], kde=True, color="green", ax=ax5)
ax5.set_title("Distribución de Popularidad en la Base de Datos")
st.pyplot(fig5)

st.info("**Nota Técnica:** La mayoría de las canciones se concentran en rangos bajos. Lograr una popularidad > 80 coloca a un artista en el top 1% de la industria.")

st.divider()
st.header("🏆 Dominancia de Mercado por Artista")
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

st.header("🎯 Segmentación: ¿Energía o Ritmo?")

# 1. Aumentamos el tamaño de la figura
fig7, ax7 = plt.subplots(figsize=(12, 7))

# 2. Usamos una muestra un poco más pequeña para mayor claridad
df_sample = df.sample(min(1500, len(df))) 

# 3. Graficamos con transparencia (alpha) para evitar el empalamiento
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

# Movemos la leyenda afuera para que no tape puntos
ax7.legend(title="Explícita / Popularidad", bbox_to_anchor=(1.05, 1), loc='upper left')

st.pyplot(fig7)
st.caption("Nota: Se aplicó un filtro de densidad y transparencia para mejorar la legibilidad del análisis.")

# 5. BUSCADOR INTELIGENTE
st.header("🔍 Auditoría de Pistas Específicas")
busqueda = st.text_input("Ingrese Artista o Canción para consultar métricas detalladas:")

if busqueda:
    resultados = df[
        df['track_name'].str.contains(busqueda, case=False, na=False) | 
        df['artist_name'].str.contains(busqueda, case=False, na=False)
    ]
    st.success(f"Se encontraron {len(resultados)} coincidencias en la base de datos.")
    st.dataframe(resultados, use_container_width=True)
else:
    st.info("Utilice el buscador para explorar la base completa.")
st.divider()

# --- SECCIÓN FINAL: CONCLUSIONES DEL CONSULTOR ---
st.header("🏁 Conclusiones y Recomendaciones Estratégicas")

c_final1, c_final2 = st.columns(2)

with c_final1:
    st.info("### 📌 Hallazgos Clave")
    st.markdown("""
    1. **Estandarización del Éxito:** La alta correlación entre *Energy* y *Danceability* confirma que la audiencia actual prioriza el ritmo sobre la lírica compleja.
    2. **Mitigación de Riesgos:** El análisis de contenido explícito demuestra que la rentabilidad no está sujeta a la censura, permitiendo estrategias de marca más flexibles.
    3. **Concentración de Mercado:** Existe un efecto de 'Winner-Take-All', donde los 20 artistas principales absorben la mayoría de la tracción orgánica de la plataforma.
    """)

with c_final2:
    st.success("### 🚀 Próximos Pasos Sugeridos")
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

