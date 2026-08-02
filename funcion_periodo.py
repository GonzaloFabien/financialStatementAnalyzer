#We Create the analyzer of periods:

import xml.etree.ElementTree as ET

empresa_a_analizar = "casaGrande2024.xml"
tree = ET.parse(empresa_a_analizar)
root = tree.getroot()

def encontrar_id_año(año_buscado):
    print(f"Buscando el ID de {año_buscado}")



if __name__ == "__main__":
    encontrar_id_año("2024")