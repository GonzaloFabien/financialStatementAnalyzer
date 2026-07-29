#The proyect start:
#1- The first step is know the Scheme="URL" and also the code of the <XBRLI:identifier>B08361
#2- The second step is kwnow the taxonomy of the xml document by 'namespaces.py'

import xml.etree.ElementTree as ET

#conexión con el xml:
tree = ET.parse("casaGrande2024")
root = tree.getroot()

#3- Next, use the namespace with the taxonomy:
namespaces = {'ifrs-full': 'http://ifrs.org'}

#