# Predictor de Tasa de Víctimas NNA

Aplicación interactiva para predecir la tasa de víctimas de reclutamiento y utilización de niños, niñas y adolescentes (NNA) en el conflicto armado colombiano, basada en datos del **SIEVCAC**.

---

## Descripción

Esta aplicación despliega un modelo de **Machine Learning** entrenado con datos históricos del conflicto armado colombiano. Permite estimar la **tasa de víctimas por cada 100.000 habitantes** a partir de dos variables:

- **Total de víctimas del caso**
- **Población del territorio**

---

## Modelo

| Característica | Detalle |
|---|---|
| Algoritmo | Decision Tree Regressor |
| Métrica principal | MAPE ≈ 1.6% |
| Variables de entrada | `total_de_victimas_del_caso`, `poblacion` |
| Variable de salida | `tasa_victimas_100k` |
| Datos | SIEVCAC – últimos 3 años disponibles |

Se evaluaron 5 modelos (Decision Tree, Extra Trees, Gradient Boosting, CatBoost, AdaBoost) y se seleccionó **Decision Tree** por su menor MAPE y alta interpretabilidad.

---

## Cómo usar la aplicación

1. Ingresa el **total de víctimas** del caso
2. Ingresa la **población** del municipio o departamento
3. Haz clic en **"Calcular predicción"**
4. La app muestra la tasa estimada y el nivel de riesgo

---

## Instalación local

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la app
streamlit run app.py
```

Asegúrate de tener el archivo `modelo_victimas.pkl` en la misma carpeta.

---

## structura del proyecto

```
├── app.py                  # Aplicación principal de Streamlit
├── modelo_victimas.pkl     # Modelo entrenado (Decision Tree)
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación
```

---

## Limitaciones

- El modelo fue entrenado con datos de los últimos 3 años del SIEVCAC.
- Las predicciones son estimaciones estadísticas, no cifras oficiales.
- No reemplaza el análisis institucional especializado.

---

## utoras

- Andrea Arenas Posada  
- Daniela Arizmendi Baron  
- Mariana Olivares Gomez  

**Proyecto en Analítica Aplicada · 2026**
