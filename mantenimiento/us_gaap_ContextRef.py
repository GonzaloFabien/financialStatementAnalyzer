import xml.etree.ElementTree as ET

def extraer_id_contextos_puros(xml_file_path):
    """
    Escanea el XBRL US-GAAP y extrae UNICAMENTE los IDs de contexto de forma limpia.
    Devuelve las estructuras crudas para que puedas iterar sobre ellas libremente en el futuro.
    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error al abrir el XML: {e}")
        return None

    # Estructuras nativas para almacenar los IDs recolectados
    todos_los_ids = set()
    contextos_instantaneos = []  # Candidatos para Balance General (Liabilities/Equity)
    contextos_duracion = []      # Candidatos para Estado de Resultados / Flujos

    print(f"Analizando estructura de contextos en: {xml_file_path}\n")

    # Iteramos sobre todo el XML de forma plana para no fallar por culpa de los Namespaces cambiantes
    for elem in root.iter():
        tag_limpio = elem.tag.split('}')[-1]
        
        # 1. Capturar los IDs directamente desde las definiciones de <context>
        if tag_limpio == 'context':
            id_contexto = elem.get('id')
            if id_contexto:
                todos_los_ids.add(id_contexto)
                
                # Identificar su estructura interna cruda sin parsear fechas
                es_instant = False
                es_duration = False
                
                for sub_elem in elem.iter():
                    sub_tag = sub_elem.tag.split('}')[-1]
                    if sub_tag == 'instant':
                        es_instant = True
                    if sub_tag == 'startDate' or sub_tag == 'endDate':
                        es_duration = True
                
                if es_instant:
                    contextos_instantaneos.append(id_contexto)
                elif es_duration:
                    contextos_duracion.append(id_contexto)

    # Convertimos a listas ordenadas para facilitar tus futuros bucles
    lista_total_ids = sorted(list(todos_los_ids))
    
    # --- SALIDA EN PANTALLA EXCLUSIVA DE DE IDs ---
    print("=" * 80)
    print(f" TOTAL DE IDs DE CONTEXTO ENCONTRADOS: {len(lista_total_ids)}")
    print("=" * 80)
    
    print("\n--- Muestra de los primeros 15 IDs de cualquier tipo (para inspección visual) ---")
    for _id in lista_total_ids[:15]:
        print(f'"{_id}"')
    if len(lista_total_ids) > 15:
        print(f"... y otros {len(lista_total_ids) - 15} IDs más.")

    print("\n" + "-"*80)
    print(f" CATEGORIZACIÓN CRUDA PARA ITERACIONES FUTURAS")
    print("-" * 80)
    print(f"IDs tipo 'instant' detectados (Balance): {len(contextos_instantaneos)}")
    print(f"IDs tipo 'duration' detectados (Resultados): {len(contextos_duracion)}")
    print("-" * 80)

    # Te devolvemos un diccionario nativo con las listas de IDs puros
    # Esto te permitirá hacer cosas como: for id_ctx in resultado['instant']:
    return {
        'todos': lista_total_ids,
        'instant': sorted(contextos_instantaneos),
        'duration': sorted(contextos_duracion)
    }

# === CÓMO OBTENER TUS LISTAS DE IDS PARA ITERAR ===
# datos_contextos = extraer_id_contextos_puros("clorox2017.xml")

# Ahora tienes las variables limpias en memoria para tus futuros scripts, por ejemplo:
# lista_para_tus_bucles = datos_contextos['instant']

extraer_id_contextos_puros("clorox2017.xml")