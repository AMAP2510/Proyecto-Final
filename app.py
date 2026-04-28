import streamlit as st
import joblib
import numpy as np

# ─────────────────────────────────────────────
# Configuración de la página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Predictor de Tasa de Víctimas",
    page_icon="🕊️",
    layout="centered"
)

# ─────────────────────────────────────────────
# Estilos personalizados
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
}

/* Fondo general */
.stApp {
    background-color: #F5F0EB;
}

/* Título principal */
.titulo-principal {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    color: #1C1C1C;
    line-height: 1.2;
    margin-bottom: 0.2rem;
}

.subtitulo {
    font-size: 1rem;
    color: #6B6B6B;
    margin-bottom: 2rem;
    font-weight: 300;
}

/* Tarjeta de inputs */
.card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    margin-bottom: 1.5rem;
}

/* Resultado */
.resultado-box {
    background: #1C1C1C;
    color: #F5F0EB;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-top: 1.5rem;
}

.resultado-numero {
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    color: #E8C547;
    line-height: 1;
}

.resultado-label {
    font-size: 0.95rem;
    color: #AAAAAA;
    margin-top: 0.4rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.resultado-interpretacion {
    font-size: 1rem;
    color: #DDDDDD;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #333;
}

/* Advertencia / info */
.info-box {
    background: #FFF8E7;
    border-left: 4px solid #E8C547;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-size: 0.9rem;
    color: #555;
    margin-top: 1rem;
}

/* Error */
.error-box {
    background: #FFF0F0;
    border-left: 4px solid #E05252;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-size: 0.9rem;
    color: #C0392B;
    margin-top: 1rem;
}

/* Ocultar elementos de Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Botón */
.stButton > button {
    background-color: #1C1C1C;
    color: #F5F0EB;
    border: none;
    border-radius: 10px;
    padding: 0.75rem 2rem;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    width: 100%;
    cursor: pointer;
    transition: background 0.2s;
}
.stButton > button:hover {
    background-color: #333333;
    color: #E8C547;
}

/* Inputs */
div[data-testid="stNumberInput"] input {
    border-radius: 8px;
    border: 1.5px solid #DDDDDD;
    padding: 0.5rem 0.8rem;
    font-family: 'Source Sans 3', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Cargar modelo
# ─────────────────────────────────────────────
@st.cache_resource
def cargar_modelo():
    """Carga el modelo entrenado desde el archivo .pkl."""
    try:
        modelo = joblib.load("modelo_victimas.pkl")
        return modelo
    except FileNotFoundError:
        return None

modelo = cargar_modelo()

# ─────────────────────────────────────────────
# Encabezado
# ─────────────────────────────────────────────
st.markdown('<p class="titulo-principal">🕊️ Predictor de Tasa de Víctimas NNA</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">Reclutamiento y utilización de niños, niñas y adolescentes en el conflicto armado colombiano · SIEVCAC</p>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Verificar modelo cargado
# ─────────────────────────────────────────────
if modelo is None:
    st.markdown("""
    <div class="error-box">
        ⚠️ <strong>No se encontró el archivo del modelo.</strong><br>
        Asegúrate de que <code>modelo_victimas.pkl</code> esté en la misma carpeta que <code>app.py</code>.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
# Formulario de entrada
# ─────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### Ingresa los datos del municipio o departamento")

col1, col2 = st.columns(2)

with col1:
    victimas = st.number_input(
        "Total de víctimas del caso",
        min_value=1,
        max_value=10000,
        value=10,
        step=1,
        help="Número total de víctimas registradas en el caso."
    )

with col2:
    poblacion = st.number_input(
        "Población del territorio",
        min_value=1000,
        max_value=10_000_000,
        value=100000,
        step=1000,
        help="Población total del municipio o departamento analizado."
    )

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Validación de inputs
# ─────────────────────────────────────────────
def validar_inputs(victimas, poblacion):
    errores = []
    if victimas <= 0:
        errores.append("El número de víctimas debe ser mayor a 0.")
    if poblacion < 1000:
        errores.append("La población debe ser al menos 1.000 personas.")
    if victimas > poblacion:
        errores.append("El número de víctimas no puede superar la población total.")
    return errores

# ─────────────────────────────────────────────
# Botón de predicción
# ─────────────────────────────────────────────
if st.button("Calcular predicción →"):
    errores = validar_inputs(victimas, poblacion)

    if errores:
        for error in errores:
            st.markdown(f'<div class="error-box">❌ {error}</div>', unsafe_allow_html=True)
    else:
        try:
            # Predicción
            entrada = np.array([[victimas, poblacion]])
            prediccion = modelo.predict(entrada)[0]
            prediccion = max(0, prediccion)  # No puede ser negativa

            # Interpretación
            if prediccion < 1:
                nivel = "🟢 Bajo"
                desc = "La tasa es baja en comparación con el contexto nacional."
            elif prediccion < 5:
                nivel = "🟡 Moderado"
                desc = "La tasa es moderada. Se recomienda seguimiento continuo."
            elif prediccion < 15:
                nivel = "🟠 Alto"
                desc = "La tasa es alta. Se requiere atención prioritaria."
            else:
                nivel = "🔴 Crítico"
                desc = "La tasa es crítica. Se necesita intervención urgente."

            # Mostrar resultado
            st.markdown(f"""
            <div class="resultado-box">
                <div class="resultado-numero">{prediccion:.2f}</div>
                <div class="resultado-label">víctimas por cada 100.000 habitantes</div>
                <div class="resultado-interpretacion">
                    <strong>Nivel de riesgo:</strong> {nivel}<br>{desc}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="info-box">
                📌 <strong>Parámetros utilizados:</strong>
                Víctimas del caso: <strong>{victimas:,}</strong> ·
                Población: <strong>{poblacion:,}</strong><br>
                🤖 <strong>Modelo:</strong> Decision Tree Regressor (MAPE ≈ 1.6%)
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.markdown(f'<div class="error-box">❌ Error al generar la predicción: {str(e)}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Pie de página
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<small style='color:#AAAAAA;'>Proyecto en Analítica Aplicada · Andrea Arenas · Daniela Arizmendi · Mariana Olivares · 2025</small>",
    unsafe_allow_html=True
)
