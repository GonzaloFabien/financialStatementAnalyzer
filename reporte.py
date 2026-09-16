import json
import os
import matplotlib.pyplot as plt

#1- Conectamos a la BD Json:
ruta_json = "data_xml/reporte_analizado.json"

with open(ruta_json, "r", encoding="utf-8") as archivo:
    datos_personalizdos  = json.load(archivo)

#2- Extraemos los diccionarios de ambas emrpesas:
diccionario_casa_grande = datos_personalizdos.get('Casa Grande', {})
diccionario_cartavio =  datos_personalizdos.get('Cartavio', {})

#3- Detectamos los años que comparten ambas empresas:
años_casa_grande = set(diccionario_casa_grande.keys())
años_cartavio = set(diccionario_casa_grande.keys())
años_comunes = sorted(list(años_casa_grande.intersection(años_cartavio)))

#-----IMPORTANTE, aquí el ratio que queremos comprar/MOSTRAR:
ratio_a_graficar = 'Net Income'

#4- Aramamos la lista de valores extraidos del JSON NoSQL:
valores_casa_grande = [diccionario_casa_grande[año].get(ratio_a_graficar, 0) for año in años_comunes]
valores_car = [diccionario_cartavio[año].get(ratio_a_graficar, 0) for año in años_comunes]
