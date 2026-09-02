import xml.etree.ElementTree as ET
from funcion_buscar import buscar_elemento
from funcion_periodo import encontrar_id_año
from analyzer import analizar_empresa
from analyzer import analizar_solvencia
from analyzer import extraer_source_data_f1
from analyzer import calcular_ratios_de_extraer_source_data_f2
import json
import os

#Aquí vamos a colocar los años de los documentos que vamos a descargar:
casa_grande = ["2016", "2017","2018", "2019", "2020", "2021", "2022", "2023", "2024", "2025"]

tabla_historial = {
    "Casa Grande" : {}
}

print("Se inicia el test para poder empezar la iteración de BD")

#Se inicia el bucle:-----------------------------------------------------
for año in casa_grande:
    nombre_importacion = f"data_xml/casa_grande{año}.xml" 

    #Test para verificar si el archivo existe:
    if not os.path.exists(nombre_importacion):
        print(f"El archivo {nombre_importacion} para el año {año} no existe")
        continue

    print(f"procesamiento del año ->{año}")

    #1- conexión al XML
    try:
        root_anual = ET.parse(nombre_importacion).getroot()
    except ET.ParseError as ex:
        print(f"\tAlereta, no se pudo leer el año: {año}, error en el archivo ")
        continue
    
    #2- Buscamos y encontramos el ID de cada elemento por su año:
    ids_anual = encontrar_id_año(año, root_anual)

    #3- Datos encontrados en el diccionario:
    data_empresa_anual = extraer_source_data_f1(root_anual, ids_anual)

    #4- Se calcula los datos de cada año:
    ratios_calculados_anual = calcular_ratios_de_extraer_source_data_f2(data_empresa_anual)

    #5- Añadimos la data y ratios analizados al nuevo diccionario:
    tabla_historial["Casa Grande"][año] = ratios_calculados_anual

    #Comentario opcional de funcionalidad del código:
    print(f"\n\tFuncionó con Éxito la lectura del archivo xml, para el año: |{año}\n\t")

#6- acabado el proceso de iteración guardamos en el Json:
with open("data_xml/reporte_analizado.json", "w", encoding="utf-8") as archivo_json: 
    json.dump(tabla_historial, archivo_json, indent=4, ensure_ascii=False)


print("\nSe realizó todo el proceso de guardado con éxito:")



# Aquí el archivo de la empresa a Analizar 
casa_grande_root = (ET.parse('data_xml/casa_grande2024.xml')).getroot()
cartavio_root = (ET.parse('data_xml/cartavio2024.xml')).getroot()

#Los años se expresan en ids contextRef:
id_casa_grande_2024 = encontrar_id_año("2024", casa_grande_root)
id_cartavio_2024 = encontrar_id_año("2024", cartavio_root)

tabla_horizontal = {}

# ejecucion, pero ahora las empresas están encapsuladas para atrapar el diccionario anidado de cada empresa

#------- Sección en mantenimiento, alejarse porfavor: ----------
print("a")
data_casa_grande = extraer_source_data_f1(casa_grande_root,id_casa_grande_2024)
ratios_casa_grande = calcular_ratios_de_extraer_source_data_f2(data_casa_grande)

data_cartavio = extraer_source_data_f1(cartavio_root, id_cartavio_2024)
ratios_cartavio = calcular_ratios_de_extraer_source_data_f2(data_cartavio)

#----------

tabla_horizontal["Casa Grande"] = ratios_casa_grande
tabla_horizontal["Cartavio"] = ratios_cartavio


#Aquí haremos una vizualización horizontal de el diccionario anidado:
print("\n"+"="*40)
print(f"{'Métrica financiera':<25} | {'Casa Grande':<15} | {'Cartavio':<15}") 
print("\n"+"="*40)

#Datos del diccionario que se van a mostrar:
ratios_a_mostrar = ['Net Income', 'Net Margin','ROE','ROA', 'Quick Ratio', 'Current Ratio', 'Debt Asset Ratio']

#Bucle para mostrarlo todo: 
for ratio in ratios_a_mostrar:
    valor_casaGrande = tabla_horizontal['Casa Grande'][ratio]
    valor_Cartavio = tabla_horizontal['Cartavio'][ratio]
    print(f"{ratio:<25} | {valor_casaGrande:<13.2f} | {valor_Cartavio:<13.2f}")
print("-"*40)
