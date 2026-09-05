import json

#1- Apuntamos al archivo que guarda nuestra información"
ruta_json = "data_xml/reporte_analizado.json"

print("Inciio de interfaz financiera")

#2- Se cargan los datos históricos 
with open(ruta_json, "r", encoding="utf-8") as archivo:
    base_datos = json.load(archivo)

print("Se cargó correctamente la base de datos")


