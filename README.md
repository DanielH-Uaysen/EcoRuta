#  EcoRuta Coyhaique

**Dashboard interactivo para consultar los puntos de reciclaje de Coyhaique:** dónde están, qué materiales reciben y si están **abiertos o cerrados en este momento**.

Proyecto del ramo **Taller Avanzado de Desarrollo de Software** — Ingeniería Civil Informática, **Universidad de Aysén** (Semestre 1 – 2026).

---

##  Características

-  **Mapa interactivo** (Leaflet) con los puntos georreferenciados y pines de color según su categoría.
-  **Estado Abierto / Cerrado en tiempo real**, calculado en el navegador según el día y la hora local (se refresca cada 20 s).
-  **Panel lateral** con estadísticas (total, abiertos, cerrados) y **filtros por categoría**.
-  **Ficha de detalle** por punto (panel deslizante): dirección, horario, qué reciclar, qué **no** dejar y botón **"Cómo llegar"**.
-  Base de datos local en **JSON** que se **autogenera** con los datos semilla si se elimina.

## Tecnologías

- **Python 3.10+** y **Flask** (servidor web local).
- **Leaflet.js** (cartografía), **HTML/CSS/JS** puro, **Font Awesome** (iconos) y **Google Fonts** (Baloo 2 + Montserrat).
- Persistencia en **JSON**, sin bases de datos externas.

##  Estructura del repositorio

| Archivo | Descripción |
|---|---|
| `DashEcoRuta.ipynb` | **Aplicación principal.** Inicia el servidor Flask y abre el dashboard en el navegador. |
| `01_Instalar_Dependencias.ipynb` | Instala Flask y **descarga las librerías del mapa** (Leaflet, Font Awesome y tipografías) a `static/vendor/`. |
| `requirements.txt` | Dependencia de Python (Flask). |
| `Coordenadas_Puntos_Coyhaique.xlsx` | *(Extra)* Planilla con las coordenadas y datos de los puntos. |
| `puntos_coyhaique.json` | Base de datos local (se crea automáticamente al ejecutar la app). |
| `static/vendor/` | Librerías del mapa descargadas (se crea con el notebook de instalación). |

##  Instalación y uso

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/usuario/EcoRuta-Coyhaique.git
   cd EcoRuta-Coyhaique
   ```
2. **Ejecuta una vez** el notebook `01_Instalar_Dependencias.ipynb` completo (instala Flask y descarga las librerías del mapa).
3. **Abre y ejecuta** `DashEcoRuta.ipynb`. Se abrirá automáticamente el navegador en:
   ```
   http://127.0.0.1:5000
   ```
   Para detener el servidor, presiona **CTRL + C** en la consola (o detén el kernel del notebook).

>  **Alternativa sin Jupyter:** `pip install flask` y luego `python DashEcoRuta.py` (si exportas el notebook a `.py`).

##  Sobre la conexión a internet

La aplicación usa **librerías locales** si ejecutaste el notebook de instalación (modo recomendado); de lo contrario, las carga desde internet (CDN) de forma automática.

 **El fondo del mapa (las imágenes de las calles, o *tiles*) siempre se descarga en vivo**, por lo que **necesita conexión a internet** para mostrarse. Para una demostración sin riesgos, ten conexión disponible o abre la aplicación una vez antes con internet para que el navegador la guarde en caché.

##  Datos

Las ubicaciones, horarios y materiales aceptados de los **21 puntos** de reciclaje provienen de la planilla `Coordenadas_Puntos_Coyhaique.xlsx` y están cargados directamente en `DashEcoRuta.ipynb`.

##  Autor

**Daniel Herrero** — Ingeniería Civil Informática, Universidad de Aysén.

---

*Proyecto académico. Coyhaique, Región de Aysén, Chile.* ♻️
