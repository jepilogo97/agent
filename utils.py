"""
Utilidades comunes para la aplicación RAC Assistant
"""

import pandas as pd
import streamlit as st
from typing import Dict, Any, Optional
from config import FILE_CONFIG, UI_CONFIG


def load_excel_file(uploaded_file) -> Optional[pd.DataFrame]:
    """
    Cargar archivo Excel y retornar DataFrame
    
    Args:
        uploaded_file: Archivo subido por el usuario
        
    Returns:
        DataFrame con los datos o None si hay error
    """
    try:
        if uploaded_file.name.endswith(tuple(f'.{ext}' for ext in FILE_CONFIG['allowed_extensions'])):
            df = pd.read_excel(uploaded_file)
            return df
        else:
            st.error(f"Por favor, sube un archivo Excel ({', '.join(FILE_CONFIG['allowed_extensions'])})")
            return None
    except Exception as e:
        st.error(f"Error al cargar el archivo: {str(e)}")
        return None


def display_data_overview(df: pd.DataFrame) -> None:
    """
    Mostrar resumen del dataset con métricas principales
    
    Args:
        df: DataFrame a mostrar
    """
    cols = st.columns(UI_CONFIG['metrics_columns'])
    
    metrics = [
        ("📊 Filas", df.shape[0]),
        ("📋 Columnas", df.shape[1]),
        ("❌ Valores faltantes", df.isnull().sum().sum()),
        ("💾 Memoria", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    ]
    
    for i, (label, value) in enumerate(metrics):
        with cols[i]:
            st.metric(label, value)


def display_column_info(df: pd.DataFrame) -> None:
    """
    Mostrar información detallada de las columnas del DataFrame
    
    Args:
        df: DataFrame a analizar
    """
    col_info = pd.DataFrame({
        'Columna': df.columns,
        'Tipo': df.dtypes,
        'Valores únicos': df.nunique(),
        'Valores faltantes': df.isnull().sum()
    })
    st.dataframe(col_info, use_container_width=True)


def validate_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validar que el DataFrame tenga la estructura esperada
    
    Args:
        df: DataFrame a validar
        
    Returns:
        Diccionario con información de validación
    """
    validation_result = {
        "is_valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Verificar columnas requeridas
    missing_columns = set(FILE_CONFIG['expected_columns']) - set(df.columns)
    if missing_columns:
        validation_result["is_valid"] = False
        validation_result["errors"].append(f"Columnas faltantes: {', '.join(missing_columns)}")
    
    # Verificar si hay datos
    if df.empty:
        validation_result["is_valid"] = False
        validation_result["errors"].append("El archivo está vacío")
    
    # Advertencias
    if df.isnull().sum().sum() > 0:
        validation_result["warnings"].append("Hay valores faltantes en el dataset")
    
    return validation_result


def prepare_dataset_info(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Preparar información resumida del dataset para análisis
    
    Args:
        df: DataFrame a analizar
        
    Returns:
        Diccionario con información del dataset
    """
    return {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.to_dict(),
        "sample_data": df.head(5).to_dict(),
        "missing_values": df.isnull().sum().to_dict()
    }


def initialize_session_state() -> None:
    """
    Inicializar el estado de la sesión de Streamlit
    """
    default_state = {
        "messages": [],
        "uploaded_data": None,
        "analysis_results": None
    }
    
    for key, value in default_state.items():
        if key not in st.session_state:
            st.session_state[key] = value


def display_footer() -> None:
    """
    Mostrar el footer de la aplicación
    """
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            Optimización de Procesos con IA
        </div>
        """,
        unsafe_allow_html=True
    )
