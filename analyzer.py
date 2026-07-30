#The proyect start:
#1- The first step is know the Scheme="URL" and also the code of the <XBRLI:identifier>B08361
#2- The second step is kwnow the taxonomy of the xml document by 'namespaces.py'

import xml.etree.ElementTree as ET

#conexión con el xml:
nombre_empresa = "casaGrande2024.xml"
tree = ET.parse(nombre_empresa)
root = tree.getroot()

#3- We define the attributte we have been searching for:

nombre_cuenta = 'CashAndCashEquivalents'
monto_efectivo = None
contexto_efectivo = None

#Is the '}' be inside the tags?


for elementos in root.iter():
    #Define the elements:
    elemento_iterado = elementos.tag
    elemento_recortado = None
    
    if '}' in elemento_iterado:
        cortar = elemento_iterado.split('}')
        elemento_recortado = cortar[-1]
    else:
        elemento_recortado = elemento_iterado

    #Busqueda: 
    if elemento_recortado == nombre_cuenta:
        monto_efectivo = elementos.text
        contexto_efectivo = elementos.get('contextRef')
        print(f"tag {elemento_recortado}| valor =  {monto_efectivo} | con Id de = {contexto_efectivo}")
    
    