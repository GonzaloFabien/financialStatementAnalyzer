import xml.etree.ElementTree as ET
from funcion_buscar import buscar_elemento
from funcion_periodo import encontrar_id_año
from analyzer import analizar_empresa
from analyzer import analizar_solvencia
from analyzer import extraer_source_data_f1
from analyzer import calcular_ratios_de_extraer_source_data_f2
import json

# Aquí el archivo de la empresa a Analizar 
casa_grande_root = (ET.parse('data_xml/casaGrande2024.xml')).getroot()
cartavio_root = (ET.parse('data_xml/cartavio2024.xml')).getroot()

#Los años se expresan en ids contextRef:
id_casa_grande_2024 = encontrar_id_año("2024", casa_grande_root)
id_cartavio_2024 = encontrar_id_año("2024", cartavio_root)

tabla_horizontal = {}

# ejecucion, pero ahora las empresas están encapsuladas para atrapar el diccionario anidado de cada empresa

#------- Sección en mantenimiento, alejarse porfavor: ----------
print("a")
data_casa_grande = extraer_source_data_f1(casa_grande_root,id_casa_grande_2024)
ratios_casa_grande = calcular_ratios_de_extraer_source_data_f2(data_casa_grande)

data_cartavio = extraer_source_data_f1(cartavio_root, id_cartavio_2024)
ratios_cartavio = calcular_ratios_de_extraer_source_data_f2(data_cartavio)

#----------

tabla_horizontal["Casa Grande"] = ratios_casa_grande
tabla_horizontal["Cartavio"] = ratios_cartavio


#Aquí haremos una vizualización horizontal de el diccionario anidado:
print("\n"+"="*40)
print(f"{'Métrica financiera':<25} | {'Casa Grande':<15} | {'Cartavio':<15}") 
print("\n"+"="*40)

#Datos del diccionario que se van a mostrar:
ratios_a_mostrar = ['Net Income', 'Net Margin','ROE','ROA', 'Quick Ratio', 'Current Ratio', 'Debt Asset Ratio']

#Bucle para mostrarlo todo: 
for ratio in ratios_a_mostrar:
    valor_casaGrande = tabla_horizontal['Casa Grande'][ratio]
    valor_Cartavio = tabla_horizontal['Cartavio'][ratio]
    print(f"{ratio:<25} | {valor_casaGrande:<13.2f} | {valor_Cartavio:<13.2f}")
print("-"*40)

#Creación de una base de datos noSQL para manejar los datos en Json:



with open("data_xml/reporte_analizado.json", "w", encoding="utf-8") as archivo_json:
    json.dump(tabla_horizontal,archivo_json, indent=4, ensure_ascii=False)