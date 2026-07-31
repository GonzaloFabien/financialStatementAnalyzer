#The proyect start:
#1- The first step is know the Scheme="URL" and also the code of the <XBRLI:identifier>B08361
#2- The second step is kwnow the taxonomy of the xml document by 'namespaces.py'

import xml.etree.ElementTree as ET

#conexión con el xml:
nombre_empresa = "casaGrande2024.xml"
tree = ET.parse(nombre_empresa)
root = tree.getroot()

#------De a partir de aquí crearemos la funcón:------   
def buscar_elemento(nombre_tag):

    for elementos in root.iter():
        elemento_iterado = elementos.tag
        elemento_recortado = None

        if '}' in  elemento_iterado:
            recortar = elemento_iterado.split('}')
            elemento_recortado = recortar[-1]
        else: 
            elemento_recortado = elemento_iterado

        if elemento_recortado == nombre_tag:
            print(f"elemento encontrado:")
            print(f"nombre  tag :{elementos.text} | valor de :{elementos.text} | con id:{elementos.get('contextRef')}")

    return elementos.text

if __name__ == "__main__":
    print("hola")