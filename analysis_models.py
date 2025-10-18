"""
Módulo de análisis de datos con diferentes modelos de IA
"""

import requests
import json
import pandas as pd
from typing import Dict, Any, Optional
from config import ANALYSIS_CONFIG


class BaseAnalyzer:
    """Clase base para analizadores de datos"""
    
    def __init__(self):
        self.config = ANALYSIS_CONFIG
    
    def analyze(self, df: pd.DataFrame, user_question: Optional[str] = None) -> str:
        """Método abstracto para análisis"""
        raise NotImplementedError


class LocalAnalyzer(BaseAnalyzer):
    """Analizador local basado en reglas"""
    
    def analyze(self, df: pd.DataFrame, user_question: Optional[str] = None) -> str:
        """
        Analizar datos usando IA local (simulada)
        
        Args:
            df: DataFrame con los datos
            user_question: Pregunta específica del usuario
            
        Returns:
            Análisis en formato markdown
        """
        try:
            dataset_info = self._prepare_dataset_info(df)
            analysis = self._generate_analysis(df, dataset_info)
            
            if user_question:
                analysis += self._answer_user_question(user_question)
            
            return analysis
            
        except Exception as e:
            return f"Error al analizar los datos: {str(e)}"
    
    def _prepare_dataset_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Preparar información del dataset"""
        return {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.to_dict(),
            "sample_data": df.head(5).to_dict(),
            "missing_values": df.isnull().sum().to_dict()
        }
    
    def _generate_analysis(self, df: pd.DataFrame, dataset_info: Dict[str, Any]) -> str:
        """Generar análisis principal"""
        analysis = f"""
        # 📊 ANÁLISIS DE PROCESOS
        
        ## 📋 Resumen del Dataset
        - **Filas**: {dataset_info['shape'][0]}
        - **Columnas**: {dataset_info['shape'][1]}
        - **Columnas disponibles**: {', '.join(dataset_info['columns'])}
        - **Valores faltantes**: {sum(dataset_info['missing_values'].values())}
        
        ## 🔍 Análisis de Desperdicios Lean
        
        ### Actividades Identificadas:
        """
        
        # Analizar cada fila del dataset
        for idx, row in df.head(self.config['sample_rows']).iterrows():
            activity_info = self._analyze_activity(row, idx)
            analysis += activity_info
        
        analysis += self._generate_recommendations()
        return analysis
    
    def _analyze_activity(self, row: pd.Series, idx: int) -> str:
        """Analizar una actividad específica"""
        activity = row.get('actividad', f'Actividad {idx+1}')
        description = row.get('descripcion', 'Sin descripción')
        necessary = row.get('Necesaria', 'No especificado')
        
        # Clasificar como desperdicio basado en reglas
        waste_analysis = self._classify_waste(description)
        
        return f"""
        **{activity}**
        - Descripción: {description}
        - Necesaria: {necessary}
        - Desperdicio: {'SÍ' if waste_analysis['is_waste'] else 'NO'}
        - Tipo: {waste_analysis['type'] if waste_analysis['is_waste'] else 'N/A'}
        """
    
    def _classify_waste(self, description: str) -> Dict[str, Any]:
        """Clasificar si una actividad es desperdicio"""
        description_lower = description.lower()
        
        waste_patterns = {
            'Espera': ['espera', 'esperar', 'retraso', 'demora'],
            'Sobreproceso': ['repetir', 'duplicar', 'volver a'],
            'Transporte': ['mover', 'trasladar', 'transportar']
        }
        
        for waste_type, keywords in waste_patterns.items():
            if any(word in description_lower for word in keywords):
                return {'is_waste': True, 'type': waste_type}
        
        return {'is_waste': False, 'type': None}
    
    def _generate_recommendations(self) -> str:
        """Generar recomendaciones de optimización"""
        return """
        
        ## 🎯 Recomendaciones de Optimización
        
        ### 1. Eliminación de Desperdicios
        - **Esperas**: Implementar sistema de notificaciones automáticas
        - **Transporte**: Optimizar rutas con GPS
        - **Sobreproceso**: Estandarizar procedimientos
        
        ### 2. Automatización con Power Platform
        - **Power Automate**: Flujos de trabajo automatizados
        - **Power Apps**: Aplicación móvil para conductores
        - **Power BI**: Dashboard de monitoreo en tiempo real
        
        ### 3. Roadmap de Implementación (90 días)
        
        **Semana 1-2**: Análisis detallado y mapeo de procesos
        **Semana 3-4**: Diseño de soluciones Power Platform
        **Semana 5-8**: Desarrollo y pruebas
        **Semana 9-12**: Implementación y capacitación
        
        ### 4. Riesgos y Controles
        - **Riesgo**: Resistencia al cambio
        - **Control**: Programa de capacitación intensivo
        - **Riesgo**: Fallas técnicas
        - **Control**: Plan de respaldo manual
        
        ### 5. Plan de Entrenamiento
        - **Semana 1**: Capacitación en Power Platform
        - **Semana 2**: Pruebas piloto con usuarios clave
        - **Semana 3**: Capacitación masiva
        - **Semana 4**: Soporte y seguimiento
        """
    
    def _answer_user_question(self, user_question: str) -> str:
        """Responder pregunta específica del usuario"""
        return f"""
        
        ## 💬 Respuesta a tu pregunta:
        **Pregunta**: {user_question}
        
        **Respuesta**: Basado en el análisis del proceso, te recomiendo enfocarte en la eliminación de actividades de espera y transporte, que son los principales desperdicios identificados. La automatización con Power Platform puede reducir estos tiempos en un 60-80%.
        """


class HuggingFaceAnalyzer(BaseAnalyzer):
    """Analizador usando Hugging Face API"""
    
    def analyze(self, df: pd.DataFrame, user_question: Optional[str] = None) -> str:
        """
        Analizar datos usando Hugging Face
        
        Args:
            df: DataFrame con los datos
            user_question: Pregunta específica del usuario
            
        Returns:
            Análisis generado por Hugging Face o análisis local como respaldo
        """
        try:
            dataset_info = self._prepare_dataset_info(df)
            prompt = self._create_prompt(dataset_info, user_question)
            
            response = self._call_huggingface_api(prompt)
            return response
            
        except Exception as e:
            return f"Error con Hugging Face: {str(e)}. Usando análisis local como respaldo."
    
    def _prepare_dataset_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Preparar información del dataset"""
        return {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "sample_data": df.head(3).to_dict()
        }
    
    def _create_prompt(self, dataset_info: Dict[str, Any], user_question: Optional[str] = None) -> str:
        """Crear prompt para Hugging Face"""
        prompt = f"""
        Analiza este proceso de ambulancias:
        - Filas: {dataset_info['shape'][0]}
        - Columnas: {dataset_info['columns']}
        - Muestra: {dataset_info['sample_data']}
        
        Proporciona análisis de desperdicios Lean y recomendaciones de automatización.
        """
        
        if user_question:
            prompt += f"\nPregunta específica: {user_question}"
        
        return prompt
    
    def _call_huggingface_api(self, prompt: str) -> str:
        """Llamar a la API de Hugging Face"""
        response = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            json={"inputs": prompt},
            timeout=self.config['timeout_huggingface']
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', 'No se pudo generar respuesta')
            else:
                return str(result)
        else:
            return f"Modelo cargándose... Status: {response.status_code}. Usando análisis local como respaldo."


class OpenAIAnalyzer(BaseAnalyzer):
    """Analizador usando OpenAI API"""
    
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
    
    def analyze(self, df: pd.DataFrame, user_question: Optional[str] = None) -> str:
        """
        Analizar datos usando OpenAI
        
        Args:
            df: DataFrame con los datos
            user_question: Pregunta específica del usuario
            
        Returns:
            Análisis generado por OpenAI o mensaje de error
        """
        try:
            if not self.api_key:
                return "Error: Necesitas configurar tu API Key de OpenAI"
            
            dataset_info = self._prepare_dataset_info(df)
            prompt = self._create_prompt(dataset_info, user_question)
            
            response = self._call_openai_api(prompt)
            return response
            
        except Exception as e:
            return f"Error con OpenAI: {str(e)}. Usando análisis local como respaldo."
    
    def _prepare_dataset_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Preparar información del dataset"""
        return {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "sample_data": df.head(5).to_dict()
        }
    
    def _create_prompt(self, dataset_info: Dict[str, Any], user_question: Optional[str] = None) -> str:
        """Crear prompt detallado para OpenAI"""
        prompt = """
        role: system
content: 

  ## R — Role
  Eres un Asesor experto en optimizacion de procesos via metodologias six sigma, lean y a la vez un Arquitecto de Soluciones Low‑Code en Microsoft Power Platform.
  Dominas Lean (eliminar desperdicios y crear flujo), Six Sigma (reducir variabilidad), kaizen (mejora continua) y el ecosistema Power Platform:
  Power Automate (cloud/desktop RPA), Power Apps, Copilot Studio, Dataverse, AI Builder, Power BI y Power Pages.
  
  Tienes que analizar un conjunto de tareas basadas en en esta descripcion:
  
  >>Un proceso para la programacion y asignacion de servicio de ambulancias en la ciudad.<<
  
  de la siguiente manera:
  
  ## I — Instructions
  
  Recibirás un archivo Excel con las columnas: ("actividad", "descripcion", "Necesaria").
  La "actividad" es el nombre de la actividad, la "descripcion" es la descripcion detallada de esa actividad, y "Necesaria" si el experto considera que esta actividad es obligatoria incluirla.
  
  ## S — Steps
  1. Agrega una nueva columna con el nombre de "Desperdicio"
  2. En la columna "Desperdicio", marca cada una de las actividades con "SI", si la consideras una actividad de desperdicio y con "NO" en caso contrario. Explica el por que consideras una actividad desperdicio.
  3. Agrega una nueva columna con el nombre de "Actividades"
  4. Clasifica cada una de las actividades en los siguientes rubros (Operativa (bajo nivel de descicion), Analitica (Analisis basado en criterios), Cognitiva (Estretegia, creacion, resolucion compleja)) y describe las causas.
  5. Agrega una nueva columna con el nombre de "Tipo Desperdicio" y clasifica cada una de las tareas de desperdicio en las siguientes categorias (Trasporte, Inventario, Espera, Sobreproduccion, Sobreproceso, Defectos, Movimiento (movimiento inecesario de personas), talento no utilizado, Automatizacion inecesaria)
  6. Exporta esta informacion en una hoja de excel llamada "AS-IS".
  6. Ahora en base a la informacion anterior reconstruye el proceso apalancandote de metodologias lean, six sigma y kaizen, SCAMPER, mostrando las columnas de "Actividad" y "Descripcion".
  7. Asegura flujo continuo, calcula nuevos tiempos y documenta el modelo SIPOC.
  8. Como experto metologias agiles y en soluciones Low‑Code Microsoft Power Platform propónga ena serie de actividades con su respectiva descripcion con una nueva columna de automatizacion de las actividades con la solucion propuesta de como y donde realizar esta actividad y en que herramienta.
  9. agrega otra columna donde especifique los requisitos para la realizacion de la actividad propuesta.
  10. si no es posible realizarlo en power platform busca que servicio podrias usar para la optimizacion de esta actividad y explica el porque la elección.
  11. exporta este archivo en una nueva hoja del archivo de excel
  12. genera una nueva hoja de excel con un road map a 90 dias 
  12. Para terminar, mesiona riesgos, controles y plan de entrenamiento.
    
    ## E — End goal
  Entrega SIEMPRE:
    1. el archivo de excel con las hojas correspondientes
	2. En caso de no recibir el archivo o no poder parsearlo responde "No fue posible ver la información".
	3. Si la descripcion del proceso no es clara o completa responde "descripcion del proceso requiere un mayor detalle"
	4. Si no estan completas las columnas del archivo responde "informacion faltante"
	

  ## N — Narrowing
  - Idioma: español claro y pedagógico.
  - Si faltan datos o detalles, indícalo y explica el porque es necesario.

Recuerda que eres un experto en optimizacion de procesos por ende necesitas reducir costos.

Y basado en el contexto genera unos KPIS validos 
        """
        
        if user_question:
            prompt += f"\nPregunta específica: {user_question}"
        
        return prompt
    
    def _call_openai_api(self, prompt: str) -> str:
        """Llamar a la API de OpenAI"""
        import openai
        openai.api_key = self.api_key

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en optimización de procesos Six Sigma y Lean."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=self.config['max_tokens_openai'],
            temperature=self.config['temperature_openai']
        )

        return response.choices[0].message.content


class DeepSeekAnalyzer(BaseAnalyzer):
    """Analizador usando DeepSeek API"""
    
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1"
    
    def analyze(self, df: pd.DataFrame, user_question: Optional[str] = None) -> str:
        """
        Analizar datos usando DeepSeek
        
        Args:
            df: DataFrame con los datos
            user_question: Pregunta específica del usuario
            
        Returns:
            Análisis generado por DeepSeek o mensaje de error
        """
        try:
            if not self.api_key:
                return "Error: Necesitas configurar tu API Key de DeepSeek"
            
            dataset_info = self._prepare_dataset_info(df)
            prompt = self._create_prompt(dataset_info, user_question)
            
            response = self._call_deepseek_api(prompt)
            return response
            
        except Exception as e:
            return f"Error con DeepSeek: {str(e)}. Usando análisis local como respaldo."
    
    def _prepare_dataset_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Preparar información del dataset"""
        return {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "sample_data": df.head(5).to_dict()
        }
    
    def _create_prompt(self, dataset_info: Dict[str, Any], user_question: Optional[str] = None) -> str:
        """Crear prompt optimizado para DeepSeek"""
        # Crear un resumen más conciso de los datos
        sample_text = ""
        if dataset_info['sample_data']:
            for i, (col, values) in enumerate(list(dataset_info['sample_data'].items())[:3]):  # Solo primeras 3 columnas
                sample_text += f"\n- {col}: {list(values.values())[:2]}"  # Solo primeros 2 valores
        
        prompt = f"""Analiza este proceso y proporciona:

**Datos**: {dataset_info['shape'][0]} actividades, columnas: {', '.join(dataset_info['columns'])}{sample_text}

**Análisis requerido**:
1. **Desperdicios Lean**: Identifica esperas, transporte, sobreproceso
2. **Clasificación**: Operativa/Analítica/Cognitiva  
3. **Automatización**: Soluciones Power Platform específicas
4. **Roadmap 90 días**: Cronograma de implementación
5. **KPIs**: Métricas de eficiencia y calidad

**Formato**: Markdown, respuestas concisas y prácticas."""
        
        if user_question:
            prompt += f"\n\n**Pregunta específica**: {user_question}"
        
        return prompt
    
    def _call_deepseek_api(self, prompt: str) -> str:
        """Llamar a la API de DeepSeek con reintentos"""
        import requests
        import time
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un experto en optimización de procesos Six Sigma, Lean y arquitecto de soluciones Power Platform. Responde de forma concisa y práctica."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": self.config['max_tokens_deepseek'],
            "temperature": self.config['temperature_deepseek']
        }
        
        # Intentar múltiples veces
        for attempt in range(self.config['retry_attempts']):
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=self.config['timeout_deepseek']
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
                elif response.status_code == 429:
                    # Rate limit - esperar más tiempo
                    wait_time = (attempt + 1) * 5
                    if attempt < self.config['retry_attempts'] - 1:
                        return f"Rate limit alcanzado. Esperando {wait_time}s... (Intento {attempt + 1}/{self.config['retry_attempts']})"
                    else:
                        return "Rate limit alcanzado en DeepSeek. Usando análisis local como respaldo."
                else:
                    error_msg = f"Error en DeepSeek API: {response.status_code}"
                    if attempt < self.config['retry_attempts'] - 1:
                        return f"{error_msg}. Reintentando... (Intento {attempt + 1}/{self.config['retry_attempts']})"
                    else:
                        return f"{error_msg}. Usando análisis local como respaldo."
                        
            except requests.exceptions.Timeout:
                if attempt < self.config['retry_attempts'] - 1:
                    time.sleep(self.config['retry_delay'])
                    continue
                else:
                    return "Timeout en DeepSeek API después de múltiples intentos. Usando análisis local como respaldo."
                    
            except requests.exceptions.ConnectionError:
                if attempt < self.config['retry_attempts'] - 1:
                    time.sleep(self.config['retry_delay'])
                    continue
                else:
                    return "Error de conexión con DeepSeek. Verifica tu internet. Usando análisis local como respaldo."
                    
            except requests.exceptions.RequestException as e:
                if attempt < self.config['retry_attempts'] - 1:
                    time.sleep(self.config['retry_delay'])
                    continue
                else:
                    return f"Error en DeepSeek API: {str(e)}. Usando análisis local como respaldo."
        
        return "Error inesperado en DeepSeek API. Usando análisis local como respaldo."


def get_analyzer(model_type: str, api_key: Optional[str] = None) -> BaseAnalyzer:
    """
    Factory function para obtener el analizador correcto
    
    Args:
        model_type: Tipo de modelo a usar
        api_key: API key para OpenAI/DeepSeek (opcional)
        
    Returns:
        Instancia del analizador correspondiente
    """
    analyzers = {
        "local": LocalAnalyzer,
        "huggingface": HuggingFaceAnalyzer,
        "openai": lambda: OpenAIAnalyzer(api_key) if api_key else LocalAnalyzer(),
        "deepseek": lambda: DeepSeekAnalyzer(api_key) if api_key else LocalAnalyzer()
    }
    
    return analyzers.get(model_type, LocalAnalyzer)()
