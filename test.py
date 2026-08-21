import xml.etree.ElementTree as ET
from funcion_buscar import buscar_elemento
from funcion_periodo import encontrar_id_año

año_2024 = encontrar_id_año("2024")
año_2023 = encontrar_id_año("2023")

#Aquí el archivo de la empresa a Analizar 
nombre_empresa = (ET.parse('casaGrande2024.xml')).getroot()
#The id1 ranges from the start of 2024 to the end of 2024
#The id3 starts at the 2024-12-31 instant, thats mean the end of 2024

#Agregamos otra empresa para analizar y comparar ratios financieros: 

empresa_2 = (ET.parse('cartavio2024.xml')).getroot()

Utilidad_neta_2024_cartavio = buscar_elemento('ProfitLoss',año_2024,empresa_2)
print(f"\nPrimeramente, la utilidad del 2024 de Cartavio fue: {Utilidad_neta_2024_cartavio} en soles\n\n")

#Test para los id
efectivo_2024 = buscar_elemento('CashAndCashEquivalents', año_2024, nombre_empresa)

#test para la consola:
print(f"\n\n\tTest para el efectivo: {efectivo_2024}\n\n")

ventas_2024 = buscar_elemento('Revenue',   año_2024,nombre_empresa)
Beneficio_bruto_2024 = buscar_elemento('GrossProfit', año_2024,nombre_empresa)
Utilidad_neta_2024 = buscar_elemento('ProfitLoss', año_2024,nombre_empresa)
capital_2024 = buscar_elemento('Equity', año_2024,nombre_empresa)
pasivos_2024 =  buscar_elemento('Liabilities', año_2024,nombre_empresa)
activos_2024 = buscar_elemento('Assets', año_2024,nombre_empresa)
activos_corrientes_2024 = buscar_elemento('CurrentAssets', año_2024,nombre_empresa)
inventarios_2024 = buscar_elemento('Inventories', año_2024,nombre_empresa)
pasivos_corrientes = buscar_elemento('CurrentLiabilities', año_2024,nombre_empresa)

print(f"\n\t\n El capital para el 2024 es: {capital_2024}\n")
print(f"\n\t\n Valor de la utilidad Neta del 2024: {Utilidad_neta_2024}\n")
margen_neto_2024 = Utilidad_neta_2024/ventas_2024 *100

#Mostamos ratios financieros:
print(f"Margen 2024: {margen_neto_2024:.2f} % ")

print(f"ROE: {((Utilidad_neta_2024/capital_2024 )*100):.2f} %")

print(f"ROA: {Utilidad_neta_2024/activos_2024*100:.2f} %")

print(f"Ratio Solvencia: {pasivos_2024/capital_2024*100:.2f} %")

print(f"Ratio Deuda/Activo : {pasivos_2024/activos_2024*100:.2f} %")

print(f"Prueba Acida : {(activos_corrientes_2024-inventarios_2024)/pasivos_corrientes   } ")

