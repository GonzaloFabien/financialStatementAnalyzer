#Este script permite leer la taxonomía que usará la SMV para poder extraer tags.
import xml.etree.ElementTree as ET

#nos conectamos al archivo:
tree = ET.parse('casaGrande2024.xml')
root = tree.getroot()

#Al no encontrar ningún nameSpaces lo que haremos ahora será buscarlo mediante python:
namespaces = dict([nodo for evento, nodo in ET.iterparse('casaGrande2024.xml', events=['start-ns'])])

print("--Namespaces encontrados:--")
for prefijo, url in namespaces.items():
    print(f"Prefijo -> : {prefijo}---> url -->: {url}")