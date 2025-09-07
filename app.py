"""
Sistema de Análisis Automatizado para Variables en Datasets de Diabetes

Aplicación web para análisis automatizado de variables críticas en datasets de diabetes.
Utiliza técnicas de similitud textual para identificar y mapear variables clínicas.

Funcionalidades principales:
- Detección automática de variables críticas mediante análisis de similitud semántica
- Procesamiento de múltiples formatos de archivos (CSV, Excel)
- Generación de reportes detallados con métricas de calidad
- Interfaz web para parametrización y análisis interactivo
"""
from flask import Flask, render_template, request, jsonify
from config.settings import Config
from models.variable_manager import VariableManager
from services.file_processor import FileProcessor
from services.similarity_engine import SimilarityEngine
from services.report_generator import ReportGenerator
from utils.text_utils import limpiar_lista_sinonimos

# Inicializar aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Inicializar servicios
variable_manager = VariableManager()
file_processor = FileProcessor()
similarity_engine = SimilarityEngine()
report_generator = ReportGenerator()

@app.route('/')
def inicio():
    """Página principal de la aplicación"""
    return render_template('inicio.html')

@app.route('/parametrizacion')
def parametrizacion():
    """Página de parametrización de variables"""
    variables = variable_manager.obtener_todas_variables()
    return render_template('parametrizacion.html', variables=variables)

@app.route('/analisis')
def analisis():
    """Página de análisis de datasets"""
    return render_template('analisis.html')

# ==================== API ENDPOINTS ====================

@app.route('/api/variables', methods=['GET'])
def obtener_variables():
    """
    Obtiene todas las variables configuradas
    
    Returns:
        JSON: Diccionario de variables y sinónimos
    """
    try:
        variables = variable_manager.obtener_todas_variables()
        return jsonify(variables)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/variables/<variable_key>', methods=['POST'])
def actualizar_variable(variable_key):
    """
    Actualiza una variable existente
    
    Args:
        variable_key (str): Nombre de la variable a actualizar
        
    Returns:
        JSON: Resultado de la operación
    """
    try:
        data = request.get_json()
        
        if not data or 'sinonimos' not in data:
            return jsonify({'success': False, 'error': 'Datos inválidos'})
        
        # Limpiar sinónimos
        sinonimos_texto = ', '.join(data['sinonimos']) if isinstance(data['sinonimos'], list) else data['sinonimos']
        sinonimos = limpiar_lista_sinonimos(sinonimos_texto)
        
        if not sinonimos:
            return jsonify({'success': False, 'error': 'Debe proporcionar al menos un sinónimo válido'})
        
        success = variable_manager.actualizar_variable(variable_key, sinonimos)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Variable no encontrada'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/variables/<variable_key>', methods=['DELETE'])
def eliminar_variable(variable_key):
    """
    Elimina una variable
    
    Args:
        variable_key (str): Nombre de la variable a eliminar
        
    Returns:
        JSON: Resultado de la operación
    """
    try:
        success = variable_manager.eliminar_variable(variable_key)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Variable no encontrada'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/variables', methods=['POST'])
def crear_variable():
    """
    Crea una nueva variable
    
    Returns:
        JSON: Resultado de la operación
    """
    try:
        data = request.get_json()
        
        if not data or 'nombre' not in data or 'sinonimos' not in data:
            return jsonify({'success': False, 'error': 'Datos inválidos'})
        
        nombre = data['nombre'].strip()
        if not nombre:
            return jsonify({'success': False, 'error': 'El nombre de la variable no puede estar vacío'})
        
        # Limpiar sinónimos
        sinonimos_texto = ', '.join(data['sinonimos']) if isinstance(data['sinonimos'], list) else data['sinonimos']
        sinonimos = limpiar_lista_sinonimos(sinonimos_texto)
        
        if not sinonimos:
            return jsonify({'success': False, 'error': 'Debe proporcionar al menos un sinónimo válido'})
        
        success = variable_manager.crear_variable(nombre, sinonimos)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'La variable ya existe o el nombre es inválido'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analizar', methods=['POST'])
def analizar_dataset():
    """
    Endpoint principal para análisis automatizado de datasets de diabetes.
    
    Este endpoint implementa el algoritmo principal de análisis que:
    1. Procesa archivos subidos en formatos estándar (CSV, Excel)
    2. Aplica técnicas de similitud semántica para identificar variables críticas
    3. Genera métricas de calidad y confianza para cada variable detectada
    4. Produce un analisis estructurado
    
    Metodología:
    - Utiliza normalización de texto Unicode para comparaciones robustas
    - Implementa algoritmo de similitud basado en SequenceMatcher de Python
    - Aplica umbrales de confianza configurables para control de calidad
    - Maneja casos especiales como variables dietéticas distribuidas
    
    Variables críticas analizadas (según literatura médica):
    - Glucosa en ayunas (FPG): Indicador primario de diabetes
    - HbA1c: Hemoglobina glucosilada, estándar de oro para diagnóstico
    - BMI: Índice de masa corporal, factor de riesgo establecido
    - Edad: Variable demográfica crítica
    - Factores dietéticos: Consumo de frutas y vegetales
    
    Returns:
        JSON: Estructura de respuesta con:
            - success (bool): Estado de la operación
            - archivo (str): Nombre del archivo procesado
            - filas/columnas_total (int): Dimensiones del dataset
            - resultados (List[Dict]): Detalle de variables encontradas
            - estadisticas (Dict): Métricas de cobertura y confianza
            - sugerencias (List[str]): Recomendaciones para mejora
            - reporte_completo (Dict): Reporte estructurado completo
            
    Raises:
        400: Archivo no válido o formato no soportado
        413: Archivo excede límite de tamaño
        500: Error interno del servidor
        
    """
    try:
        # Verificar que se subió un archivo
        if 'archivo' not in request.files:
            return jsonify({'success': False, 'error': 'No se subió ningún archivo'})
        
        archivo = request.files['archivo']
        if not archivo or archivo.filename == '':
            return jsonify({'success': False, 'error': 'No se seleccionó ningún archivo'})
        
        # Obtener umbral personalizado si se envió
        umbral_personalizado = request.form.get('umbral_confianza')
        if umbral_personalizado:
            try:
                umbral_personalizado = float(umbral_personalizado)
                # Validar que esté en rango válido
                if not (0.0 <= umbral_personalizado <= 1.0):
                    umbral_personalizado = None
            except ValueError:
                umbral_personalizado = None
        
        # Procesar archivo
        df, filepath, error = file_processor.procesar_archivo_subido(archivo)
        if error:
            return jsonify({'success': False, 'error': error})
        
        try:
            # Obtener información del dataset
            info_dataset = file_processor.obtener_info_dataset(df)
            advertencias = file_processor.validar_columnas(df)
            
            # Obtener variables configuradas
            variables_config = variable_manager.obtener_todas_variables()
            
            # Ajustar umbral si se proporcionó uno personalizado
            if umbral_personalizado:
                similarity_engine.ajustar_umbral(umbral_personalizado)
            
            # Realizar búsqueda de variables
            resultados_busqueda = similarity_engine.buscar_todas_variables(
                variables_config, 
                info_dataset['columnas']
            )
            
            # Calcular estadísticas
            estadisticas = similarity_engine.obtener_estadisticas_busqueda(resultados_busqueda)
            
            # Generar sugerencias
            sugerencias = similarity_engine.obtener_sugerencias_mejora(
                resultados_busqueda, 
                info_dataset['columnas']
            )
            
            # Información del archivo (obtener tamaño de manera segura)
            import os
            tamaño_mb = 0
            if filepath and os.path.exists(filepath):
                tamaño_mb = round(os.path.getsize(filepath) / 1024 / 1024, 2)
            
            info_archivo = {
                'nombre': str(archivo.filename),
                'tamaño_mb': float(tamaño_mb),
                'extension': str(archivo.filename.split('.')[-1] if '.' in archivo.filename else '')
            }
            
            # Generar reporte completo
            reporte_completo = report_generator.generar_reporte_completo(
                info_archivo=info_archivo,
                info_dataset=info_dataset,
                resultados_busqueda=resultados_busqueda,
                estadisticas=estadisticas,
                sugerencias=sugerencias
            )
            
            # Preparar respuesta para el frontend
            respuesta = {
                'success': True,
                'archivo': archivo.filename,
                'filas': info_dataset['filas'],
                'columnas_total': info_dataset['columnas_total'],
                'columnas': info_dataset['columnas'],
                'resultados': resultados_busqueda,
                'estadisticas': estadisticas,
                'sugerencias': sugerencias,
                'advertencias': advertencias,
                'reporte_completo': reporte_completo
            }
            
            return jsonify(respuesta)
            
        finally:
            # Limpiar archivo temporal
            if filepath:
                file_processor.limpiar_archivo(filepath)
                
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error interno del servidor: {str(e)}'}), 500

@app.route('/api/estadisticas', methods=['GET'])
def obtener_estadisticas_sistema():
    """
    Obtiene estadísticas generales del sistema
    
    Returns:
        JSON: Estadísticas del sistema
    """
    try:
        estadisticas = {
            'total_variables_configuradas': variable_manager.contar_variables(),
            'nombres_variables': variable_manager.obtener_nombres_variables(),
            'umbral_similitud_actual': similarity_engine.umbral_similitud,
            'formatos_soportados': list(Config.ALLOWED_EXTENSIONS),
            'tamaño_maximo_archivo_mb': Config.MAX_CONTENT_LENGTH / (1024 * 1024)
        }
        
        return jsonify(estadisticas)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/configuracion/umbral', methods=['POST'])
def ajustar_umbral_similitud():
    """
    Ajusta el umbral de similitud del motor de búsqueda
    
    Returns:
        JSON: Resultado de la operación
    """
    try:
        data = request.get_json()
        
        if not data or 'umbral' not in data:
            return jsonify({'success': False, 'error': 'Umbral no especificado'})
        
        nuevo_umbral = float(data['umbral'])
        
        if not (0.0 <= nuevo_umbral <= 1.0):
            return jsonify({'success': False, 'error': 'El umbral debe estar entre 0.0 y 1.0'})
        
        success = similarity_engine.ajustar_umbral(nuevo_umbral)
        
        if success:
            return jsonify({'success': True, 'nuevo_umbral': nuevo_umbral})
        else:
            return jsonify({'success': False, 'error': 'Error al ajustar umbral'})
            
    except ValueError:
        return jsonify({'success': False, 'error': 'Valor de umbral inválido'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/variables/resetear', methods=['POST'])
def resetear_variables():
    """
    Resetea las variables a los valores predeterminados
    
    Returns:
        JSON: Resultado de la operación
    """
    try:
        success = variable_manager.resetear_a_predeterminadas()
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Error al resetear variables'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(404)
def pagina_no_encontrada(error):
    """Maneja errores 404"""
    return render_template('base.html'), 404

@app.errorhandler(413)
def archivo_muy_grande(error):
    """Maneja errores de archivo muy grande"""
    return jsonify({
        'success': False, 
        'error': f'El archivo es demasiado grande. Máximo permitido: {Config.MAX_CONTENT_LENGTH / (1024 * 1024):.1f} MB'
    }), 413

@app.errorhandler(500)
def error_interno_servidor(error):
    """Maneja errores internos del servidor"""
    return jsonify({
        'success': False, 
        'error': 'Error interno del servidor. Intente nuevamente.'
    }), 500

# ==================== CONTEXTO DE TEMPLATES ====================

@app.context_processor
def inyectar_variables_globales():
    """Inyecta variables globales en todos los templates"""
    return {
        'total_variables': variable_manager.contar_variables(),
        'umbral_similitud': similarity_engine.umbral_similitud
    }

# ==================== PUNTO DE ENTRADA ====================

if __name__ == '__main__':
    """
    Punto de entrada principal de la aplicación.
    
    Configuración recomendada:
    - debug=True: Habilitado para desarrollo, desactivar en producción
    - host='127.0.0.1': Localhost, cambiar a '0.0.0.0' para acceso externo
    - port=5000: Puerto estándar Flask
    
    """
    app.run(debug=True, host='127.0.0.1', port=5000)