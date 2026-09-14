import json
import matplotlib.pyplot as plt

#Cargamos la base de datos:

ruta_json = "data_xml/reporte_analizado.json"
with open(ruta_json, "r", encoding="utf-8") as archivo:
    base_datos = json.load(archivo)

#En adelante vamos a cargar los datos del del NoSQL Json: Casa Grande Cartavio (puede ser cualquier otro)

data_casa_grande = base_datos.get('Casa Grande',{})
data_cartavio = base_datos.get('Cartavio',{})

print("Se cargaron los datos")