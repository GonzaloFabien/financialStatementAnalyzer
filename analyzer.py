#The proyect start:
#1- The first step is know the Scheme="URL" and also the code of the <XBRLI:identifier>B08361
#2- The second step is kwnow the taxonomy of the xml document by 'namespaces.py'
from funcion_buscar import buscar_elemento
import xml.etree.ElementTree as ET

#FUNCION 1: Esta función solo extrae datos a un diccionario anidado:
#MANTENIMIENTO:
def extraer_source_data_f1(root_empresa, año_a_analizar):
    datos = {
        'Revenue' : buscar_elemento('Revenue',año_a_analizar, root_empresa) or  buscar_elemento('RevenueFromContractWithCustomerExcludingAssessedTax',año_a_analizar, root_empresa),
        'CostOfSales' : buscar_elemento('CostOfSales', año_a_analizar, root_empresa),
        'CashAndCashEquivalents' : buscar_elemento('CashAndCashEquivalents', año_a_analizar, root_empresa),
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
    revenue = diccionario_fuente_generado['Revenue'] or 0
    cost_of_sales = diccionario_fuente_generado['CostOfSales']
    net_income = diccionario_fuente_generado['ProfitLoss'] or 0
    equity = diccionario_fuente_generado['Equity'] or 0
    assets = diccionario_fuente_generado['Assets'] or 0
    liabilities = diccionario_fuente_generado['Liabilities']
    current_assets = diccionario_fuente_generado['CurrentAssets'] or 0
    inventories = diccionario_fuente_generado['Inventories'] or 0 
    current_liabilities = diccionario_fuente_generado['CurrentLiabilities'] or 0
    cashAndCashEquivalents = diccionario_fuente_generado['CashAndCashEquivalents']or 0 
    
    #Estos son los tag del diccionario a buscar:
    ratios_calculados = {
        'Revenue' : revenue,
        'CostOfSales' : cost_of_sales,
        'Equity': equity,
        'CashAndCashEquivalents': cashAndCashEquivalents,
        'Net Income': net_income,
        'Net Margin': (net_income / revenue * 100) if revenue > 0 else 0,
        'ROE': (net_income / equity * 100) if equity > 0 else 0,
        'ROA': (net_income / assets * 100) if assets > 0 else 0,
        'Cash Ratio': (cashAndCashEquivalents/current_assets) if current_assets > 0 else 0,
        'Current Ratio': (liabilities / equity * 100) if equity > 0 else 0,
        'Debt Asset Ratio': (liabilities / assets * 100) if assets > 0 else 0,
        'Quick Ratio': (current_assets - inventories) / current_liabilities if current_liabilities > 0 else 0
    }

    return ratios_calculados



#Demostramos que es un package:
if __name__ == "__main__":
    print("hola")
