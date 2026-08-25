import xml.etree.ElementTree as ET
from funcion_buscar import buscar_elemento
from funcion_periodo import encontrar_id_año
from analyzer import analizar_empresa
from analyzer import analizar_solvencia

#Los años se expresan en ids contextRef:
año_2024 = encontrar_id_año("2024")
año_2023 = encontrar_id_año("2023")

# Aquí el archivo de la empresa a Analizar 
casa_grande_root = (ET.parse('casaGrande2024.xml')).getroot()
cartavio_root = (ET.parse('cartavio2024.xml')).getroot()

tabla_horizontal = {}

# ejecucion, pero ahora las empresas están encapsuladas para atrapar el diccionario anidado de cada empresa
ratios_casa_grande = analizar_empresa(casa_grande_root, año_2024,"Casa Grande")
ratios_cartavio = analizar_empresa(cartavio_root,año_2024 ,"Cartavio")

tabla_horizontal["Casa Grande"] = ratios_casa_grande
tabla_horizontal["Cartavio"] = ratios_cartavio

print(f"\n[Test]: El ROE guardado de cartavio debería ser :7%| y es | {tabla_horizontal['Casa Grande']['ROE']:.2f}%")



