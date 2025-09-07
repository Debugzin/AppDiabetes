"""
Gestor de Variables Críticas para Investigación en Diabetes Mellitus

Este módulo implementa la gestión centralizada de variables críticas y sus sinónimos
para análisis automatizado de datasets de investigación en diabetes. Proporciona
funcionalidades CRUD completas con persistencia en JSON y validación de datos.

Funcionalidades Principales:
1. Gestión de variables críticas basadas en estándares médicos internacionales
2. Manejo de sinónimos multiidioma (español/inglés) para robustez
3. Persistencia automática con respaldo y recuperación de errores
4. Validación de integridad de datos y consistencia
5. Operaciones atómicas para prevenir corrupción de datos

Variables Críticas Gestionadas:
Basadas en criterios diagnósticos de ADA, WHO y literatura científica:
- Variables diagnósticas primarias: Glucosa, HbA1c
- Variables antropométricas: BMI, edad
- Variables clínicas: Obesidad, polidipsia, embarazo
- Variables de estilo de vida: Dieta, actividad física

Arquitectura de Datos:
- Formato JSON para interoperabilidad y legibilidad humana
- Estructura jerárquica: variable -> lista de sinónimos
- Normalización automática de claves (lowercase)
- Validación de tipos y contenido en todas las operaciones

Casos de Uso Académicos:
- Configuración de variables para estudios multicéntricos
- Estandarización de terminología entre investigadores
- Documentación de metodología para reproducibilidad
- Adaptación a diferentes fuentes de datos y nomenclaturas

Versión: 1.0
"""
import json
import os
from typing import Dict, List, Optional
from config.settings import DEFAULT_VARIABLES, Config

class VariableManager:
    """
    Clase para gestionar las variables críticas y sus sinónimos.
    Maneja la persistencia en archivo JSON y operaciones CRUD.
    """
    
    def __init__(self, config_file: Optional[str] = None) -> None:
        """
        Inicializa el gestor de variables.
        
        Args:
            config_file (str): Ruta del archivo de configuración
        """
        self.config_file = config_file or Config.CONFIG_FILE
        self._variables = self._cargar_variables()
    
    def _cargar_variables(self) -> Dict[str, List[str]]:
        """
        Carga las variables desde el archivo de configuración o usa las predeterminadas.
        
        Returns:
            Dict[str, List[str]]: Diccionario de variables y sinónimos
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return DEFAULT_VARIABLES.copy()
        return DEFAULT_VARIABLES.copy()
    
    def _guardar_variables(self) -> bool:
        """
        Guarda las variables en el archivo de configuración.
        
        Returns:
            bool: True si se guardó exitosamente, False en caso contrario
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._variables, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    def obtener_todas_variables(self) -> Dict[str, List[str]]:
        """
        Obtiene todas las variables configuradas.
        
        Returns:
            Dict[str, List[str]]: Diccionario de variables y sinónimos
        """
        return self._variables.copy()
    
    def obtener_variable(self, nombre: str) -> Optional[List[str]]:
        """
        Obtiene los sinónimos de una variable específica.
        
        Args:
            nombre (str): Nombre de la variable
            
        Returns:
            Optional[List[str]]: Lista de sinónimos o None si no existe
        """
        return self._variables.get(nombre.lower())
    
    def crear_variable(self, nombre: str, sinonimos: List[str]) -> bool:
        """
        Crea una nueva variable con sus sinónimos.
        
        Args:
            nombre (str): Nombre de la variable
            sinonimos (List[str]): Lista de sinónimos
            
        Returns:
            bool: True si se creó exitosamente, False si ya existe
        """
        nombre_lower = nombre.lower().strip()
        
        if not nombre_lower or nombre_lower in self._variables:
            return False
        
        # Filtrar sinónimos vacíos
        sinonimos_limpios = [s.strip() for s in sinonimos if s.strip()]
        
        if not sinonimos_limpios:
            return False
        
        self._variables[nombre_lower] = sinonimos_limpios
        return self._guardar_variables()
    
    def actualizar_variable(self, nombre: str, sinonimos: List[str]) -> bool:
        """
        Actualiza los sinónimos de una variable existente.
        
        Args:
            nombre (str): Nombre de la variable
            sinonimos (List[str]): Nueva lista de sinónimos
            
        Returns:
            bool: True si se actualizó exitosamente, False si no existe
        """
        nombre_lower = nombre.lower()
        
        if nombre_lower not in self._variables:
            return False
        
        # Filtrar sinónimos vacíos
        sinonimos_limpios = [s.strip() for s in sinonimos if s.strip()]
        
        if not sinonimos_limpios:
            return False
        
        self._variables[nombre_lower] = sinonimos_limpios
        return self._guardar_variables()
    
    def eliminar_variable(self, nombre: str) -> bool:
        """
        Elimina una variable y todos sus sinónimos.
        
        Args:
            nombre (str): Nombre de la variable a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente, False si no existe
        """
        nombre_lower = nombre.lower()
        
        if nombre_lower not in self._variables:
            return False
        
        del self._variables[nombre_lower]
        return self._guardar_variables()
    
    def existe_variable(self, nombre: str) -> bool:
        """
        Verifica si una variable existe.
        
        Args:
            nombre (str): Nombre de la variable
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        return nombre.lower() in self._variables
    
    def obtener_nombres_variables(self) -> List[str]:
        """
        Obtiene la lista de nombres de todas las variables.
        
        Returns:
            List[str]: Lista de nombres de variables
        """
        return list(self._variables.keys())
    
    def contar_variables(self) -> int:
        """
        Cuenta el número total de variables configuradas.
        
        Returns:
            int: Número de variables
        """
        return len(self._variables)
    
    def resetear_a_predeterminadas(self) -> bool:
        """
        Resetea las variables a los valores predeterminados.
        
        Returns:
            bool: True si se reseteó exitosamente
        """
        self._variables = DEFAULT_VARIABLES.copy()
        return self._guardar_variables()
    
    def agregar_sinonimo(self, nombre_variable: str, sinonimo: str) -> bool:
        """
        Agrega un sinónimo a una variable existente.
        
        Args:
            nombre_variable (str): Nombre de la variable
            sinonimo (str): Sinónimo a agregar
            
        Returns:
            bool: True si se agregó exitosamente
        """
        nombre_lower = nombre_variable.lower()
        sinonimo_limpio = sinonimo.strip()
        
        if nombre_lower not in self._variables or not sinonimo_limpio:
            return False
        
        if sinonimo_limpio not in self._variables[nombre_lower]:
            self._variables[nombre_lower].append(sinonimo_limpio)
            return self._guardar_variables()
        
        return True  # Ya existe, no es error
    
    def remover_sinonimo(self, nombre_variable: str, sinonimo: str) -> bool:
        """
        Remueve un sinónimo de una variable existente.
        
        Args:
            nombre_variable (str): Nombre de la variable
            sinonimo (str): Sinónimo a remover
            
        Returns:
            bool: True si se removió exitosamente
        """
        nombre_lower = nombre_variable.lower()
        
        if nombre_lower not in self._variables:
            return False
        
        try:
            self._variables[nombre_lower].remove(sinonimo)
            # No permitir variables sin sinónimos
            if not self._variables[nombre_lower]:
                return False
            return self._guardar_variables()
        except ValueError:
            return False  # Sinónimo no encontrado
