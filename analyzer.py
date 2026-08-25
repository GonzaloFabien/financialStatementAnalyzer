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

    ratios_calculados = {
        'Capital' : (f"El capital para el 2024 es: {capital_2024}"),
        'Utilidad_NETA' : (f"Valor de la utilidad Neta del 2024: {Utilidad_neta_2024}"),
        'Margen_neto' : (f"Margen 2024: {margen_neto_2024:.2f} % "),
        'ROE' :(f"ROE: {((Utilidad_neta_2024 / capital_2024) * 100 if capital_2024 > 0 else 0):.2f} %")
        (f"ROA: {Utilidad_neta_2024 / activos_2024 * 100 if activos_2024 > 0 else 0:.2f} %")
        (f"Ratio Solvencia: {pasivos_2024 / capital_2024 * 100 if capital_2024 > 0 else 0:.2f} %")
        (f"Ratio Deuda/Activo : {pasivos_2024 / activos_2024 * 100 if activos_2024 > 0 else 0:.2f} %")
        (f"Prueba Acida : {(activos_corrientes_2024 - inventarios_2024) / pasivos_corrientes if pasivos_corrientes > 0 else 0} ")
    }
    print("-" * 40)

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


#Demostramos que es un package:
if __name__ == "__main__":
    print("hola")