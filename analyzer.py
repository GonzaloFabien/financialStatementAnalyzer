#The proyect start:
#1- The first step is know the Scheme="URL" and also the code of the <XBRLI:identifier>B08361
#2- The second step is kwnow the taxonomy of the xml document by 'namespaces.py'
from funcion_buscar import buscar_elemento
import xml.etree.ElementTree as ET

#FUNCION 0: Auxiliar para limpiar valor de los números:
def limpiar_valor(valor):
    if valor is None:
        return 0
    if isinstance(valor, (int, float)):
        return valor
    try:
        #Elimina impuresas:
        return int(float(str(valor).strip()))
    except ValueError:
        return 0


#FUNCION 1: Esta función solo extrae datos a un diccionario anidado:
#MANTENIMIENTO:
def extraer_source_data_f1(root_empresa, año_a_analizar):
    #------Mantenimiento---- manejo de DUPLAS---DURATION---INSTANT---]
    ids_duration, ids_instant = año_a_analizar
    duration_id = ids_duration[0] if ids_duration else ""
    instant_id = ids_instant[1] if ids_instant else ""


    
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
    revenue = limpiar_valor(diccionario_fuente_generado['Revenue'])
    cost_of_sales = limpiar_valor(diccionario_fuente_generado['CostOfSales'])
    net_income = limpiar_valor(diccionario_fuente_generado['ProfitLoss'])
    equity = limpiar_valor(diccionario_fuente_generado['Equity'])
    assets = limpiar_valor(diccionario_fuente_generado['Assets'])
    liabilities = limpiar_valor(diccionario_fuente_generado['Liabilities'])
    current_assets = limpiar_valor(diccionario_fuente_generado['CurrentAssets'])
    inventories = limpiar_valor(diccionario_fuente_generado['Inventories']) 
    current_liabilities = limpiar_valor(diccionario_fuente_generado['CurrentLiabilities'])
    cashAndCashEquivalents = limpiar_valor(diccionario_fuente_generado['CashAndCashEquivalents']) 
    
    #Estos son los tag del diccionario a buscar:
    ratios_calculados = {
        'Revenue' : revenue,
        'CostOfSales' : cost_of_sales,
        'Equity': equity,
        'CashAndCashEquivalents': cashAndCashEquivalents,
        'Net Income': net_income,
        'Net Margin': (net_income / revenue * 100) if revenue > 0 else 0,
        'ROE': (net_income / equity * 100),
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
