#We Create the analyzer of periods:

import xml.etree.ElementTree as ET

empresa_a_analizar = "casaGrande2024.xml"
tree = ET.parse(empresa_a_analizar)
root = tree.getroot()

def encontrar_id_año(año_buscado):
    for elemento in root.iter():
        nombre_original = elemento.tag
        nombre_limpio = nombre_original.split('}')[-1] if '}' in nombre_original else nombre_original
        
        if nombre_limpio == "context":

            id_contexto = elemento.get('id')
            print(f"Fecha del ID es = {id_contexto}")
        



if __name__ == "__main__":
    encontrar_id_año("2024")