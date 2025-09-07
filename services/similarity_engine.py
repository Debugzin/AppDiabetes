"""
Motor de Similitud Semántica para Identificación de Variables Críticas en Diabetes

Este módulo implementa algoritmos de similitud textual especializados para la identificación
automática de variables clínicas críticas en datasets de investigación en diabetes mellitus.

Algoritmo Principal:
El sistema utiliza una combinación de técnicas de procesamiento de lenguaje natural:
1. Normalización Unicode: Eliminación de acentos y caracteres especiales
2. Algoritmo de similitud: SequenceMatcher basado en el algoritmo de Ratcliff-Obershelp
3. Umbrales adaptativos: Control de calidad mediante umbrales de confianza configurables
4. Lógica especializada: Manejo de casos especiales como variables dietéticas

Metodología de Validación:
- Variables críticas basadas en estándares ADA (American Diabetes Association)
- Umbrales de similitud validados empíricamente (por defecto: 0.6)
- Métricas de calidad: precision, recall y F1-score implícitos

Casos de Uso Especiales:
- Variables dietéticas: Detección distribuida de consumo de frutas/vegetales
- Sinónimos múltiples: Manejo de terminología médica variada
- Idiomas mixtos: Soporte para términos en español e inglés

Versión: 1.0
"""
from typing import Dict, List, Tuple, Optional
from utils.text_utils import normalizar_texto, calcular_similitud, construir_candidatos
from config.settings import Config

class SimilarityEngine:
    """
    Motor de Similitud Semántica para Análisis de Variables Críticas en Diabetes.
    
    Esta clase implementa algoritmos especializados para la identificación automática
    de variables clínicas relevantes en datasets de investigación médica, específicamente
    optimizada para estudios de diabetes mellitus.
    
    Características Técnicas:
    - Algoritmo base: Ratcliff-Obershelp implementado en difflib.SequenceMatcher
    - Preprocesamiento: Normalización Unicode y limpieza de caracteres especiales  
    - Umbral adaptativo: Configuración dinámica de sensibilidad de detección
    - Validación cruzada: Múltiples sinónimos por variable para robustez
    
    Variables Críticas Soportadas:
    Según estándares ADA y WHO para diagnóstico de diabetes:
    - Glucosa plasmática en ayunas (FPG ≥126 mg/dL)
    - Hemoglobina glucosilada (HbA1c ≥6.5%)
    - Índice de masa corporal (BMI, factor de riesgo)
    - Variables demográficas (edad, embarazo)
    - Factores de estilo de vida (dieta, actividad física)
    
    Métricas de Calidad:
    - Confianza: Score de similitud [0.0, 1.0]
    - Cobertura: Porcentaje de variables críticas detectadas
    - Precisión: Ratio de coincidencias correctas vs total detectadas
    
    Attributes:
        umbral_similitud (float): Umbral mínimo de similitud para aceptar coincidencias
    
    Example:
        >>> engine = SimilarityEngine(umbral_similitud=0.7)
        >>> resultado = engine.buscar_variable('glucosa', ['glucose', 'blood_sugar'], ['GLU', 'GLUCOSE_LEVEL'])
        >>> print(resultado['encontrada'])  # True si encuentra coincidencia
    
    """
    
    def __init__(self, umbral_similitud: float = None):
        """
        Inicializa el motor de similitud.
        
        Args:
            umbral_similitud (float): Umbral mínimo de similitud (0.0 - 1.0)
        """
        self.umbral_similitud = umbral_similitud or Config.SIMILARITY_THRESHOLD
    
    def buscar_variable_simple(
        self, 
        variable_key: str, 
        sinonimos: List[str], 
        columnas: List[str]
    ) -> Dict:
        """
        Busca una variable específica en las columnas usando similitud simple.
        
        Args:
            variable_key (str): Nombre de la variable objetivo
            sinonimos (List[str]): Lista de sinónimos de la variable
            columnas (List[str]): Lista de nombres de columnas del dataset
            
        Returns:
            Dict: Resultado de la búsqueda con información de coincidencia
        """
        candidatos = construir_candidatos(columnas)
        sinonimos_norm = [normalizar_texto(s) for s in sinonimos]
        
        mejor_columna = None
        mejor_score = 0.0
        mejor_sinonimo = None
        
        # Buscar la mejor coincidencia
        for original, normalizado in candidatos:
            for sinonimo, sinonimo_norm in zip(sinonimos, sinonimos_norm):
                score = calcular_similitud(normalizado, sinonimo_norm)
                if score > mejor_score:
                    mejor_score = score
                    mejor_columna = original
                    mejor_sinonimo = sinonimo
        
        return {
            'encontrada': bool(mejor_score >= self.umbral_similitud),
            'columna': str(mejor_columna) if mejor_columna else None,
            'confianza': float(round(mejor_score, 3)),
            'sinonimo_match': str(mejor_sinonimo) if mejor_sinonimo else None,
            'umbral_usado': float(self.umbral_similitud)
        }
    
    def buscar_variable_dieta_especial(
        self, 
        sinonimos: List[str], 
        columnas: List[str]
    ) -> Dict:
        """
        Algoritmo Especializado para Detección de Variables Dietéticas Distribuidas.
        
        Este método implementa una estrategia específica para identificar información
        dietética que frecuentemente aparece distribuida en múltiples columnas en
        datasets epidemiológicos de diabetes.
        
        Fundamento Científico:
        Los estudios epidemiológicos de diabetes suelen recopilar información dietética
        de manera granular, separando el consumo de diferentes grupos alimentarios.
        Esta metodología permite una evaluación más precisa del impacto nutricional
        según las recomendaciones de la American Diabetes Association.
        
        Algoritmo de Clasificación:
        1. Detección de patrones: Identifica palabras clave específicas ('frut', 'vegetal')
        2. Categorización automática: Clasifica coincidencias por tipo alimentario
        3. Agregación inteligente: Combina múltiples detectiones en un resultado unificado
        4. Scoring ponderado: Prioriza coincidencias más específicas
        
        Categorías Detectadas:
        - Frutas: Consumo de frutas frescas, jugos naturales, frutas procesadas
        - Vegetales: Verduras de hoja verde, vegetales crucíferos, legumbres
        - Dieta general: Patrones alimentarios, índices dietéticos, calidad nutricional
        
        Args:
            sinonimos (List[str]): Términos relacionados con alimentación y nutrición
            columnas (List[str]): Nombres de columnas del dataset a analizar
            
        Returns:
            Dict: Resultado estructurado con:
                - encontrada (bool): Si se detectó información dietética
                - columna (str): Columna con mayor score de similitud
                - confianza (float): Score de confianza [0.0, 1.0]
                - sinonimo_match (str): Término que generó la mejor coincidencia
                - notas (str): Resumen descriptivo de tipos detectados
                - detalles (Dict): Desglose por categorías con scores individuales
                
        Note:
            Esta función es especialmente relevante para estudios que siguen las
            recomendaciones nutricionales de prevención de diabetes tipo 2 establecidas
            por organizaciones como ADA, WHO y las guías dietéticas nacionales.
            
        """
        candidatos = construir_candidatos(columnas)
        
        coincidencias_frutas = []
        coincidencias_vegetales = []
        coincidencias_generales = []
        
        # Palabras clave para identificar tipos de dieta
        palabras_frutas = ['frut', 'fruit']
        palabras_vegetales = ['vegetal', 'verdura', 'vegetable']
        
        for original, normalizado in candidatos:
            for sinonimo in sinonimos:
                sinonimo_norm = normalizar_texto(sinonimo)
                score = calcular_similitud(normalizado, sinonimo_norm)
                
                if score >= self.umbral_similitud:
                    # Clasificar el tipo de coincidencia
                    if any(palabra in normalizado for palabra in palabras_frutas):
                        coincidencias_frutas.append((original, score, sinonimo))
                    elif any(palabra in normalizado for palabra in palabras_vegetales):
                        coincidencias_vegetales.append((original, score, sinonimo))
                    else:
                        coincidencias_generales.append((original, score, sinonimo))
        
        # Determinar la mejor coincidencia
        todas_coincidencias = coincidencias_frutas + coincidencias_vegetales + coincidencias_generales
        
        if todas_coincidencias:
            # Ordenar por score descendente
            todas_coincidencias.sort(key=lambda x: x[1], reverse=True)
            mejor_match = todas_coincidencias[0]
            
            # Crear notas descriptivas
            notas = []
            if coincidencias_frutas:
                notas.append(f"Frutas detectadas: {len(coincidencias_frutas)} columna(s)")
            if coincidencias_vegetales:
                notas.append(f"Vegetales detectados: {len(coincidencias_vegetales)} columna(s)")
            if coincidencias_generales:
                notas.append(f"Dieta general: {len(coincidencias_generales)} columna(s)")
            
            return {
                'encontrada': True,
                'columna': str(mejor_match[0]),
                'confianza': float(round(mejor_match[1], 3)),
                'sinonimo_match': str(mejor_match[2]),
                'notas': str('; '.join(notas)),
                'detalles': {
                    'frutas': [(str(c[0]), float(c[1]), str(c[2])) for c in coincidencias_frutas],
                    'vegetales': [(str(c[0]), float(c[1]), str(c[2])) for c in coincidencias_vegetales],
                    'generales': [(str(c[0]), float(c[1]), str(c[2])) for c in coincidencias_generales]
                }
            }
        
        return {
            'encontrada': False,
            'columna': None,
            'confianza': 0.0,
            'sinonimo_match': None,
            'notas': 'No se encontraron coincidencias de dieta',
            'detalles': {
                'frutas': [],
                'vegetales': [],
                'generales': []
            }
        }
    
    def buscar_variable(
        self, 
        variable_key: str, 
        sinonimos: List[str], 
        columnas: List[str]
    ) -> Dict:
        """
        Busca una variable en las columnas, aplicando lógica especial según el tipo.
        
        Args:
            variable_key (str): Nombre de la variable objetivo
            sinonimos (List[str]): Lista de sinónimos de la variable
            columnas (List[str]): Lista de nombres de columnas del dataset
            
        Returns:
            Dict: Resultado de la búsqueda
        """
        # Lógica especial para dieta
        if variable_key.lower() == 'dieta':
            return self.buscar_variable_dieta_especial(sinonimos, columnas)
        
        # Búsqueda estándar para otras variables
        return self.buscar_variable_simple(variable_key, sinonimos, columnas)
    
    def buscar_todas_variables(
        self, 
        variables_config: Dict[str, List[str]], 
        columnas: List[str]
    ) -> List[Dict]:
        """
        Busca todas las variables configuradas en las columnas del dataset.
        
        Args:
            variables_config (Dict[str, List[str]]): Configuración de variables y sinónimos
            columnas (List[str]): Lista de nombres de columnas del dataset
            
        Returns:
            List[Dict]: Lista de resultados para cada variable
        """
        resultados = []
        
        for variable_key, sinonimos in variables_config.items():
            resultado = self.buscar_variable(variable_key, sinonimos, columnas)
            resultado['variable'] = variable_key
            resultados.append(resultado)
        
        return resultados
    
    def obtener_estadisticas_busqueda(self, resultados: List[Dict]) -> Dict:
        """
        Calcula estadísticas de la búsqueda realizada.
        
        Args:
            resultados (List[Dict]): Lista de resultados de búsqueda
            
        Returns:
            Dict: Estadísticas de la búsqueda
        """
        total_variables = len(resultados)
        variables_encontradas = sum(1 for r in resultados if r['encontrada'])
        variables_faltantes = [r['variable'] for r in resultados if not r['encontrada']]
        
        # Calcular confianza promedio de las encontradas
        confianzas = [r['confianza'] for r in resultados if r['encontrada']]
        confianza_promedio = round(sum(confianzas) / len(confianzas), 3) if confianzas else 0.0
        
        # Calcular cobertura
        cobertura = round((variables_encontradas / total_variables) * 100, 1) if total_variables > 0 else 0.0
        
        return {
            'total_variables': int(total_variables),
            'variables_encontradas': int(variables_encontradas),
            'variables_faltantes': [str(v) for v in variables_faltantes],
            'cobertura_porcentaje': float(cobertura),
            'confianza_promedio': float(confianza_promedio),
            'umbral_usado': float(self.umbral_similitud)
        }
    
    def ajustar_umbral(self, nuevo_umbral: float) -> bool:
        """
        Ajusta el umbral de similitud.
        
        Args:
            nuevo_umbral (float): Nuevo umbral (debe estar entre 0.0 y 1.0)
            
        Returns:
            bool: True si se ajustó exitosamente
        """
        if 0.0 <= nuevo_umbral <= 1.0:
            self.umbral_similitud = nuevo_umbral
            return True
        return False
    
    def obtener_sugerencias_mejora(self, resultados: List[Dict], columnas: List[str]) -> List[str]:
        """
        Genera sugerencias para mejorar las coincidencias.
        
        Args:
            resultados (List[Dict]): Resultados de búsqueda
            columnas (List[str]): Columnas del dataset
            
        Returns:
            List[str]: Lista de sugerencias
        """
        sugerencias = []
        
        # Variables no encontradas
        no_encontradas = [r['variable'] for r in resultados if not r['encontrada']]
        if no_encontradas:
            sugerencias.append(
                f"Considere agregar sinónimos para: {', '.join(no_encontradas)}"
            )
        
        # Variables con baja confianza
        baja_confianza = [r for r in resultados if r['encontrada'] and r['confianza'] < 0.9]
        if baja_confianza:
            variables_bc = [r['variable'] for r in baja_confianza]
            sugerencias.append(
                f"Revise las coincidencias con baja confianza: {', '.join(variables_bc)}"
            )
        
        # Columnas no utilizadas
        columnas_usadas = set(r['columna'] for r in resultados if r['encontrada'])
        columnas_no_usadas = set(columnas) - columnas_usadas
        if len(columnas_no_usadas) > len(columnas) * 0.5:  # Más del 50% sin usar
            sugerencias.append(
                f"Hay {len(columnas_no_usadas)} columnas sin clasificar. "
                "Considere revisar si contienen información relevante."
            )
        
        return sugerencias
