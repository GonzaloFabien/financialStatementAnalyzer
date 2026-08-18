#The proyect start:
#1- The first step is know the Scheme="URL" and also the code of the <XBRLI:identifier>B08361
#2- The second step is kwnow the taxonomy of the xml document by 'namespaces.py'

import xml.etree.ElementTree as ET

#conexión con el xml:


#------De a partir de aquí crearemos la funcón:------   
def buscar_elemento(nombre_tag, id_buscado, nombre_empresa):

    tree = ET.parse(nombre_empresa)
    root = tree.getroot()

    for elementos in root.iter():
        elemento_iterado = elementos.tag
        elemento_recortado = None
        elemento_encontrado = None #Si lanza None es porque no se encontró nada


        if '}' in  elemento_iterado:
            recortar = elemento_iterado.split('}')
            elemento_recortado = recortar[-1]
        else: 
            elemento_recortado = elemento_iterado

        #Esto para el id[0]
        if elemento_recortado == nombre_tag and id_buscado[0] == elementos.get('contextRef'):
            elemento_encontrado = elementos.text
            return int(elemento_encontrado)
            print(f"nombre del tag : {nombre_tag} = || {elementos.text} || con id:{elementos.get('contextRef')}")

        #Si lo anterior devuelve None, entonces id[1]
        if elemento_recortado == nombre_tag and id_buscado[1] == elementos.get('contextRef'):
                    elemento_encontrado = elementos.text
                    return int(elemento_encontrado)
                    print(f"nombre del tag : {nombre_tag} = || {elementos.text} || con id:{elementos.get('contextRef')}")

    

if __name__ == "__main__":
    print("hola")