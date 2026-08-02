from funcion_buscar import buscar_elemento
from funcion_buscar import nombre_empresa


#The id1 ranges from the start of 2024 to the end of 2024
#The id3 starts at the 2024-12-31 instant, thats mean the end of 2024
empresa_buscada = "casaGrande2024.xml"
efectivo_2024 = buscar_elemento('CashAndCashEquivalents', 'id3')
ventas_2024 = buscar_elemento('Revenue', 'id1')
Beneficio_bruto_2024 = buscar_elemento('GrossProfit', 'id1')
Utilidad_neta_2024 = buscar_elemento('ProfitLoss', 'id1')


margen_neto_2024 = Utilidad_neta_2024/ventas_2024 *100

print(f"Margen {nombre_empresa} 2024: {margen_neto_2024:.2f} % ")