#The proyect start:
#1- The first step is know the Scheme="URL" and also the code of the <XBRLI:identifier>B08361
#2- The second step is kwnow the taxonomy of the xml document by 'namespaces.py'
from funcion_buscar import buscar_elemento
import xml.etree.ElementTree as ET

#FUNCION 1: Esta función solo extrae datos a un diccionario anidado:
#MANTENIMIENTO:
def extraer_source_data_f1(root_empresa, año_a_analizar):
    #------Mantenimiento---- manejo de DUPLAS---DURATION---INSTANT---]
    ids_duration, ids_instant = año_a_analizar
    duration_id = ids_duration[0] if ids_duration else ""
    instant_id = ids_instant[0] if ids_instant else ""


    
    datos = {
        # --- Cuentas del Estado de Resultados (Usan año_a_analizar) ---
        'Revenue' : buscar_elemento('Revenue', duration_id, root_empresa) or buscar_elemento('RevenueFromContractWithCustomerExcludingAssessedTax', duration_id, root_empresa),        
        'CostOfSales' : buscar_elemento('CostOfSales', duration_id, root_empresa) or buscar_elemento('CostOfGoodsAndServicesSold', duration_id, root_empresa) or buscar_elemento('CostOfGoodsSold', duration_id, root_empresa),        
        'ProfitLoss': buscar_elemento('ProfitLoss', duration_id, root_empresa) or buscar_elemento('NetIncomeLoss', duration_id, root_empresa),
        # --- Cuentas del Balance General (Usan año_a_analizar) ---
        'CashAndCashEquivalents' : buscar_elemento('CashAndCashEquivalents', instant_id, root_empresa) or buscar_elemento('CashAndCashEquivalentsAtCarryingValue', instant_id, root_empresa),        
        'Equity': buscar_elemento('Equity', instant_id, root_empresa) or buscar_elemento('StockholdersEquity', instant_id, root_empresa) or buscar_elemento('StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest', instant_id, root_empresa) or buscar_elemento('LimitedLiabilityCompanyLlcMembersEquityIncludingPortionAttributableToNoncontrollingInterest', instant_id, root_empresa),
        'Assets': buscar_elemento('Assets', instant_id, root_empresa),
        'Liabilities': buscar_elemento('LiabilitiesAndStockholdersEquity', instant_id, root_empresa),        
        'CurrentAssets': buscar_elemento('CurrentAssets', instant_id, root_empresa) or buscar_elemento('AssetsCurrent', instant_id, root_empresa),        
        'Inventories': buscar_elemento('Inventories', instant_id, root_empresa) or buscar_elemento('InventoryNet', instant_id, root_empresa),        
        'CurrentLiabilities': buscar_elemento('CurrentLiabilities', instant_id, root_empresa)
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
    liabilities = diccionario_fuente_generado['Liabilities'] or 0
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
