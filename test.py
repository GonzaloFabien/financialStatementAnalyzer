import xml.etree.ElementTree as ET
from funcion_buscar import buscar_elemento
from funcion_periodo import encontrar_id_año
from analyzer import analizar_empresa
from analyzer import analizar_solvencia

#Los años se expresan en ids contextRef:
año_2024 = encontrar_id_año("2024")
año_2023 = encontrar_id_año("2023")

# Aquí el archivo de la empresa a Analizar 
nombre_empresa = (ET.parse('casaGrande2024.xml')).getroot()
empresa_2 = (ET.parse('cartavio2024.xml')).getroot()


#Pese a los cambios igual podemos invocar, datos tags standars como el efectivo:
efectivo_cartavio_2024 = buscar_elemento('CashAndCashEquivalents', año_2024, empresa_2)
print(f"\n el efectivo de cartavio es {efectivo_cartavio_2024} para el 2024")

# EJECUCIÓN: Llamamos a tu función para las dos empresas de forma directa
analizar_empresa(nombre_empresa, año_2024,"Casa Grande")
analizar_empresa(empresa_2,año_2024 ,"Cartavio")

#Utilizamos los demás métodos:
analizar_solvencia(nombre_empresa, año_2024,"Casa Grande")
