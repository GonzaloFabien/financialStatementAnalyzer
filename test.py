from funcion_buscar import buscar_elemento
from funcion_buscar import nombre_empresa
from funcion_periodo import encontrar_id_año

año_2024 = encontrar_id_año("2024")
año_2023 = encontrar_id_año("2023")
#The id1 ranges from the start of 2024 to the end of 2024
#The id3 starts at the 2024-12-31 instant, thats mean the end of 2024

#Test para los id
efectivo_2024 = buscar_elemento('CashAndCashEquivalents', año_2024)

#test para la consola:
print(f"\n\n\tTest para el efectivo: {efectivo_2024}\n\n")

ventas_2024 = buscar_elemento('Revenue',   año_2024 )
Beneficio_bruto_2024 = buscar_elemento('GrossProfit', año_2024)
Utilidad_neta_2024 = buscar_elemento('ProfitLoss', año_2024)
capital_2024 = buscar_elemento('Equity', año_2024)
pasivos_2024 =  buscar_elemento('Liabilities', año_2024)
activos_2024 = buscar_elemento('Assets', año_2024)
activos_corrientes_2024 = buscar_elemento('CurrentAssets', año_2024)
inventarios_2024 = buscar_elemento('Inventories', año_2024)
pasivos_corrientes = buscar_elemento('CurrentLiabilities', año_2024)

print(f"\n\t\n El capital para el 2024 es: {capital_2024}\n")
print(f"\n\t\n Valor de la utilidad Neta del 2024: {Utilidad_neta_2024}\n")
margen_neto_2024 = Utilidad_neta_2024/ventas_2024 *100

#Mostamos ratios financieros:
print(f"Margen 2024: {margen_neto_2024:.2f} % ")

print(f"ROE: {((Utilidad_neta_2024/capital_2024 )*100):.2f} %")

print(f"ROA: {Utilidad_neta_2024/activos_2024:.2f} %")

print(f"Ratio Solvencia: {pasivos_2024/capital_2024:.2f} %")

print(f"Ratio Deuda/Activo : {pasivos_2024/activos_2024:.2f} %")

print(f"Prueba Acida : {(activos_corrientes_2024-inventarios_2024)/pasivos_corrientes}")

