# Sistema de Análisis Automatizado para Variables Críticas en Datasets de Diabetes

## Resumen Ejecutivo

Este sistema implementa una solución automatizada para la identificación y análisis de variables críticas en datasets de investigación en diabetes mellitus. Utiliza técnicas de procesamiento de lenguaje natural y algoritmos de similitud semántica para detectar automáticamente variables clínicas relevantes, facilitando el preprocesamiento de datos y la documentación metodológica para publicaciones científicas.

## Características Principales

### 🔬 **Análisis Científico Automatizado**
- Detección automática de variables críticas basada en estándares ADA/WHO
- Algoritmos de similitud semántica optimizados para terminología médica
- Soporte multiidioma (español/inglés) para estudios internacionales
- Métricas de calidad validadas para evaluación de datasets

### 📊 **Procesamiento de Datos Robusto**
- Soporte para múltiples formatos: CSV, Excel (XLS/XLSX)
- Validación automática de integridad de datos
- Manejo de casos especiales (variables dietéticas distribuidas)
- Generación de reportes estructurados para documentación científica

### 🎯 **Variables Críticas Predefinidas**
Basadas en literatura médica y criterios diagnósticos establecidos:
- **Diagnósticas primarias**: Glucosa plasmática, HbA1c
- **Antropométricas**: BMI, edad
- **Clínicas**: Obesidad, polidipsia, embarazo
- **Estilo de vida**: Dieta, actividad física

## Arquitectura del Sistema

```
diabetes-analyzer/
├── app.py                 # Aplicación Flask principal
├── config/
│   └── settings.py       # Configuraciones y variables críticas
├── models/
│   └── variable_manager.py   # Gestión de variables y sinónimos
├── services/
│   ├── file_processor.py     # Procesamiento de archivos
│   ├── similarity_engine.py  # Motor de similitud semántica
│   └── report_generator.py   # Generación de reportes científicos
├── utils/
│   └── text_utils.py        # Utilidades de procesamiento de texto
└── templates/              # Interfaz web
```

## Metodología Científica

### Algoritmo de Similitud
- **Base algorítmica**: Ratcliff-Obershelp (implementado en difflib.SequenceMatcher)
- **Preprocesamiento**: Normalización Unicode y limpieza de caracteres especiales
- **Umbral por defecto**: 0.6
- **Optimizaciones**: Manejo especial para variables dietéticas distribuidas

### Métricas de Calidad
- **Cobertura**: Porcentaje de variables críticas detectadas
- **Confianza**: Score de similitud promedio [0.0, 1.0]
- **Clasificación**: Alta (≥0.9), Media (0.7-0.9), Baja (<0.7)
- **Estado general**: Excelente, Bueno, Regular, Deficiente

### Cálculo del Nivel de Confianza

#### Definición Matemática
La aplicación define la confianza de detección de cada variable como el máximo valor de similitud encontrado en estas comparaciones. Matemáticamente, si **C** es el conjunto de columnas normalizadas y **S_V** el conjunto de sinónimos de la variable **V**, la confianza se calcula como:

**Confianza(V) = max(c∈C,s∈S_V) sim(c,s)**

donde **sim(c,s)** corresponde a la similitud entre una columna **c** y un sinónimo **s**. Si este valor supera un umbral mínimo, el cual por defecto está configurado en **0.6**, la variable se considera detectada.

#### Proceso de Cálculo
1. **Normalización de texto**: Se eliminan acentos, se convierte a minúsculas y se limpian caracteres especiales
2. **Comparación exhaustiva**: Se compara cada columna normalizada con todos los sinónimos de cada variable crítica
3. **Algoritmo de similitud**: Se utiliza Ratcliff-Obershelp para obtener un valor entre 0.0 (sin similitud) y 1.0 (idéntico)
4. **Selección del máximo**: Se toma el mayor score encontrado para cada variable
5. **Aplicación del umbral**: Solo se consideran detectadas las variables que superen el umbral de 0.6

#### Ejemplo de Cálculo
- **Columna del dataset**: "blood_glucose_level"  
- **Sinónimo de variable**: "blood glucose"
- **Después de normalización**: "blood glucose level" vs "blood glucose"
- **Score calculado**: 0.812 (81.2% de similitud)
- **Resultado**: ✅ Detectada (supera umbral de 0.6)

## Instalación y Configuración

### Requisitos del Sistema
```bash
Python >= 3.8
Flask >= 2.0
pandas >= 1.3
openpyxl >= 3.0
```

### Instalación
```bash
# Descargar el proyecto
# Instalar dependencias
pip install -r requirements.txt
# Ejecutar la aplicación
python app.py
```

### Configuración
El sistema utiliza variables críticas predefinidas en `config/settings.py`. Para estudios específicos, estas pueden personalizarse mediante la interfaz web o editando el archivo de configuración.

## Uso en Investigación

### Para Investigadores
1. **Carga de datos**: Suba su dataset en formato CSV o Excel
2. **Análisis automático**: El sistema identifica variables críticas automáticamente
3. **Evaluación de calidad**: Revise métricas de cobertura y confianza
4. **Documentación**: Exporte reportes para su manuscrito

### Para Revisores
- Los reportes generados incluyen toda la información necesaria para evaluar la calidad de los datos
- Métricas estandarizadas facilitan la comparación entre estudios
- Documentación completa de metodología para reproducibilidad

## Aplicaciones Académicas

### Descripción del Sistema
El sistema utiliza algoritmos de similitud semántica para identificar automáticamente 
variables críticas en datasets de diabetes. Analiza variables diagnósticas 
(glucosa, HbA1c), antropométricas (BMI, edad) y clínicas relevantes.

### Tablas Descriptivas
El sistema genera automáticamente tablas con:
- Variables detectadas y sus niveles de confianza
- Cobertura por categorías de variables
- Métricas de calidad del dataset

## Validación y Calidad

### Estándares Implementados
- Validación de formatos de archivo
- Control de calidad de datos
- Documentación completa

### Control de Calidad
- Validación automática de formatos de archivo
- Detección de columnas duplicadas o vacías
- Verificación de integridad de datos
- Generación de advertencias y sugerencias


## Contribuciones

Para contribuir al desarrollo del sistema, contacte al equipo de desarrollo.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - vea el archivo [LICENSE](LICENSE) para detalles.

## Contacto

Para preguntas o colaboraciones, contacte al equipo de desarrollo.


---

*Sistema desarrollado para facilitar la investigación en diabetes mellitus y mejorar la calidad de la documentación científica.*