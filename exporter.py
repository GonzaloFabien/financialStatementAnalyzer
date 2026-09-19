import json 
import os
import pandas as pd

#Apuntamos a la ubicación del json y del excel a exportar:
ruta_json = "data_xml/reporte_analizado.json"
ruta_excel = "data_xml/reporte_excel.xlsx"

with open(ruta_json, "r", encoding="utf-8") as archivo:
    base_datos = json.load(archivo)

ratios_a_exportar = ['Net Income', 'Margen Neto', 'ROE', 'ROA']

#1- iniciamos pandas:
with pd.ExcelWriter(ruta_excel, engine='openpyxl') as writer:
    for empresa, datos_historicos in base_datos.items():
        años_ordenados = sorted(list(datos_historicos.keys()))

        #Escruturamos los datos en un nuevo diccionario intermedio 
        matriz_excel = {}
        for ratio in ratios_a_exportar:
            #Extraemos los valores del diccionario de manera segura:
            matriz_excel[ratio] = [datos_historicos[año].get(ratio, 0) for año in años_ordenados]
        #Extructuramos los datos en un dataFrame de pandas
        df = pd.DataFrame(matriz_excel, index=años_ordenados).T

        #Convertimos  Excel
        df.to_excel(writer, sheet_name= empresa, index_label = "Ratio / Métrica " )

print(f"Se generó el archivo excel en {ruta_excel}")