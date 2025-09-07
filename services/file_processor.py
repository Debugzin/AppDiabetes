"""
Procesador de archivos para diferentes formatos de datasets
"""
import os
import pandas as pd
from typing import Optional, Tuple, List, Dict, Any, Union
from werkzeug.utils import secure_filename
from config.settings import Config, SUPPORTED_READERS

class FileProcessor:
    """
    Clase para procesar archivos de datasets en diferentes formatos.
    Maneja la carga, validación y extracción de información de archivos.
    """
    
    def __init__(self, upload_folder: Optional[str] = None) -> None:
        """
        Inicializa el procesador de archivos.
        
        Args:
            upload_folder (str): Carpeta para archivos temporales
        """
        self.upload_folder = upload_folder or Config.UPLOAD_FOLDER
        self.allowed_extensions = Config.ALLOWED_EXTENSIONS
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def es_extension_permitida(self, filename: str) -> bool:
        """
        Verifica si la extensión del archivo está permitida.
        
        Args:
            filename (str): Nombre del archivo
            
        Returns:
            bool: True si la extensión está permitida
        """
        if not filename:
            return False
        
        # Obtener extensión en minúsculas
        _, ext = os.path.splitext(filename.lower())
        return ext in self.allowed_extensions
    
    def obtener_metodo_lectura(self, filename: str) -> Optional[str]:
        """
        Obtiene el método de pandas para leer el archivo según su extensión.
        
        Args:
            filename (str): Nombre del archivo
            
        Returns:
            Optional[str]: Nombre del método de pandas o None si no está soportado
        """
        if not filename:
            return None
        
        _, ext = os.path.splitext(filename.lower())
        return SUPPORTED_READERS.get(ext)
    
    def guardar_archivo_temporal(self, archivo) -> Optional[str]:
        """
        Guarda un archivo subido temporalmente.
        
        Args:
            archivo: Archivo subido (FileStorage de Flask)
            
        Returns:
            Optional[str]: Ruta del archivo guardado o None si hay error
        """
        if not archivo or not archivo.filename:
            return None
        
        if not self.es_extension_permitida(archivo.filename):
            return None
        
        try:
            filename = secure_filename(archivo.filename)
            filepath = os.path.join(self.upload_folder, filename)
            archivo.save(filepath)
            return filepath
        except Exception as e:
            return None
    
    def leer_dataset(self, filepath: str) -> Optional[pd.DataFrame]:
        """
        Lee un dataset desde un archivo.
        
        Args:
            filepath (str): Ruta del archivo
            
        Returns:
            Optional[pd.DataFrame]: DataFrame con los datos o None si hay error
        """
        if not os.path.exists(filepath):
            return None
        
        filename = os.path.basename(filepath)
        metodo = self.obtener_metodo_lectura(filename)
        
        if not metodo:
            return None
        
        try:
            if metodo == "read_csv":
                return pd.read_csv(filepath)
            elif metodo == "read_csv_tab":
                return pd.read_csv(filepath, sep="\t")
            elif metodo == "read_excel":
                return pd.read_excel(filepath, engine="openpyxl")
            else:
                return None
        except Exception as e:
            return None
    
    def procesar_archivo_subido(self, archivo) -> Tuple[Optional[pd.DataFrame], Optional[str], Optional[str]]:
        """
        Procesa un archivo subido completamente: guarda, lee y limpia.
        
        Args:
            archivo: Archivo subido (FileStorage de Flask)
            
        Returns:
            Tuple[Optional[pd.DataFrame], Optional[str], Optional[str]]: 
            (DataFrame, filepath, error_message)
        """
        # Validar archivo
        if not archivo or not archivo.filename:
            return None, None, "No se subió ningún archivo"
        
        if not self.es_extension_permitida(archivo.filename):
            return None, None, f"Formato de archivo no soportado. Use: {', '.join(self.allowed_extensions)}"
        
        # Guardar temporalmente
        filepath = self.guardar_archivo_temporal(archivo)
        if not filepath:
            return None, None, "Error al guardar el archivo temporalmente"
        
        # Leer dataset
        df = self.leer_dataset(filepath)
        if df is None:
            self.limpiar_archivo(filepath)
            return None, None, "Error al leer el archivo. Verifique el formato."
        
        # Validar que tenga datos
        if df.empty:
            self.limpiar_archivo(filepath)
            return None, None, "El archivo está vacío"
        
        return df, filepath, None
    
    def limpiar_archivo(self, filepath: str) -> bool:
        """
        Elimina un archivo temporal.
        
        Args:
            filepath (str): Ruta del archivo a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            return False
    
    def obtener_info_dataset(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Obtiene información básica del dataset.
        
        Args:
            df (pd.DataFrame): DataFrame a analizar
            
        Returns:
            dict: Información del dataset
        """
        # Convertir tipos de datos a strings para serialización JSON
        tipos_datos_serializables = {}
        for col, dtype in df.dtypes.items():
            tipos_datos_serializables[str(col)] = str(dtype)
        
        return {
            'filas': int(df.shape[0]),
            'columnas_total': int(df.shape[1]),
            'columnas': [str(col) for col in df.columns.tolist()],
            'tipos_datos': tipos_datos_serializables,
            'memoria_mb': round(float(df.memory_usage(deep=True).sum() / 1024 / 1024), 2)
        }
    
    def validar_columnas(self, df: pd.DataFrame) -> List[str]:
        """
        Valida las columnas del dataset y retorna advertencias.
        
        Args:
            df (pd.DataFrame): DataFrame a validar
            
        Returns:
            List[str]: Lista de advertencias
        """
        advertencias = []
        
        # Verificar columnas duplicadas
        columnas_duplicadas = df.columns.duplicated()
        if columnas_duplicadas.any():
            advertencias.append("El dataset tiene columnas con nombres duplicados")
        
        # Verificar columnas vacías
        columnas_vacias = df.columns[df.isnull().all()].tolist()
        if columnas_vacias:
            advertencias.append(f"Columnas completamente vacías: {', '.join(columnas_vacias)}")
        
        # Verificar nombres de columnas problemáticos
        columnas_problematicas = []
        for col in df.columns:
            if not isinstance(col, str) or not col.strip():
                columnas_problematicas.append(str(col))
        
        if columnas_problematicas:
            advertencias.append(f"Columnas con nombres problemáticos: {', '.join(columnas_problematicas)}")
        
        return advertencias
