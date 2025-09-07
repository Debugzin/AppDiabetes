"""
Configuración del Sistema de Análisis de Variables en Diabetes

Configuraciones centralizadas del sistema:
- Parámetros del algoritmo de similitud
- Variables críticas predefinidas
- Configuraciones de seguridad y límites

Variables Críticas:
1. VARIABLES DIAGNÓSTICAS: Glucosa, HbA1c
2. VARIABLES ANTROPOMÉTRICAS: BMI, Edad
3. VARIABLES CLÍNICAS: Polidipsia, Obesidad
4. VARIABLES DE ESTILO DE VIDA: Dieta, Embarazo

Umbral de similitud por defecto: 0.6
"""
import os

# Configuración de la aplicación Flask
class Config:
    SECRET_KEY = 'diabetes_app_key_2024'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    
    # Configuración de archivos
    ALLOWED_EXTENSIONS = {'.csv', '.xlsx', '.xls'}
    CONFIG_FILE = 'variables_config.json'
    
    # Configuración del motor de similitud
    SIMILARITY_THRESHOLD = 0.6
    
    @staticmethod
    def init_app(app):
        """Inicializa configuraciones específicas de la app"""
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Variables críticas predefinidas para estudios de diabetes
DEFAULT_VARIABLES = {
    # VARIABLE DIAGNÓSTICA PRIMARIA
    # Glucosa plasmática en ayunas
    "glucosa": [
        "glucosa", "glucemia", "glucose", "blood glucose", 
        "glucosa mg dl", "fpg", "fasting plasma glucose", 
        "azucar en sangre", "glc", "glucose_mg_dl", "Glucose"
    ],
    
    # VARIABLE ANTROPOMÉTRICA
    # Índice de masa corporal
    "bmi": [
        "bmi", "imc", "indice de masa corporal", 
        "body mass index", "bmi_calculado", "BMI"
    ],
    
    # VARIABLE DEMOGRÁFICA
    # Edad del paciente
    "edad": [
        "edad", "age", "years", "anios", "años", 
        "edad_paciente", "patient_age", "Age"
    ],
    
    # VARIABLE DIAGNÓSTICA
    # Hemoglobina glucosilada
    "hba1c": [
        "hba1c", "hemoglobina glucosilada", "hemoglobina glicosilada", 
        "a1c", "hemoglobina_a1c", "glycated_hemoglobin"
    ],
    
    # VARIABLE DE ESTILO DE VIDA
    # Información dietética
    "dieta": [
        "dieta", "diet", "vegetales", "verduras", "frutas", 
        "consumo de frutas", "consumo de vegetales", "vegetable intake", 
        "fruit intake", "consumo_frutas_diario", "consumo_vegetales_diario"
    ],
    
    # VARIABLE CLÍNICA
    # Diagnóstico de obesidad
    "obesidad": [
        "obesidad", "obesity", "obese", "diagnostico obesidad",
        "diagnostico_obesidad", "obesity_diagnosis"
    ],
    
    # SÍNTOMA CLÍNICO
    # Sed excesiva
    "polidipsia": [
        "polidipsia", "polydipsia", "sed excesiva", "excessive thirst",
        "sed_excesiva", "excessive_thirst"
    ],
    
    # VARIABLE DE ESTADO
    # Estado de embarazo
    "embarazo": [
        "embarazo", "pregnancy", "pregnant", "gestacion", "gestación",
        "estado_embarazo", "pregnancy_status"
    ]
}

# Lectores de archivos soportados
SUPPORTED_READERS = {
    ".csv": "read_csv",
    ".tsv": "read_csv_tab",
    ".xlsx": "read_excel",
    ".xls": "read_excel",
}
