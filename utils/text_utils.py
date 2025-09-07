"""
Utilidades de Procesamiento de Lenguaje Natural para Análisis de Variables Médicas

Este módulo implementa funciones especializadas para el procesamiento y normalización
de texto en el contexto de análisis de variables clínicas y epidemiológicas.

Algoritmos Implementados:
1. Normalización Unicode: Eliminación sistemática de acentos y caracteres especiales
2. Similitud textual: Implementación del algoritmo de Ratcliff-Obershelp
3. Construcción de candidatos: Optimización para comparaciones masivas
4. Limpieza de sinónimos: Preprocesamiento para terminología médica

Aplicaciones Específicas:
- Normalización de nombres de columnas en datasets médicos
- Comparación robusta de terminología clínica multiidioma
- Procesamiento de sinónimos para variables críticas de diabetes
- Optimización de rendimiento para análisis de datasets grandes

Consideraciones Técnicas:
- Compatible con Unicode completo (incluyendo caracteres especiales médicos)
- Optimizado para terminología médica en español e inglés
- Algoritmo de similitud balanceado entre precisión y rendimiento
- Manejo robusto de casos edge en nomenclatura clínica

Versión: 1.0
"""
import re
import unicodedata
from difflib import SequenceMatcher
from typing import List, Tuple, Optional, Union

def normalizar_texto(texto: Union[str, int, float]) -> str:
    """
    Normaliza texto para comparación eliminando acentos, 
    convirtiendo a minúsculas y limpiando caracteres especiales.
    
    Args:
        texto (str): Texto a normalizar
        
    Returns:
        str: Texto normalizado
    """
    if not isinstance(texto, str):
        texto = str(texto)
    
    # Convertir a minúsculas y quitar espacios
    texto = texto.strip().lower()
    
    # Quitar acentos
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
    
    # Reemplazar caracteres especiales por espacios
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    
    # Limpiar espacios múltiples
    return re.sub(r"\s+", " ", texto).strip()

def calcular_similitud(texto1: str, texto2: str) -> float:
    """
    Calcula la similitud entre dos textos usando SequenceMatcher.
    
    Args:
        texto1 (str): Primer texto
        texto2 (str): Segundo texto
        
    Returns:
        float: Valor de similitud entre 0.0 y 1.0
    """
    return SequenceMatcher(None, texto1, texto2).ratio()

def construir_candidatos(columnas: List[str]) -> List[Tuple[str, str]]:
    """
    Construye una lista de candidatos con texto original y normalizado.
    
    Args:
        columnas (List[str]): Lista de nombres de columnas
        
    Returns:
        List[Tuple[str, str]]: Lista de tuplas (original, normalizado)
    """
    candidatos = []
    for columna in columnas:
        texto_normalizado = normalizar_texto(columna)
        candidatos.append((columna, texto_normalizado))
    return candidatos

def encontrar_mejor_coincidencia(
    texto_objetivo: str, 
    candidatos: List[Tuple[str, str]], 
    umbral: float = 0.8
) -> Tuple[Optional[str], float]:
    """
    Encuentra la mejor coincidencia para un texto objetivo entre los candidatos.
    
    Args:
        texto_objetivo (str): Texto a buscar
        candidatos (List[Tuple[str, str]]): Lista de candidatos (original, normalizado)
        umbral (float): Umbral mínimo de similitud
        
    Returns:
        Tuple[str, float]: (mejor_coincidencia, score) o (None, 0.0) si no hay coincidencias
    """
    texto_objetivo_norm = normalizar_texto(texto_objetivo)
    mejor_coincidencia = None
    mejor_score = 0.0
    
    for original, normalizado in candidatos:
        score = calcular_similitud(texto_objetivo_norm, normalizado)
        if score > mejor_score:
            mejor_score = score
            mejor_coincidencia = original
    
    if mejor_score >= umbral:
        return mejor_coincidencia, mejor_score
    else:
        return None, 0.0

def limpiar_lista_sinonimos(sinonimos_texto: str) -> List[str]:
    """
    Limpia y procesa una lista de sinónimos separados por comas.
    
    Args:
        sinonimos_texto (str): Texto con sinónimos separados por comas
        
    Returns:
        List[str]: Lista de sinónimos limpios
    """
    if not sinonimos_texto:
        return []
    
    sinonimos = sinonimos_texto.split(',')
    sinonimos_limpios = []
    
    for sinonimo in sinonimos:
        sinonimo_limpio = sinonimo.strip()
        if sinonimo_limpio:  # Solo agregar si no está vacío
            sinonimos_limpios.append(sinonimo_limpio)
    
    return sinonimos_limpios
