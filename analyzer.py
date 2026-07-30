#The proyect start:
#1- The first step is know the Scheme="URL" and also the code of the <XBRLI:identifier>B08361
#2- The second step is kwnow the taxonomy of the xml document by 'namespaces.py'

import xml.etree.ElementTree as ET

#conexión con el xml:
nombre_empresa = "casaGrande2024.xml"
tree = ET.parse(nombre_empresa)
root = tree.getroot()

#3- We define the attributte we have been searching for:

cuenta_efectivo = 'CashAndCashEquivalents'
monto_efectivo = None
contexto_efectivo = None

#Is the '}' be inside the tags?
for elemnts in root.iter():
    
    nombre_corto_temp = elemnts.tag
    if '}' in nombre_corto_temp:
        partes = nombre_corto_temp.split('}')
        nombre_limpio_tag = partes[-1]
    else: 
        nombre_limpio_tag = nombre_corto_temp

#4- We find the tag and the attribute
    if nombre_limpio_tag == cuenta_efectivo:
        monto_efectivo = elemnts.text
        contexto_efectivo = elemnts.get('contextRef')
        print(f"-> Econtrado: {nombre_limpio_tag} | monto: {monto_efectivo} | contexto: {contexto_efectivo}")