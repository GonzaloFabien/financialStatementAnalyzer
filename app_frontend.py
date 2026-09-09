import json

#1- Apuntamos al archivo que guarda nuestra información"
ruta_json = "data_xml/reporte_analizado.json"

print("Inciio de interfaz financiera")

#2- Se cargan los datos históricos 
with open(ruta_json, "r", encoding="utf-8") as archivo:
    base_datos = json.load(archivo)

print("Se cargó correctamente la base de datos")

#3- Accedemos a los datos de la empresa
datos_empresa = base_datos['Casa Grande']

"""
#Esto es para saber los tags disponibles a utilizar del diccionario:
ratos_test = datos_empresa['2016'].keys()
print(list(ratos_test))
"""
#4- Los mostramos en una lista ordenada
años_disponibles = sorted(list(datos_empresa.keys()))
print(f"\nAños historicos detectados :  {años_disponibles}")

#5- Redefinimos los ratios para poder utilizarlos libremente y en el orden deseado.

ratios_a_mostrar_1 = ['Net Income', 'Margen Neto', 'ROE', 'ROA', 'Prueba ácida', 'Ratio Deuda/Activo' ]

#6- Creamos la cabecera horizontal uniendo los años del JSON:
columna_por_años = " | ".join([f"{año:<10}" for año in años_disponibles])
cabecera = f"{'Ratio /  ': <22} | {columna_por_años}"

#Mostramos temporalmente en consola

print("\n" + "=" *len(cabecera))
print(cabecera)
print("="*len(cabecera))
print("\n")

#7- Mostrar en bucle los años
for ratio in ratios_a_mostrar_1:
    valores_fila = []

    for año in años_disponibles:
        #Se entra al JSON:
        valor = datos_empresa[año].get(ratio, 0)

        #Formateamos el numero con el formato
        valores_fila.append(f"{valor:<10.2f}")

        #Guardamos en formato 2. decimales
    fila_completa = " | ".join(valores_fila)

        #Se imprime en consola con formato:
    print(f"{ratio:<22} | {fila_completa}")

print("="*len(cabecera))