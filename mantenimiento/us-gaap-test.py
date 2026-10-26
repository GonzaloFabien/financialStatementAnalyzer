import xml.etree.ElementTree as ET

def leer_xbrl_ajustado(xml_file_path):
    # Cargar el archivo directamente desde tu ruta local
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    # Lista de conceptos clave que queremos encontrar (Pasivo y Patrimonio)
    conceptos_objetivo = [
        'Liabilities', 
        'LiabilitiesCurrent', 
        'StockholdersEquity', 
        'RetainedEarningsAccumulatedDeficit',
        'TreasuryStockValue'
    ]
    
    # Filtro de contextos anuales principales del documento
    contextos_validos = ['FI2017Q4', 'FI2016Q4']
    
    print(f"{'Concepto Encontrado':<40} | {'Contexto':<12} | {'Valor original':<15} | {'Formateado':<15}")
    print("-" * 90)
    
    # Iteramos sobre absolutamente todos los elementos del XML para no perder ninguno por culpa del Namespace
    for elem in root.iter():
        # Extraemos solo el nombre de la etiqueta (eliminando lo que esté entre {})
        tag_name = elem.tag.split('}')[-1]
        
        if tag_name in conceptos_objetivo:
            contexto = elem.get('contextRef')
            
            # Si pertenece a los periodos clave de cierre de año, lo imprimimos
            if contexto in contextos_validos:
                val_text = elem.text if elem.text else "0"
                try:
                    formatted_val = f"${int(val_text):,}"
                except ValueError:
                    formatted_val = val_text
                
                print(f"{tag_name:<40} | {contexto:<12} | {val_text:<15} | {formatted_val:>15}")

# === CÓMO USARLO ===
# Guarda tu XML con el nombre 'reporte.xml' en la misma carpeta que este script y ejecuta:
# leer_xbrl_ajustado('reporte.xml')

leer_xbrl_ajustado("clorox2017.xml")
