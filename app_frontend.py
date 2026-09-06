import json

#1- Apuntamos al archivo que guarda nuestra información"
ruta_json = "data_xml/reporte_analizado.json"

print("Inciio de interfaz financiera")

#2- Se cargan los datos históricos 
with open(ruta_json, "r", encoding="utf-8") as archivo:
    base_datos = json.load(archivo)

print("Se cargó correctamente la base de datos")

#3- Accedemos a los datos de la empresa
datos_empresa = base_datos['Casa Grande']

"""
#Esto es para saber los tags disponibles a utilizar del diccionario:
ratos_test = datos_empresa['2016'].keys()
print(list(ratos_test))
"""
#4- Los mostramos en una lista ordenada
años_disponibles = sorted(list(datos_empresa.keys()))
print(f"\nAños historicos detectados :  {años_disponibles}")
