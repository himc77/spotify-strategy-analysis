import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Configuración de la página (Modo Ancho y Título en la pestaña)
st.set_page_config(page_title="Spotify Insights 2025", layout="wide")

# 2. Carga de datos con "Cache" para que sea veloz
@st.cache_data
def load_data():
    df = pd.read_parquet("spotify_master_final.parquet", engine='fastparquet')
    return df

df = load_data()

# --- DISEÑO DE LA PÁGINA ---

# Encabezado Principal con estilo
st.title("🎵 Análisis Estratégico de la Industria Musical")
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
    
    *Insight para el Consejo:* La inversión en mercados emergentes está rindiendo 
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

# Pie de página
st.markdown("---")
st.caption("Dashboard desarrollado por Carlos Hidalgo, Salvador Garcia y Sergio Bárcena  | Humanidades Digitales")

