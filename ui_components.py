"""
Componentes de interfaz de usuario para la aplicación RAC Assistant
"""

import streamlit as st
from typing import Optional
from config import MODEL_OPTIONS, FUNCTIONALITIES, UI_CONFIG


def render_sidebar(selected_model: str, api_key: Optional[str] = None) -> tuple:
    """
    Renderizar la barra lateral con configuración
    
    Args:
        selected_model: Modelo de IA seleccionado
        api_key: API key para OpenAI (opcional)
        
    Returns:
        Tupla con (selected_model, api_key)
    """
    with st.sidebar:
        st.header(UI_CONFIG['sidebar_title'])
        
        # Selección de modelo
        selected_model = st.selectbox(
            "Tipo de IA",
            options=list(MODEL_OPTIONS.keys()),
            format_func=lambda x: MODEL_OPTIONS[x],
            help="Selecciona el tipo de IA a usar"
        )
        
        # Si selecciona OpenAI o DeepSeek, pedir API key
        if selected_model == "openai":
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                help="Ingresa tu API Key de OpenAI"
            )
        elif selected_model == "deepseek":
            api_key = st.text_input(
                "DeepSeek API Key",
                type="password",
                help="Ingresa tu API Key de DeepSeek"
            )
        else:
            api_key = None
        
        st.markdown("---")
        st.markdown("### 📊 Funcionalidades")
        for functionality in FUNCTIONALITIES:
            st.markdown(functionality)
    
    return selected_model, api_key


def render_file_upload_tab() -> Optional[object]:
    """
    Renderizar la pestaña de carga de archivos
    
    Returns:
        Archivo subido o None
    """
    st.header("📁 Carga tu archivo Excel de Procesos")
    
    st.markdown("""
    **Formato esperado del archivo Excel:**
    - Columna "actividad": Nombre de la actividad
    - Columna "descripcion": Descripción detallada de la actividad  
    - Columna "Necesaria": Si la actividad es obligatoria (SI/NO)
    """)
    
    uploaded_file = st.file_uploader(
        "Selecciona un archivo Excel con datos de procesos",
        type=['xlsx', 'xls'],
        help="Sube un archivo Excel con el formato: actividad, descripcion, Necesaria"
    )
    
    return uploaded_file


def render_data_preview(df) -> None:
    """
    Renderizar vista previa de los datos cargados
    
    Args:
        df: DataFrame con los datos
    """
    if df is not None:
        st.success(f"✅ Archivo cargado exitosamente")
        
        # Mostrar resumen
        from utils import display_data_overview
        display_data_overview(df)
        
        # Mostrar preview de datos
        st.subheader("👀 Vista previa de los datos")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Mostrar información de columnas
        st.subheader("📋 Información de columnas")
        from utils import display_column_info
        display_column_info(df)


def render_chat_tab(uploaded_data) -> None:
    """
    Renderizar la pestaña de chat con IA
    
    Args:
        uploaded_data: DataFrame con los datos cargados
    """
    st.header("💬 Chat con el Experto en Procesos")
    
    st.markdown("""
    **El asistente es un experto en:**
    - 🎯 Metodologías Six Sigma y Lean
    - ⚡ Microsoft Power Platform
    - 🔄 Optimización de procesos
    - 📊 Análisis de desperdicios    
    """)
    
    if uploaded_data is None:
        st.warning("⚠️ Primero carga un archivo Excel en la pestaña 'Cargar Datos'")
    else:
        # Mostrar historial de chat
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input para nuevo mensaje
        if prompt := st.chat_input("Haz una pregunta sobre optimización de procesos..."):
            # Agregar mensaje del usuario
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            return prompt
    
    return None


def render_chat_response(selected_model: str, uploaded_data, prompt: str, api_key: Optional[str] = None) -> None:
    """
    Renderizar respuesta del chat
    
    Args:
        selected_model: Modelo de IA seleccionado
        uploaded_data: DataFrame con los datos
        prompt: Pregunta del usuario
        api_key: API key para OpenAI (opcional)
    """
    with st.chat_message("assistant"):
        with st.spinner("🤔 Analizando tu proceso..."):
            from analysis_models import get_analyzer
            
            analyzer = get_analyzer(selected_model, api_key)
            response = analyzer.analyze(uploaded_data, prompt)
            
            st.markdown(response)
    
    # Agregar respuesta del asistente
    st.session_state.messages.append({"role": "assistant", "content": response})


def render_main_layout() -> None:
    """
    Renderizar el layout principal de la aplicación
    """
    st.title(UI_CONFIG['main_title'])
    
    # Crear pestañas
    tab1, tab2 = st.tabs(["📁 Cargar Datos", "💬 Chat con IA"])
    
    return tab1, tab2
