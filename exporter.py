import json 
import os
import pandas as pd

#Apuntamos a la ubicación del json y del excel a exportar:
ruta_json = "data_xml/reporte_analizado.json"
ruta_excel = "data_xml/reporte_excel.xlsx"

with open(ruta_json, "r", encoding="utf-8") as archivo:
    base_datos = json.load(archivo)

ratios_a_exportar = ['Net Income', 'Margen Neto', 'ROE', 'ROA']

