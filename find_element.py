#This script is to find elements into a xml document:

import xml.etree.ElementTree as ET

tree = ET.parse("casaGrande2024.xml")
root = tree.getroot()

print("--- Rastreando cuentas con nombres similares de efectivo:")

for element in root.iter():
    if "cash" in element.tag.lower():
        nombre_minusculas = element.tag.split('}')[-1] if '}' in element.tag else element.tag
        print(f"Cuenta encontrada como: {nombre_minusculas} | valor: {element.text} | contexto: {element.get('contextRef')}")