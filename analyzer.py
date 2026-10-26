#The proyect start:
#1- The first step is know the Scheme="URL" and also the code of the <XBRLI:identifier>B08361
#2- The second step is kwnow the taxonomy of the xml document by 'namespaces.py'
from funcion_buscar import buscar_elemento
import xml.etree.ElementTree as ET

#FUNCION 1: Esta función solo extrae datos a un diccionario anidado:
#MANTENIMIENTO:
def extraer_source_data_f1(root_empresa, año_a_analizar):
    #------Mantenimiento----
    id_resultados = año_a_analizar["ER"]
    id_balance = año_a_analizar["BG"]
    
    datos = {
        # --- Cuentas del Estado de Resultados (Usan id_resultados) ---
        'Revenue' : buscar_elemento('Revenue', id_resultados, root_empresa) or buscar_elemento('RevenueFromContractWithCustomerExcludingAssessedTax', id_resultados, root_empresa),
        
        'CostOfSales' : buscar_elemento('CostOfSales', id_resultados, root_empresa) or buscar_elemento('CostOfGoodsAndServicesSold', id_resultados, root_empresa) or buscar_elemento('CostOfGoodsSold', id_resultados, root_empresa),
        
        'ProfitLoss': buscar_elemento('ProfitLoss', id_resultados, root_empresa) or buscar_elemento('NetIncomeLoss', id_resultados, root_empresa),

        # --- Cuentas del Balance General (Usan id_balance) ---
        'CashAndCashEquivalents' : buscar_elemento('CashAndCashEquivalents', id_balance, root_empresa) or buscar_elemento('CashAndCashEquivalentsAtCarryingValue', id_balance, root_empresa),
        
        'Equity': buscar_elemento('Equity', id_balance, root_empresa) or buscar_elemento('StockholdersEquity', id_balance, root_empresa) or buscar_elemento('PartnersCapital', id_balance, root_empresa) or buscar_elemento('LimitedLiabilityCompanyLlcMembersEquityIncludingPortionAttributableToNoncontrollingInterest', id_balance, root_empresa),
        
        'Assets': buscar_elemento('Assets', id_balance, root_empresa),
        
        'Liabilities': buscar_elemento('LiabilitiesAndStockholdersEquity', id_balance, root_empresa),
        
        'CurrentAssets': buscar_elemento('CurrentAssets', id_balance, root_empresa) or buscar_elemento('AssetsCurrent', id_balance, root_empresa),
        
        'Inventories': buscar_elemento('Inventories', id_balance, root_empresa) or buscar_elemento('InventoryNet', id_balance, root_empresa),
        
        'CurrentLiabilities': buscar_elemento('CurrentLiabilities', id_balance, root_empresa)
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
