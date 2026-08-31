#The proyect start:
#1- The first step is know the Scheme="URL" and also the code of the <XBRLI:identifier>B08361
#2- The second step is kwnow the taxonomy of the xml document by 'namespaces.py'
from funcion_buscar import buscar_elemento
import xml.etree.ElementTree as ET


#Considera que año a analizar es un ID
def analizar_empresa(root_empresa, año_a_analizar ,nombre_imprimir):
    print(f"\n--- ANÁLISIS DE RATIOS PARA: {nombre_imprimir} ---")

    #Aquí se tendrá todos los tags de las variables: 
    efectivo_2024 = buscar_elemento('CashAndCashEquivalents', año_a_analizar, root_empresa)
    ventas_2024 = buscar_elemento('Revenue', año_a_analizar, root_empresa)
    Beneficio_bruto_2024 = buscar_elemento('GrossProfit', año_a_analizar, root_empresa)
    Utilidad_neta_2024 = buscar_elemento('ProfitLoss', año_a_analizar, root_empresa)
    capital_2024 = buscar_elemento('Equity', año_a_analizar, root_empresa)
    pasivos_2024 =  buscar_elemento('Liabilities', año_a_analizar, root_empresa)
    activos_2024 = buscar_elemento('Assets', año_a_analizar, root_empresa)
    activos_corrientes_2024 = buscar_elemento('CurrentAssets', año_a_analizar, root_empresa)
    inventarios_2024 = buscar_elemento('Inventories', año_a_analizar, root_empresa)
    pasivos_corrientes = buscar_elemento('CurrentLiabilities', año_a_analizar, root_empresa)
    
    margen_neto_2024 = Utilidad_neta_2024 / ventas_2024 * 100 if ventas_2024 > 0 else 0

    #Diccionario anidado:
    ratios_calculados = {
        'Capital' : capital_2024,
        'Utilidad Neta' : Utilidad_neta_2024,
        'Margen Neto' : margen_neto_2024,
        'ROE' : Utilidad_neta_2024 / capital_2024 * 100 if capital_2024 > 0 else 0,
        'ROA' : Utilidad_neta_2024 / activos_2024 * 100 if activos_2024 > 0 else 0,
        'Ratio Solvencia' : pasivos_2024 / capital_2024 * 100 if capital_2024 > 0 else 0,
        'Ratio Deuda/Activo' : pasivos_2024 / activos_2024 * 100 if activos_2024 > 0 else 0,
        'Prueba Acida' : (activos_corrientes_2024 - inventarios_2024) / pasivos_corrientes if pasivos_corrientes > 0 else 0
    }
    print("-" * 40)
    return ratios_calculados




#Ratios de solvencia
def analizar_solvencia(root_empresa, año_a_analizar, nombre_imprimir):
    print(f"\n--- ANÁLISIS DE RATIOS DE SOLVENCIA PARA: {nombre_imprimir} ---")
    
    # Aquí se tendrán todos los tags de las variables para solvencia:
    capital_2024 = buscar_elemento('Equity', año_a_analizar, root_empresa)
    pasivos_2024 = buscar_elemento('Liabilities', año_a_analizar, root_empresa)
    activos_2024 = buscar_elemento('Assets', año_a_analizar, root_empresa)
    pasivos_no_corrientes = buscar_elemento('NonCurrentLiabilities', año_a_analizar, root_empresa)
    
    # Cálculo de los ratios de solvencia más importantes:
    ratio_solvencia = pasivos_2024 / capital_2024 * 100 if capital_2024 > 0 else 0
    ratio_deuda_activo = pasivos_2024 / activos_2024 * 100 if activos_2024 > 0 else 0
    multiplicador_capital = activos_2024 / capital_2024 if capital_2024 > 0 else 0
    
    print(f"El capital para el 2024 es: {capital_2024}")
    print(f"Valor de los pasivos totales del 2024: {pasivos_2024}")
    print(f"Ratio Solvencia (Deuda/Patrimonio): {ratio_solvencia:.2f} %")
    print(f"Ratio Deuda/Activo : {ratio_deuda_activo:.2f} %")
    print(f"Multiplicador del Capital: {multiplicador_capital:.2f}")
    print("-" * 40)

#FUNCION 1: Esta función solo extrae datos a un diccionario anidado:
def extraer_source_data_f1(root_empresa, año_a_analizar):
    datos = {
        'Revenue' : buscar_elemento('Revenue',año_a_analizar, root_empresa),
        'ProfitLoss': buscar_elemento('ProfitLoss', año_a_analizar, root_empresa),
        'Equity': buscar_elemento('Equity', año_a_analizar, root_empresa),
        'Assets': buscar_elemento('Assets', año_a_analizar, root_empresa),
        'Liabilities': buscar_elemento('Liabilities', año_a_analizar, root_empresa),
        'CurrentAssets': buscar_elemento('CurrentAssets', año_a_analizar, root_empresa),
        'Inventories': buscar_elemento('Inventories', año_a_analizar, root_empresa),
        'CurrentLiabilities': buscar_elemento('CurrentLiabilities', año_a_analizar, root_empresa)
    }
    return datos

#FUNCION 2: Esta función solo hará matemática y generará los ratios:
def calcular_ratios_de_extraer_source_data_f2(diccionario_fuente_generado):
    #Se generan varias variables para poder trabajarlas
    revenue = diccionario_fuente_generado['Revenue']
    net_income = diccionario_fuente_generado['ProfitLoss']
    equity = diccionario_fuente_generado['Equity']
    assets = diccionario_fuente_generado['Assets']
    liabilities = diccionario_fuente_generado['Liabilities']
    current_assets = diccionario_fuente_generado['CurrentAssets']
    inventories = diccionario_fuente_generado['Inventories']
    current_liabilities = diccionario_fuente_generado['CurrentLiabilities']

    ratios_calculados = {
        'Equity': equity,
        'Net Income': net_income,
        'Net Margin': (net_income / revenue * 100) if revenue > 0 else 0,
        'ROE': (net_income / equity * 100) if equity > 0 else 0,
        'ROA': (net_income / assets * 100) if assets > 0 else 0,
        'Current Ratio': (liabilities / equity * 100) if equity > 0 else 0,
        'Debt Asset Ratio': (liabilities / assets * 100) if assets > 0 else 0,
        'Quick Ratio': (current_assets - inventories) / current_liabilities if current_liabilities > 0 else 0
    }

    return ratios_calculados



#Demostramos que es un package:
if __name__ == "__main__":
    print("hola")
