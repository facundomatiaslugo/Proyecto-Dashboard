# 🇦🇷 La Albiceleste en los Mundiales - Dashboard Interactivo

Este proyecto consiste en un dashboard interactivo desarrollado en **Python** con **Streamlit**, que explora y analiza la historia de la Selección Argentina de fútbol en las Copas del Mundo, desde Uruguay 1930 hasta el Mundial 2026.

El objetivo principal es aplicar técnicas de **tratamiento de datos** y **Storytelling**, transformando un dataset con información cruda en una aplicación web visual y fácil de explorar.

## 🛠️ Tecnologías Utilizadas
*   **Python** (Lógica y procesamiento)
*   **Pandas** (Limpieza y transformación de datos)
*   **Streamlit** (Desarrollo de la aplicación web)
*   **Plotly** (Gráficos interactivos y visualizaciones dinámicas)

## ⚙️ Características del Proyecto
*   **Pipeline de Datos:** El script `scripts/limpieza.py` procesa un dataset público (1930-2022), incorpora datos del Mundial 2026 y genera bases de datos limpias para el análisis.
*   **Dashboard Interactivo:** Tres pestañas principales (Resumen histórico, Goles/Goleadores y Partido a Partido) con KPIs, tablas dinámicas y gráficos.
*   **Storytelling:** El dashboard no solo muestra datos, sino que guía al usuario a través de la evolución del rendimiento del equipo, destacando los ciclos de goleadores y la mejora defensiva a lo largo de las décadas.

## 🚀 ¿Cómo ejecutar el proyecto localmente?
Si deseás correr este proyecto en tu computadora, seguí estos pasos:

1. Cloná el repositorio:
   `git clone https://github.com/facundomatiaslugo/Proyecto-Dashboard`
2. Instalá las dependencias:
   `pip install -r requirements.txt`
3. Ejecutá la aplicación:
   `streamlit run app.py`

---
*Proyecto desarrollado para la materia Análisis y Exploración de Datos - Instituto Tecnológico Beltrán (2026).*
