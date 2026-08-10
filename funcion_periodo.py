#We Create the analyzer of periods:

import xml.etree.ElementTree as ET

empresa_a_analizar = "casaGrande2024.xml"
tree = ET.parse(empresa_a_analizar)
root = tree.getroot()

#Esto es para limpiar el tag de nuestro código, para poderlo optimizar mucho mejor: 
def cortar_llaves(tag):
    return tag.split('}')[-1] if '}' in tag else tag

def encontrar_id_año(año_buscado):
    #Creamos el array para ids[]
    array_ids = []

    for elemento in root.iter():
        nombre_original = elemento.tag
        nombre_limpio = cortar_llaves(nombre_original)
        
        if nombre_limpio == "context":

            id_contexto =   elemento.get('id')
            #Variables para verificar las fechas:
            fecha_inicio =  None
            fecha_fin =  None
            fecha_instant = None
            sub_nombre = None

            for sub_elemento in elemento.iter():
                sub_nombre = cortar_llaves(sub_elemento.tag)

                if sub_nombre =="startDate":
                    fecha_inicio = sub_elemento.text
                if sub_nombre == "endDate":
                    fecha_fin = sub_elemento.text
                if sub_nombre == "instant":
                    fecha_instant = sub_elemento.text

            #Condición 1: ¿Es el id intervalo de tiempo[startDate, endDate]?
            if fecha_inicio is not None and fecha_fin is not None:
                if año_buscado in fecha_inicio or año_buscado in fecha_fin:
                    if id_contexto not in array_ids:
                        array_ids.append(id_contexto)
                        print(f"Encontramos el Id de | {año_buscado} | corresponde a | {id_contexto}")
                       
            #Condición 2: ¿Es el id un instante de tiempo?
            if fecha_instant is not None:
                if año_buscado in fecha_instant:
                    if id_contexto not in array_ids:
                        array_ids.append(id_contexto)
                        print(f"Encontramos en el año {año_buscado} | el instante | {id_contexto}")

    #Una vez terminado el bucle devuele el valor de los array_ids[]:
    print(f"El valor para el año {año_buscado} son = || {array_ids}")
    return array_ids

if __name__ == "__main__":
    encontrar_id_año("2024")