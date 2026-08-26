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


#Aquí haremos una vizualización horizontal de el diccionario anidado:
print("\n"+"="*40)
print(f"{'Métrica financiera':<25} | {'Casa Grande':<15} | {'Cartavio':<15}") 
print("\n"+"="*40)

#Datos del diccionario que se van a mostrar:
ratios_a_mostrar = ['Utilidad Neta', 'Margen Neto','ROE','ROA', 'Prueba Acida']

#Bucle para mostrarlo todo: 
for ratio in ratios_a_mostrar:
    valor_casaGrande = tabla_horizontal['Casa Grande'][ratio]
    valor_Cartavio = tabla_horizontal['Cartavio'][ratio]
    print(f"{ratio:<25} | {valor_casaGrande:<13.2f} | {valor_Cartavio:<13.2f}")
print("-"*40)