import os
import xml.etree.ElementTree as ET
from datetime import datetime

def encontrar_id_balance_general(root, año_buscado):
    """
    PASO 1 y 2: Identifica la fecha exacta de cierre del año fiscal actual 
    inspeccionando los periodos de ~365 días (Duration).
    PASO 3: Busca el contexto de tipo 'instant' que coincida exactamente 
    con esa fecha encontrada.
    """
    año_str = str(año_buscado)
    fecha_cierre_oficial = None

    # Primero: Busquemos el contexto de tipo Duration del año completo actual
    for context in root.findall('.//{*}context'):
        period = context.find('.//{*}period')
        if period is not None:
            start_node = period.find('.//{*}startDate')
            end_node = period.find('.//{*}endDate')
            
            if start_node is not None and end_node is not None and start_node.text and end_node.text:
                start_txt = start_node.text.strip()
                end_txt = end_node.text.strip()
                
                # Verificamos si el fin del periodo termina en el año que estamos buscando
                if end_txt.startswith(año_str):
                    try:
                        # Calculamos la diferencia de días para asegurar que representa el año completo
                        fecha_inicio = datetime.strptime(start_txt, "%Y-%m-%d")
                        fecha_fin = datetime.strptime(end_txt, "%Y-%m-%d")
                        diferencia_dias = (fecha_fin - fecha_inicio).days
                        
                        # Un año fiscal regular tiene entre 350 y 375 días (considerando semanas variables de reporte)
                        if 350 <= diferencia_dias <= 375:
                            fecha_cierre_oficial = end_txt
                            break
                    except ValueError:
                        continue

    # Si el XML no reporta un año completo que termine en ese año, usamos un fallback basado en texto básico
    if not fecha_cierre_oficial:
        for context in root.findall('.//{*}context'):
            period = context.find('.//{*}period')
            if period is not None:
                instant_node = period.find('.//{*}instant')
                if instant_node is not None and instant_node.text:
                    inst_txt = instant_node.text.strip()
                    # Si el instante contiene exactamente el año buscado y es fin de mes común (ej. 06-30 o 12-31)
                    if inst_txt.startswith(año_str) and ("-06-" in inst_txt or "-12-" in inst_txt or "-09-" in inst_txt):
                        fecha_cierre_oficial = inst_txt
                        break

    if not fecha_cierre_oficial:
        return None

    # Segundo: Ahora que sabemos la fecha exacta de cierre (ej. '2017-06-30'), 
    # buscamos el contexto de tipo INSTANT que use exactamente esa fecha.
    for context in root.findall('.//{*}context'):
        context_id = context.get('id')
        period = context.find('.//{*}period')
        if period is not None:
            instant_node = period.find('.//{*}instant')
            if instant_node is not None and instant_node.text:
                if instant_node.text.strip() == fecha_cierre_oficial:
                    print(f"para el año {año_buscado} el contexto es {context_id} type: {type(context_id)}")
                    return context_id

    return None


def extraer_patrimonio_us_gaap(ruta_archivo, año_buscado):
    """
    PASO 4: Utiliza el ID de contexto del Balance General obtenido dinámicamente
    para extraer el valor correcto de la etiqueta de patrimonio.
    """
    if not os.path.exists(ruta_archivo):
        return "Archivo no existe"

    try:
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()
    except Exception as e:
        return f"Error leyendo XML: {e}"

    # Obtenemos la llave maestra del Balance General para este año específico
    contexto_valido = encontrar_id_balance_general(root, año_buscado)
    
    if not contexto_valido:
        return f"No se detectó el contexto de cierre para el año {año_buscado}"

    # Etiquetas oficiales admitidas por la taxonomía US-GAAP
    tags_patrimonio = {
        'StockholdersEquity',
        'StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest'
    }

    # Buscamos el valor emparejado únicamente a esa llave maestra
    for elemento in root.iter():
        tag_local = elemento.tag.split('}')[-1]

        if tag_local in tags_patrimonio:
            if elemento.get('contextRef') == contexto_valido:
                valor_texto = elemento.text
                if valor_texto:
                    try:
                        return int(float(valor_texto.strip()))
                    except ValueError:
                        continue

    return f"No encontrado para el contexto oficial asignado ('{contexto_valido}')"


# =====================================================================
# CONFIGURACIÓN DE TU BÚSQUEDA FILTRADA
# =====================================================================

# Lista de tus años a buscar
años_a_buscar = ["2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]

# DISCRIMINACIÓN: Define aquí la empresa que vas a procesar
empresa_a_buscar = "clorox"

# Ruta de tu carpeta con los archivos XML
directorio_base = "../data_xml"

print(f"--- EJECUTANDO EXTRACTOR ADAPTATIVO US-GAAP (FILTRO: {empresa_a_buscar.upper()}) ---")

for año in años_a_buscar:
    nombre_importacion = f"/{empresa_a_buscar}{año}.xml"
    ruta_completa = f"{directorio_base}{nombre_importacion}"
    
    resultado = extraer_patrimonio_us_gaap(ruta_completa, año)
    
    nombre_consola = f"{empresa_a_buscar}{año}.xml"
    print(f"{nombre_consola} : {resultado}")
