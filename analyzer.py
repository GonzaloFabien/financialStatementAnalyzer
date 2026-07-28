#The proyect start:
#1- The first step is know the Scheme="URL" and also the code of the <XBRLI:identifier>B08361
#2- The second step is extract and understand the times periods.

import xml.etree.ElementTree as ET

#nos conectamos al archivo:
tree = ET.parse('casaGrande2024.xml')
root = tree.getroot()

print(f"etique principal: {root.tag}")