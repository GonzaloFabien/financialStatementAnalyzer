#The proyect start:
#1- The first step is know the Scheme="URL" and also the code of the <XBRLI:identifier>B08361
#2- The second step is kwnow the taxonomy of the xml document by 'namespaces.py'

import xml.etree.ElementTree as ET

#conexión con el xml:
nombre_empresa = "casaGrande2024.xml"
tree = ET.parse(nombre_empresa)
root = tree.getroot()

nombre_tag = 'CashAndCashEquivalents'
#monto_tag = None
#contexto_tag = None

#Buscamos el tag borrando primero las interferencias:

for elementos in root.iter():
    #Creamos dos varibles de visualización:
    elemento_buscado = elementos.tag
    elemento_recortado = None #Vamos a trabajar con el elemento recortado

    if '}' in elemento_buscado:
        elemento_cortado = elemento_buscado.split('}')
        elemento_recortado = elemento_cortado[-1]
    else:
        elemento_recortado = elemento_buscado
    #Una vez recotado ahora si podemos verificar si coincide con lo que el tag que buscamos:

    if elemento_recortado == nombre_tag:
        print("elemento encontrado")
        print(f"{nombre_tag} : {elementos.text} | usando el id: {elementos.get('contextRef')}")