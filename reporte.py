import json
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker 

nombre_empresa_1 = "Casa Grande"
nombre_empresa_2 = "Cartavio"

#1- Conectamos a la BD Json:
carpeta_sctipt_actual = os.path.dirname(os.path.abspath(__file__))
ruta_jsonl = os.path.abspath(os.path.join(carpeta_sctipt_actual,"data_xml","reporte_analizado.json"))


with open(ruta_json, "r", encoding="utf-8") as archivo:
    datos_personalizdos  = json.load(archivo)

#2- Extraemos los diccionarios de ambas emrpesas:
diccionario_casa_grande = datos_personalizdos.get('Casa Grande', {})
diccionario_cartavio =  datos_personalizdos.get('Cartavio', {})

#3- Detectamos los años que comparten ambas empresas:
años_casa_grande = set(diccionario_casa_grande.keys())
años_cartavio = set(diccionario_casa_grande.keys())
años_comunes = sorted(list(años_casa_grande.intersection(años_cartavio)))

"""
#-----IMPORTANTE, aquí el ratio que queremos comparar/MOSTRAR:
"""

ratio_a_graficar = 'Net Margin'

#4- Aquí de desgloza los valores del ratio a graficar 'Net Income' para cada año disponible
valores_casa_grande = [diccionario_casa_grande[año].get(ratio_a_graficar, 0) for año in años_comunes]
valores_cartavio = [diccionario_cartavio[año].get(ratio_a_graficar, 0) for año in años_comunes]

"""
    DISEÑO DEL GRÁFICO:
"""
plt.plot(años_comunes, valores_casa_grande, marker="o", linewidth=1.5, color="#21B2DB", label=nombre_empresa_1)
plt.plot(años_comunes, valores_cartavio, marker="s", linewidth=1.5,color="#ED9B24", label=nombre_empresa_2)

plt.title(f"Comparativa : {ratio_a_graficar} anual", fontsize=14, fontweight="bold")
plt.xlabel("Años fiscales", fontsize=12)
plt.ylabel(" %/$", fontsize=12)



"""
    Configuración opcional:
"""
# Cuadriculas de fondo
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11)

# Layout de los margenes del gráfico:
plt.tight_layout()

"""
    PLASMAR GRÁFICO:
"""
#correción del gráfico en el eje Y, porcentual y en millones (000,000)
def formatear_eje_y(valor, pos): 
    #Si el valor del tag es menor a |10| o sea su valor absoluto, entonces es un valor_porcentual:
    if abs(valor) < 100:
        return f"{valor:.1f}%"
    else:
        #al ser un número grande, no es posible que sea porcentual y se mantiene:
        datos_en_millones = valor/1_000_000 #podemos utilizar esto para ver que son millones
        return f"{datos_en_millones:.1f}M"
"""Nota: Aunque reparamos el eje_y podría tener poblemas con ratios corrientes, ya que podrían ser superiores a 100
si eso pasa, entonces puedes subir el humbral de 100 a 500 etc, o cambiar la forma en que se expresa el dato en su 
función de como se guarda en su diccionario, ya no de forma porcentual si no en decimal"""


plt.gca().yaxis.set_major_formatter( ticker.FuncFormatter(formatear_eje_y))
plt.show()