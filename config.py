"""
Configuración de la aplicación RAC Assistant
"""

# Configuración de la página de Streamlit
PAGE_CONFIG = {
    "page_title": "RAC Assistant - Análisis con IA Gratuita",
    "page_icon": "🤖",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Opciones de modelos de IA disponibles
MODEL_OPTIONS = {
    "local": "IA Local (Recomendado)",
    "huggingface": "Hugging Face (Online)",
    "openai": "OpenAI (Requiere API Key)",
    "deepseek": "DeepSeek (Requerie API Key)"
}

# Configuración de análisis
ANALYSIS_CONFIG = {
    "sample_rows": 10,
    "max_tokens_openai": 2000,
    "temperature_openai": 0.7,
    "timeout_huggingface": 30,
    "max_tokens_deepseek": 1500,  # Reducido para evitar timeouts
    "temperature_deepseek": 0.7,
    "timeout_deepseek": 60,  # Aumentado a 60 segundos
    "retry_attempts": 3,  # Número de reintentos
    "retry_delay": 2  # Segundos entre reintentos
}

# Configuración de archivos
FILE_CONFIG = {
    "allowed_extensions": ['xlsx', 'xls'],
    "expected_columns": ["actividad", "descripcion", "Necesaria"],
    "max_file_size_mb": 10
}

# Configuración de UI
UI_CONFIG = {
    "sidebar_title": "⚙️ Configuración",
    "main_title": "Optimización de Procesos con IA",
    "metrics_columns": 4
}

# Funcionalidades de la aplicación
FUNCTIONALITIES = [
    "📁 Carga archivos Excel de procesos",
    "🔍 Análisis de desperdicios Lean",
    "🧠 Clasificación Six Sigma",
    "⚡ Automatización Power Platform",
    "💬 Chat con experto en procesos",
    "📈 Roadmap de optimización"
]
