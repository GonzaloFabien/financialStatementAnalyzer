import json
import matplotlib.pyplot as plt

#Cargamos la base de datos:

ruta_json = "data_xml/reporte_analizado.json"
with open(ruta_json, "r", encoding="utf-8") as archivo:
    base_datos = json.load(archivo)
