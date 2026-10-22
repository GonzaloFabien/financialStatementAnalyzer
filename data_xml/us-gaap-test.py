import xml.etree.ElementTree as ET

# Definición de los Namespaces según el encabezado del archivo
namespaces = {
    'xbrli': 'http://xbrl.org',
    'us-gaap': 'http://fasb.org',  # Taxonomía identificada
    'clx': 'http://clorox.com'
}

def leer_xbrl_liabilities_equity(xml_content):
    # Cargar el contenido XML
    root = ET.fromstring(xml_content)
    
    # Lista de etiquetas us-gaap objetivo para liabilities y equity
    target_tags = [
        'Liabilities', 
        'LiabilitiesCurrent', 
        'StockholdersEquity', 
        'RetainedEarningsAccumulatedDeficit',
        'TreasuryStockValue'
    ]
    
    print(f"{'Concepto US-GAAP':<40} | {'Contexto':<12} | {'Valor':<15}")
    print("-" * 75)
    
    # Buscar cada elemento dentro del archivo usando el espacio de nombres de us-gaap
    for tag in target_tags:
        # Formato de búsqueda: {namespace}tag
        search_path = f".//us-gaap:{tag}"
        elements = root.findall(search_path, namespaces)
        
        for elem in elements:
            context = elem.get('contextRef')
            value = elem.text
            # Filtrar por los contextos principales de balance anual (2017 y 2016)
            if context in ['FI2017Q4', 'FI2016Q4']:
                try:
                    # Dar formato numérico legible
                    formatted_val = f"${int(value):,}"
                except ValueError:
                    formatted_val = value
                    
                print(f"us-gaap:{tag:<32} | {context:<12} | {formatted_val:>15}")

# Para ejecutarlo con tu archivo, puedes pasar el texto del documento como argumento:
# leer_xbrl_liabilities_equity(tu_texto_xml)
