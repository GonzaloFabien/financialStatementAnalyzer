import xml.etree.ElementTree as ET
from funcion_buscar import buscar_elemento
from funcion_periodo import encontrar_id_año
from analyzer import extraer_source_data_f1
from analyzer import calcular_ratios_de_extraer_source_data_f2
from data_xml.instant import encontrar_contextos_xbrl
import json
import os

#Aquí vamos a colocar los años de los documentos que vamos a descargar:
años_a_buscar = [ "2017","2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]

ruta_json_existente = "data_xml/reporte_analizado.json"

#Persistimos el Json anterior:
if os.path.exists(ruta_json_existente):
    with open(ruta_json_existente, "r", encoding="utf-8") as archivo:
        tabla_guardada = json.load(archivo)
else:
    #Si por alguna razón no existe tabla_historial la creamos desde cero:
    tabla_guardada = {}

"""
    Se crea la función para poder agregar empresas más rápidamente, solo coloca el nombre:
"""
def agregar_empresa_a_bd(nombre_base, nombre_file):
    #Si no existe nuestra actual empresa a importar, entonces la creamos:
    if nombre_base not in tabla_guardada:
        tabla_guardada[nombre_base] = {}


    #Se inicia el bucle:-----------------------------------------------------
    for año in años_a_buscar:
        nombre_importacion = f"data_xml/{nombre_file}{año}.xml" 

        #Test para verificar si el archivo existe:
        if not os.path.exists(nombre_importacion):
            print(f"El archivo {nombre_importacion} para el año {año} no existe")
            continue    

        #1- conexión al XML
        try:
            root_anual = ET.parse(nombre_importacion).getroot()
        except ET.ParseError as ex:
            print(f"\tAlereta, no se pudo leer el archivo del año {año}")
            continue

        #-----EN MANTENIMIENTO, siga adelante por favor-------
        #2- Buscamos y encontramos el ID de cada elemento por su año ------- EN MANTENIMIENTO-------:

        ids_del_año = encontrar_contextos_xbrl(root=root_anual, año_buscado=año)


        #----- FIN DEL MANTENIMIENTO


        #3- Datos encontrados en el diccionario:

        data_empresa_anual = extraer_source_data_f1(root_anual, ids_del_año)

        #4- Se calcula los datos de cada año:
        ratios_calculados_anual = calcular_ratios_de_extraer_source_data_f2(data_empresa_anual)

        #5- Añadimos la data y ratios analizados al nuevo diccionario:
        tabla_guardada[nombre_base][año] = ratios_calculados_anual

        #Comentario opcional de funcionalidad del código:
        print(f"\tFuncionó con Éxito la lectura del {nombre_file} xml, para el año: |{año}")

    #6- acabado el proceso de iteración guardamos en el Json:
    with open("data_xml/reporte_analizado.json", "w", encoding="utf-8") as archivo_json: 
        json.dump(tabla_guardada, archivo_json, indent=4, ensure_ascii=False)

    #Fin del bucle----



#Proceso para ejecutar correctamente todo el código:

if __name__ == "__main__":
    agregar_empresa_a_bd("Clorox","clorox")
