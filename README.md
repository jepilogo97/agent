# RAC Assistant - Optimización de Procesos con IA

Una aplicación Streamlit para el análisis y optimización de procesos empresariales utilizando metodologías Lean, Six Sigma y Microsoft Power Platform.

## 🚀 Características

- **📁 Carga de archivos Excel** con análisis automático de procesos
- **🔍 Análisis de desperdicios Lean** con clasificación automática
- **🧠 Clasificación Six Sigma** de actividades
- **⚡ Recomendaciones de automatización** con Power Platform
- **💬 Chat interactivo** con experto en procesos
- **📈 Roadmap de optimización** a 90 días

## 📋 Requisitos

- Python 3.8+
- Streamlit
- Pandas
- NumPy
- OpenAI (opcional)

## 🛠️ Instalación

1. Clona el repositorio:
```bash
git clone <repository-url>
cd proyecto_final_mia
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:
```bash
streamlit run app.py
```

## 📁 Estructura del Proyecto

```
proyecto_final_mia/
├── app.py                 # Aplicación principal
├── app_fixed.py          # Versión original (referencia)
├── config.py             # Configuración de la aplicación
├── utils.py              # Utilidades comunes
├── analysis_models.py    # Módulos de análisis con IA
├── ui_components.py      # Componentes de interfaz
├── requirements.txt      # Dependencias
└── README.md            # Este archivo
```

## 🔧 Configuración

### Modelos de IA Disponibles

1. **IA Local (Recomendado)**: Análisis basado en reglas predefinidas
2. **Hugging Face**: Análisis usando modelos públicos en línea
3. **OpenAI**: Análisis avanzado con GPT (requiere API key)
4. **DeepSeek**: Análisis con modelo DeepSeek (requiere API key, más económico)

### Formato de Archivo Excel

El archivo Excel debe contener las siguientes columnas:
- `actividad`: Nombre de la actividad
- `descripcion`: Descripción detallada de la actividad
- `Necesaria`: Si la actividad es obligatoria (SI/NO)

## 🎯 Uso

1. **Cargar Datos**: Sube un archivo Excel con el formato especificado
2. **Análisis Automático**: La aplicación analizará automáticamente los desperdicios
3. **Chat Interactivo**: Haz preguntas específicas sobre optimización
4. **Recomendaciones**: Recibe sugerencias de automatización con Power Platform

## 📊 Funcionalidades de Análisis

### Desperdicios Lean Identificados
- **Espera**: Tiempos de inactividad
- **Transporte**: Movimientos innecesarios
- **Sobreproceso**: Actividades redundantes
- **Inventario**: Acumulación excesiva
- **Defectos**: Errores y correcciones

### Recomendaciones Power Platform
- **Power Automate**: Automatización de flujos
- **Power Apps**: Aplicaciones móviles
- **Power BI**: Dashboards de monitoreo
- **Dataverse**: Gestión de datos

## 🔒 Seguridad

- Las API keys se manejan de forma segura
- Los datos se procesan localmente cuando es posible
- No se almacenan archivos permanentemente

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 📞 Soporte

Para soporte técnico o preguntas, por favor abre un issue en el repositorio.

---

**Desarrollado con ❤️ para la optimización de procesos empresariales**