"""
Generador de Reportes Científicos para Análisis de Datasets de Diabetes

Este módulo implementa la generación automatizada de reportes estructurados para
análisis de variables críticas en datasets de investigación en diabetes mellitus.
Los reportes están diseñados para cumplir con estándares de documentación científica
y facilitar la redacción de publicaciones académicas.

Características del Sistema de Reportes:
1. Estructura estandarizada siguiendo convenciones de investigación médica
2. Métricas de calidad validadas para evaluación de datasets
3. Clasificación automática de variables según relevancia clínica
4. Generación de múltiples formatos (JSON, HTML, CSV) para diferentes usos

Métricas Implementadas:
- Cobertura de variables: Porcentaje de variables críticas detectadas
- Confianza promedio: Score de similitud de variables encontradas  
- Clasificación por confianza: Alta (≥0.9), Media (0.7-0.9), Baja (<0.7)
- Estado general del dataset: Excelente, Bueno, Regular, Deficiente

Aplicaciones Académicas:
- Documentación de metodología para sección "Materials and Methods"
- Generación de tablas descriptivas para manuscritos
- Reportes de calidad de datos para revisores
- Documentación de preprocesamiento para reproducibilidad

Versión: 1.0
"""
from typing import Dict, List, Any
from datetime import datetime
import pandas as pd

class ReportGenerator:
    """
    Generador de Reportes Científicos para Documentación de Análisis de Datasets.
    
    Esta clase implementa la generación automatizada de reportes estructurados
    que cumplen con estándares de documentación científica para investigación
    en diabetes mellitus y estudios epidemiológicos relacionados.
    
    Funcionalidades Principales:
    1. Generación de reportes completos con metadatos y timestamps
    2. Cálculo de métricas de calidad de datos validadas
    3. Clasificación automática de hallazgos según relevancia clínica
    4. Exportación en múltiples formatos para diferentes audiencias
    
    Estándares de Calidad Implementados:
    - Cobertura ≥80%: Excelente calidad de datos
    - Confianza ≥0.9: Alta precisión en detección de variables
    - Documentación completa: Trazabilidad y reproducibilidad
    
    Formatos de Salida:
    - JSON: Intercambio de datos y procesamiento automatizado
    - HTML: Visualización web y presentaciones
    - CSV: Análisis estadístico y tablas para manuscritos
    
    Aplicación en Investigación:
    Los reportes generados pueden utilizarse directamente en:
    - Sección "Data Sources and Variables" de manuscritos
    - Tablas suplementarias para revisores
    - Documentación de metodología para reproducibilidad
    - Reportes de calidad de datos para comités de ética
    
    Example:
        >>> generator = ReportGenerator()
        >>> reporte = generator.generar_reporte_completo(
        ...     info_archivo, info_dataset, resultados, estadisticas
        ... )
        >>> print(reporte['resumen']['estado_general'])  # 'excelente'
    
    Note:
        Los umbrales de calidad están basados en estándares establecidos
        en la literatura de investigación clínica y epidemiológica.
    """
    
    def __init__(self):
        """Inicializa el generador de reportes."""
        pass
    
    def generar_reporte_completo(
        self,
        info_archivo: Dict[str, Any],
        info_dataset: Dict[str, Any],
        resultados_busqueda: List[Dict],
        estadisticas: Dict[str, Any],
        sugerencias: List[str] = None
    ) -> Dict[str, Any]:
        """
        Genera un reporte completo del análisis.
        
        Args:
            info_archivo (Dict): Información del archivo procesado
            info_dataset (Dict): Información del dataset
            resultados_busqueda (List[Dict]): Resultados de búsqueda de variables
            estadisticas (Dict): Estadísticas del análisis
            sugerencias (List[str]): Sugerencias de mejora
            
        Returns:
            Dict: Reporte completo estructurado
        """
        timestamp = datetime.now()
        
        reporte = {
            'metadatos': {
                'timestamp': timestamp.isoformat(),
                'fecha_legible': timestamp.strftime("%d/%m/%Y %H:%M:%S"),
                'version_reporte': '1.0'
            },
            'archivo': info_archivo,
            'dataset': info_dataset,
            'analisis': {
                'resultados': resultados_busqueda,
                'estadisticas': estadisticas,
                'sugerencias': sugerencias or []
            },
            'resumen': self._generar_resumen(resultados_busqueda, estadisticas)
        }
        
        return reporte
    
    def _generar_resumen(self, resultados: List[Dict], estadisticas: Dict) -> Dict:
        """
        Genera un resumen ejecutivo del análisis.
        
        Args:
            resultados (List[Dict]): Resultados de búsqueda
            estadisticas (Dict): Estadísticas del análisis
            
        Returns:
            Dict: Resumen ejecutivo
        """
        variables_criticas = ['glucosa', 'bmi', 'edad', 'hba1c']
        variables_criticas_encontradas = [
            r['variable'] for r in resultados 
            if r['variable'] in variables_criticas and r['encontrada']
        ]
        
        # Clasificar variables por confianza
        alta_confianza = [r for r in resultados if r['encontrada'] and r['confianza'] >= 0.9]
        media_confianza = [r for r in resultados if r['encontrada'] and 0.7 <= r['confianza'] < 0.9]
        baja_confianza = [r for r in resultados if r['encontrada'] and r['confianza'] < 0.7]
        
        return {
            'cobertura_general': estadisticas['cobertura_porcentaje'],
            'variables_criticas_encontradas': len(variables_criticas_encontradas),
            'total_variables_criticas': len(variables_criticas),
            'confianza_promedio': estadisticas['confianza_promedio'],
            'clasificacion_confianza': {
                'alta': len(alta_confianza),
                'media': len(media_confianza),
                'baja': len(baja_confianza)
            },
            'estado_general': self._determinar_estado_general(estadisticas),
            'principales_hallazgos': self._generar_hallazgos_principales(resultados, estadisticas)
        }
    
    def _determinar_estado_general(self, estadisticas: Dict) -> str:
        """
        Determina el estado general del dataset basado en estadísticas.
        
        Args:
            estadisticas (Dict): Estadísticas del análisis
            
        Returns:
            str: Estado general (excelente, bueno, regular, deficiente)
        """
        cobertura = estadisticas['cobertura_porcentaje']
        confianza = estadisticas['confianza_promedio']
        
        if cobertura >= 80 and confianza >= 0.9:
            return 'excelente'
        elif cobertura >= 60 and confianza >= 0.8:
            return 'bueno'
        elif cobertura >= 40 and confianza >= 0.7:
            return 'regular'
        else:
            return 'deficiente'
    
    def _generar_hallazgos_principales(self, resultados: List[Dict], estadisticas: Dict) -> List[str]:
        """
        Genera una lista de hallazgos principales del análisis.
        
        Args:
            resultados (List[Dict]): Resultados de búsqueda
            estadisticas (Dict): Estadísticas del análisis
            
        Returns:
            List[str]: Lista de hallazgos principales
        """
        hallazgos = []
        
        # Cobertura
        cobertura = estadisticas['cobertura_porcentaje']
        if cobertura >= 80:
            hallazgos.append(f"Excelente cobertura de variables ({cobertura}%)")
        elif cobertura >= 60:
            hallazgos.append(f"Buena cobertura de variables ({cobertura}%)")
        else:
            hallazgos.append(f"Cobertura limitada de variables ({cobertura}%)")
        
        # Variables críticas
        variables_criticas = ['glucosa', 'bmi', 'edad', 'hba1c']
        criticas_encontradas = [
            r for r in resultados 
            if r['variable'] in variables_criticas and r['encontrada']
        ]
        
        if len(criticas_encontradas) == len(variables_criticas):
            hallazgos.append("Todas las variables críticas están presentes")
        elif len(criticas_encontradas) >= len(variables_criticas) * 0.75:
            hallazgos.append("La mayoría de variables críticas están presentes")
        else:
            hallazgos.append("Faltan variables críticas importantes")
        
        # Confianza
        confianza_promedio = estadisticas['confianza_promedio']
        if confianza_promedio >= 0.9:
            hallazgos.append("Alta confianza en las coincidencias encontradas")
        elif confianza_promedio >= 0.8:
            hallazgos.append("Confianza moderada en las coincidencias")
        else:
            hallazgos.append("Baja confianza en algunas coincidencias")
        
        # Variables especiales detectadas
        dieta_resultado = next((r for r in resultados if r['variable'] == 'dieta'), None)
        if dieta_resultado and dieta_resultado['encontrada']:
            if 'notas' in dieta_resultado and dieta_resultado['notas']:
                hallazgos.append(f"Información dietética detectada: {dieta_resultado['notas']}")
        
        return hallazgos
    
    def generar_reporte_csv(self, resultados: List[Dict]) -> str:
        """
        Genera un reporte en formato CSV.
        
        Args:
            resultados (List[Dict]): Resultados de búsqueda
            
        Returns:
            str: Contenido del reporte en formato CSV
        """
        # Preparar datos para CSV
        datos_csv = []
        for resultado in resultados:
            datos_csv.append({
                'Variable': resultado['variable'].capitalize(),
                'Encontrada': 'Sí' if resultado['encontrada'] else 'No',
                'Columna_Detectada': resultado.get('columna', ''),
                'Confianza': resultado['confianza'],
                'Sinonimo_Match': resultado.get('sinonimo_match', ''),
                'Notas': resultado.get('notas', '')
            })
        
        # Convertir a DataFrame y luego a CSV
        df = pd.DataFrame(datos_csv)
        return df.to_csv(index=False, encoding='utf-8')
    
    def generar_reporte_html(self, reporte_completo: Dict) -> str:
        """
        Genera un reporte en formato HTML.
        
        Args:
            reporte_completo (Dict): Reporte completo estructurado
            
        Returns:
            str: Contenido del reporte en formato HTML
        """
        html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Reporte de Análisis - Dataset de Diabetes</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: #2c5282; color: white; padding: 20px; border-radius: 5px; }}
                .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
                .success {{ color: #28a745; }}
                .warning {{ color: #ffc107; }}
                .danger {{ color: #dc3545; }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f8f9fa; }}
                .metric {{ display: inline-block; margin: 10px; padding: 15px; border-radius: 5px; background: #f8f9fa; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Reporte de Análisis - Dataset de Diabetes</h1>
                <p>Generado el: {reporte_completo['metadatos']['fecha_legible']}</p>
            </div>
            
            <div class="section">
                <h2>Información del Dataset</h2>
                <div class="metric">
                    <strong>Filas:</strong> {reporte_completo['dataset']['filas']:,}
                </div>
                <div class="metric">
                    <strong>Columnas:</strong> {reporte_completo['dataset']['columnas_total']}
                </div>
                <div class="metric">
                    <strong>Cobertura:</strong> {reporte_completo['analisis']['estadisticas']['cobertura_porcentaje']}%
                </div>
            </div>
            
            <div class="section">
                <h2>Resultados por Variable</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Variable</th>
                            <th>Estado</th>
                            <th>Columna Detectada</th>
                            <th>Confianza</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for resultado in reporte_completo['analisis']['resultados']:
            estado_class = 'success' if resultado['encontrada'] else 'danger'
            estado_texto = 'Encontrada' if resultado['encontrada'] else 'No encontrada'
            columna = resultado.get('columna', '-')
            confianza = f"{resultado['confianza']:.1%}" if resultado['encontrada'] else '-'
            
            html += f"""
                        <tr>
                            <td>{resultado['variable'].capitalize()}</td>
                            <td class="{estado_class}">{estado_texto}</td>
                            <td>{columna}</td>
                            <td>{confianza}</td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h2>Principales Hallazgos</h2>
                <ul>
        """
        
        for hallazgo in reporte_completo['resumen']['principales_hallazgos']:
            html += f"<li>{hallazgo}</li>"
        
        html += """
                </ul>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def generar_reporte_json(self, reporte_completo: Dict) -> str:
        """
        Genera un reporte en formato JSON.
        
        Args:
            reporte_completo (Dict): Reporte completo estructurado
            
        Returns:
            str: Contenido del reporte en formato JSON
        """
        import json
        return json.dumps(reporte_completo, indent=2, ensure_ascii=False)
    
    def calcular_metricas_avanzadas(self, resultados: List[Dict]) -> Dict:
        """
        Calcula métricas avanzadas del análisis.
        
        Args:
            resultados (List[Dict]): Resultados de búsqueda
            
        Returns:
            Dict: Métricas avanzadas
        """
        if not resultados:
            return {}
        
        # Distribución de confianza
        confianzas = [r['confianza'] for r in resultados if r['encontrada']]
        
        if confianzas:
            confianza_min = min(confianzas)
            confianza_max = max(confianzas)
            confianza_media = sum(confianzas) / len(confianzas)
        else:
            confianza_min = confianza_max = confianza_media = 0.0
        
        # Categorización por tipo de variable
        variables_demograficas = ['edad', 'embarazo']
        variables_clinicas = ['glucosa', 'bmi', 'hba1c', 'obesidad', 'polidipsia']
        variables_estilo_vida = ['dieta']
        
        demograficas_encontradas = sum(1 for r in resultados if r['variable'] in variables_demograficas and r['encontrada'])
        clinicas_encontradas = sum(1 for r in resultados if r['variable'] in variables_clinicas and r['encontrada'])
        estilo_vida_encontradas = sum(1 for r in resultados if r['variable'] in variables_estilo_vida and r['encontrada'])
        
        return {
            'distribucion_confianza': {
                'minima': round(confianza_min, 3),
                'maxima': round(confianza_max, 3),
                'promedio': round(confianza_media, 3)
            },
            'cobertura_por_categoria': {
                'demograficas': f"{demograficas_encontradas}/{len(variables_demograficas)}",
                'clinicas': f"{clinicas_encontradas}/{len(variables_clinicas)}",
                'estilo_vida': f"{estilo_vida_encontradas}/{len(variables_estilo_vida)}"
            },
            'total_coincidencias': len([r for r in resultados if r['encontrada']]),
            'total_variables_analizadas': len(resultados)
        }
