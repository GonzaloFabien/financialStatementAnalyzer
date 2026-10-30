import os
import xml.etree.ElementTree as ET
from datetime import datetime

def encontrar_contextos_xbrl(root, año_buscado):
    """
    Escanea la taxonomía XBRL y devuelve dos listas de IDs de contextos para el año:
    1. duration_ids: Para Estado de Resultados / Flujos (ej. Revenues, Sales, NetIncome) -> ~365 días
    2. instant_ids: Para Balance General (ej. Assets, Liabilities, Equity) -> Fecha de corte
    """
    año_str = str(año_buscado).strip()
    duration_ids = []
    instant_ids = []

    # Buscar todos los nodos <context> sin importar el prefijo del namespace
    for context in root.findall('.//{*}context'):
        context_id = context.get('id')
        if not context_id:
            continue

        # FILTRO CRÍTICO: Ignorar contextos con dimensiones/segmentos para evitar duplicar valores de subsidiarias
        entity = context.find('.//{*}entity')
        if entity is not None and entity.find('.//{*}segment') is not None:
            continue

        period = context.find('.//{*}period')
        if period is None:
            continue

        # 1. Procesar contextos DURATION (Rangos de fecha para Ingresos/Gastos)
        start_node = period.find('.//{*}startDate')
        end_node = period.find('.//{*}endDate')
        
        if start_node is not None and end_node is not None and start_node.text and end_node.text:
            start_txt = start_node.text.strip()
            end_txt = end_node.text.strip()

            # El año fiscal de reporte suele terminar en el año buscado (ej: 2024-12-31)
            if end_txt.startswith(año_str):
                try:
                    start_dt = datetime.strptime(start_txt, "%Y-%m-%d")
                    end_dt = datetime.strptime(end_txt, "%Y-%m-%d")
                    dias = (end_dt - start_dt).days
                    
                    # Rango anual estándar de EE.UU. (350 a 375 días)
                    if 350 <= dias <= 375:
                        if context_id not in duration_ids:
                            duration_ids.append(context_id)
                except ValueError:
                    # Contingencia por si el formato de fecha cambia
                    if context_id not in duration_ids:
                        duration_ids.append(context_id)

        # 2. Procesar contextos INSTANT (Fechas específicas para Activos/Pasivos)
        instant_node = period.find('.//{*}instant')
        if instant_node is not None and instant_node.text:
            inst_txt = instant_node.text.strip()
            if inst_txt.startswith(año_str):
                if context_id not in instant_ids:
                    instant_ids.append(context_id)
    #Ok esto desmuestra que sí es una dupla y está retornando dos variables:
    print(f"{año_buscado} | duration = {duration_ids} | instante = {instant_ids}")
    return duration_ids, instant_ids


def extraer_datos_financieros(ruta_archivo, año_buscado):
    if not os.path.exists(ruta_archivo):
        return "El archivo especificado no existe."

    try:
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()
    except Exception as e:
        return f"Error leyendo el archivo XML: {e}"

    # Obtener los IDs correspondientes al año de forma limpia
    ctx_duration, ctx_instant = encontrar_contextos_xbrl(root, año_buscado)

    # Lista de etiquetas prioritarias de US-GAAP para Revenue (Ventas)
    tags_revenue = [
        'RevenueFromContractWithCustomerExcludingAssessedTax',
        'SalesRevenueNet',
        'Revenues',
        'SalesRevenueGoodsNet'
    ]

    # Diccionario para guardar lo que encontremos
    resultados = {"Revenue": None, "ContextRef_Usado": None}

    # Búsqueda en una sola pasada por el XML
    for elemento in root.iter():
        tag_local = elemento.tag.split('}')[-1]

        if tag_local in tags_revenue:
            ref_contexto = elemento.get('contextRef')
            
            # REGLA CONTABLE: El Revenue DEBE pertenecer a un contexto de DURACIÓN (flujo anual)
            if ref_contexto in ctx_duration:
                valor_texto = elemento.text
                if valor_texto:
                    try:
                        # Convertir de texto científico/float a entero limpio
                        valor_numerico = int(float(valor_texto.strip()))
                        resultados["Revenue"] = valor_numerico
                        resultados["ContextRef_Usado"] = ref_contexto
                        # Si encuentra el tag prioritario principal, podemos romper el ciclo
                        break 
                    except ValueError:
                        continue

    return resultados


