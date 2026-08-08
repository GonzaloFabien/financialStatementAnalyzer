#We Create the analyzer of periods:

import xml.etree.ElementTree as ET

empresa_a_analizar = "casaGrande2024.xml"
tree = ET.parse(empresa_a_analizar)
root = tree.getroot()

#Esto es para limpiar el tag de nuestro código, para poderlo optimizar mucho mejor: 
def cortar_llaves(tag):
    return tag.split('}')[-1] if '}' in tag else tag

def encontrar_id_año(año_buscado):
    for elemento in root.iter():
        nombre_original = elemento.tag
        nombre_limpio = cortar_llaves(nombre_original)
        
        if nombre_limpio == "context":

            id_contexto =   elemento.get('id')
            #Variables para verificar las fechas:
            fecha_inicio =  None
            fecha_fin =  None
            sub_nombre = None

            for sub_elemento in elemento.iter():
                sub_nombre = cortar_llaves(sub_elemento.tag)

                if sub_nombre =="startDate":
                    fecha_inicio = sub_elemento.text
                if sub_nombre == "endDate":
                    fecha_fin = sub_elemento.text
            if fecha_inicio is not None and fecha_fin is not None:
                if año_buscado in fecha_inicio or año_buscado in fecha_fin:    
                    print(f"Encontramos el Id de | {año_buscado} | corresponde a | {id_contexto}")
                    return id_contexto

         



if __name__ == "__main__":
    encontrar_id_año("2024")