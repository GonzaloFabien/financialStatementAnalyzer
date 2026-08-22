import xml.etree.ElementTree as ET
from funcion_buscar import buscar_elemento
from funcion_periodo import encontrar_id_año

año_2024 = encontrar_id_año("2024")
año_2023 = encontrar_id_año("2023")

# Aquí encapsulamos tu bloque exacto de extracción y cálculo:
def analizar_empresa(root_empresa, nombre_imprimir):
    print(f"\n--- ANÁLISIS DE RATIOS PARA: {nombre_imprimir} ---")
    
    efectivo_2024 = buscar_elemento('CashAndCashEquivalents', año_2024, root_empresa)
    ventas_2024 = buscar_elemento('Revenue', año_2024, root_empresa)
    Beneficio_bruto_2024 = buscar_elemento('GrossProfit', año_2024, root_empresa)
    Utilidad_neta_2024 = buscar_elemento('ProfitLoss', año_2024, root_empresa)
    capital_2024 = buscar_elemento('Equity', año_2024, root_empresa)
    pasivos_2024 =  buscar_elemento('Liabilities', año_2024, root_empresa)
    activos_2024 = buscar_elemento('Assets', año_2024, root_empresa)
    activos_corrientes_2024 = buscar_elemento('CurrentAssets', año_2024, root_empresa)
    inventarios_2024 = buscar_elemento('Inventories', año_2024, root_empresa)
    pasivos_corrientes = buscar_elemento('CurrentLiabilities', año_2024, root_empresa)
    
    margen_neto_2024 = Utilidad_neta_2024 / ventas_2024 * 100 if ventas_2024 > 0 else 0

    print(f"El capital para el 2024 es: {capital_2024}")
    print(f"Valor de la utilidad Neta del 2024: {Utilidad_neta_2024}")
    print(f"Margen 2024: {margen_neto_2024:.2f} % ")
    print(f"ROE: {((Utilidad_neta_2024 / capital_2024) * 100 if capital_2024 > 0 else 0):.2f} %")
    print(f"ROA: {Utilidad_neta_2024 / activos_2024 * 100 if activos_2024 > 0 else 0:.2f} %")
    print(f"Ratio Solvencia: {pasivos_2024 / capital_2024 * 100 if capital_2024 > 0 else 0:.2f} %")
    print(f"Ratio Deuda/Activo : {pasivos_2024 / activos_2024 * 100 if activos_2024 > 0 else 0:.2f} %")
    print(f"Prueba Acida : {(activos_corrientes_2024 - inventarios_2024) / pasivos_corrientes if pasivos_corrientes > 0 else 0} ")
    print("-" * 40)


# Aquí el archivo de la empresa a Analizar 
nombre_empresa = (ET.parse('casaGrande2024.xml')).getroot()
empresa_2 = (ET.parse('cartavio2024.xml')).getroot()

# Primeramente, tu print manual para Cartavio se mantiene idéntico
Utilidad_neta_2024_cartavio = buscar_elemento('ProfitLoss', año_2024, empresa_2)
print(f"\nPrimeramente, la utilidad del 2024 de Cartavio fue: {Utilidad_neta_2024_cartavio} en soles\n\n")

# EJECUCIÓN: Llamamos a tu función para las dos empresas de forma directa
analizar_empresa(nombre_empresa, "Casa Grande")
analizar_empresa(empresa_2, "Cartavio")
