import os
import xml.etree.ElementTree as ET
from datetime import datetime

def resolver_contextos_por_año(root, año_buscado):
    """
    Escanea el XML y clasifica los contextos del año buscado en dos grupos:
    1. Contextos INSTANT (cierres instantáneos a fecha oficial)
    2. Contextos DURATION (que representen un rango de año completo ~365 días)
    """
    año_str = str(año_buscado)
    contextos_instant = set()
    contextos_duration = set()

    for context in root.findall('.//{*}context'):
        context_id = context.get('id')
        period = context.find('.//{*}period')
        if period is None:
            continue

        # 1. Intentar capturar nodos de tipo INSTANT
        instant_node = period.find('.//{*}instant')
        if instant_node is not None and instant_node.text:
            inst_txt = instant_node.text.strip()
            if inst_txt.startswith(año_str):
                contextos_instant.add(context_id)
            continue

        # 2. Intentar capturar nodos de tipo DURATION (Rangos anuales de ~365 días)
        start_node = period.find('.//{*}startDate')
        end_node = period.find('.//{*}endDate')
        if start_node is not None and end_node is not None and start_node.text and end_node.text:
            start_txt = start_node.text.strip()
            end_txt = end_node.text.strip()

            if end_txt.startswith(año_str):
                try:
                    fecha_inicio = datetime.strptime(start_txt, "%Y-%m-%d")
                    fecha_fin = datetime.strptime(end_txt, "%Y-%m-%d")
                    diferencia_dias = (fecha_fin - fecha_inicio).days
                    # Un año fiscal estándar/variable se comprende en este rango de días
                    if 350 <= diferencia_dias <= 375:
                        contextos_duration.add(context_id)
                except ValueError:
                    continue

    return contextos_instant, contextos_duration


def extraer_revenue_flexible_us_gaap(ruta_archivo, año_buscado):
    """
    Busca Revenue bajo contextos INSTANT. Si no encuentra coincidencias, 
    usa la contingencia DURATION para extraer el dato consolidado anual.
    """
    if not os.path.exists(ruta_archivo):
        return "Archivo no existe"

    try:
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()
    except Exception as e:
        return f"Error leyendo XML: {e}"

    # Clasificamos dinámicamente los contextos disponibles
    ctx_instant, ctx_duration = resolver_contextos_por_año(root, año_buscado)

    # Etiquetas US-GAAP oficiales para Revenue mapeadas jerárquicamente
    tags_revenue = [
        'SalesRevenueNet',
        'Revenues',
        'RevenueFromContractWithCustomerExcludingAssessedTax',
        'SalesRevenueGoodsNet',
        'RevenuesNetOfInterestExpense'
    ]

    hallazgos_instant = {}
    hallazgos_duration = {}

    # Mapeo de elementos en una sola pasada
    for elemento in root.iter():
        tag_local = elemento.tag.split('}')[-1]

        if tag_local in tags_revenue:
            ref_contexto = elemento.get('contextRef')
            valor_texto = elemento.text
            if not valor_texto:
                continue

            try:
                valor_numerico = int(float(valor_texto.strip()))
                
                # Clasificar si cae en la categoría INSTANT asignada
                if ref_contexto in ctx_instant and tag_local not in hallazgos_instant:
                    hallazgos_instant[tag_local] = (valor_numerico, ref_contexto)
                
                # Clasificar si cae en la categoría DURATION asignada
                if ref_contexto in ctx_duration and tag_local not in hallazgos_duration:
                    hallazgos_duration[tag_local] = (valor_numerico, ref_contexto)
            except ValueError:
                continue

    # PRIORIDAD 1: Intentar retornar el Revenue detectado bajo esquema INSTANT
    for tag in tags_revenue:
        if tag in hallazgos_instant:
            valor, ctx_id = hallazgos_instant[tag]
            print(f"-> [ÉXITO INSTANT] Detectado en '{tag}' | ContextRef: {ctx_id}")
            return valor

    # PRIORIDAD 2: Contingencia automática si fallan los Instant (Muestra tu caso real: FD2017Q4YTD)
    for tag in tags_revenue:
        if tag in hallazgos_duration:
            valor, ctx_id = hallazgos_duration[tag]
            print(f"-> [FALLBACK DURATION] Detectado en '{tag}' | ContextRef: {ctx_id}")
            return valor

    return "No se localizó ningún Revenue bajo esquemas Instant ni Duration calificados"


# =====================================================================
# CONFIGURACIÓN DE TU BÚSQUEDA FILTRADA (REVENUES INTELLIGENT)
# =====================================================================

# Lista de tus años a buscar
años_a_buscar = ["2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]

# DISCRIMINACIÓN: Define aquí la empresa que vas a procesar
empresa_a_buscar = "clorox"

# Ruta de tu carpeta con los archivos XML
directorio_base = "../data_xml"

print(f"--- EJECUTANDO EXTRACTOR REVENUE CON CONTINGENCIA DURATION (FILTRO: {empresa_a_buscar.upper()}) ---")

for año in años_a_buscar:
    nombre_importacion = f"/{empresa_a_buscar}{año}.xml"
    ruta_completa = f"{directorio_base}{nombre_importacion}"
    
    resultado = extraer_revenue_flexible_us_gaap(ruta_completa, año)
    
    nombre_consola = f"{empresa_a_buscar}{año}.xml"
    print(f"{nombre_consola} : {resultado}")
    print("-" * 75)
