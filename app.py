"""
RAC Assistant - Aplicación principal para optimización de procesos con IA
"""

import streamlit as st
import pandas as pd
from config import PAGE_CONFIG
from utils import (
    initialize_session_state, 
    load_excel_file, 
    validate_dataframe,
    display_footer
)
from ui_components import (
    render_sidebar,
    render_main_layout,
    render_file_upload_tab,
    render_data_preview,
    render_chat_tab,
    render_chat_response
)


def main():
    """Función principal de la aplicación"""
    
    # Configurar página
    st.set_page_config(**PAGE_CONFIG)
    
    # Inicializar estado de la sesión
    initialize_session_state()
    
    # Renderizar sidebar y obtener configuración
    selected_model, api_key = render_sidebar("local")
    
    # Renderizar layout principal
    tab1, tab2 = render_main_layout()
    
    # Pestaña 1: Cargar Datos
    with tab1:
        uploaded_file = render_file_upload_tab()
        
        if uploaded_file is not None:
            # Cargar datos
            df = load_excel_file(uploaded_file)
            
            if df is not None:
                # Validar datos
                validation = validate_dataframe(df)
                
                if validation["is_valid"]:
                    st.session_state.uploaded_data = df
                    
                    # Mostrar advertencias si las hay
                    for warning in validation["warnings"]:
                        st.warning(f"⚠️ {warning}")
                    
                    # Renderizar vista previa
                    render_data_preview(df)
                    
                else:
                    # Mostrar errores
                    for error in validation["errors"]:
                        st.error(f"❌ {error}")
    
    # Pestaña 2: Chat con IA
    with tab2:
        prompt = render_chat_tab(st.session_state.uploaded_data)
        
        if prompt is not None:
            render_chat_response(
                selected_model, 
                st.session_state.uploaded_data, 
                prompt, 
                api_key
            )
    
    # Footer
    display_footer()


if __name__ == "__main__":
    main()
