#The proyect start:
#1- The first step is know the Scheme="URL" and also the code of the <XBRLI:identifier>B08361
#2- The second step is extract and understand the times periods.

import xml.etree.ElementTree as ET

#nos conectamos al archivo:
tree = ET.parse('casaGrande2024.xml')
root = tree.getroot()

#Creamos el namespaces para que python entienda los tag de XBRLI: IFRS
namespaces = {'xbrli' : 'http://www.xbrl.org/2003/instace',
              'ifrs-full' : 'http://ifrs.org'}

#para buscar nuestro tabulador:
primer_elemento_ifrs = root.find('.//ifrs-full:*', namespaces)

#¿Se encontró un elemento?
if primer_elemento_ifrs is not None:
    print(f"Correctos NameSpaces, primera tag es: {primer_elemento_ifrs.tag}")
else:
    print("No se encontró las etiquetas del URL")
