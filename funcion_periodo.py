#We Create the analyzer of periods:

import xml.etree.ElementTree as ET
#Agrevamos una nueva librería para trabajar StarDate, EndDate en istancias anuales:
from datetime import datetime


#Esto es para limpiar el tag de nuestro código, para poderlo optimizar mucho mejor: 
def cortar_llaves(tag):
    return tag.split('}')[-1] if '}' in tag else tag

#empresa_a_buscar es el documento xml, cartavio2024.xml por ejemplo

def encontrar_id_año(año_buscado, empresa_a_buscar):
    # En caso de que el archivo XML no se haya cargado correctamente
    if empresa_a_buscar is None:
        print("No se puede realizar la búsqueda porque el archivo XML no se cargó.")
        return []

    #Separamos en dos listas para ver que ID va primero y qué ID va segundo:
    ids_periodo_anual = []
    ids_balance_instant = []
    

    for elemento in empresa_a_buscar.iter():
        nombre_limpio = cortar_llaves(elemento.tag)
        
        if nombre_limpio == "context":
            id_contexto =   elemento.get('id')


            tiene_segmento = any(cortar_llaves(child.tag)== "segment" for child in elemento.findall('.//*'))
            if tiene_segmento:
                continue

            #Variables para verificar las fechas:
            fecha_inicio =  None
            fecha_fin =  None
            fecha_instant = None

            for periodo in elemento.iter():
                if cortar_llaves(periodo.tag) =="period":
                    for sub_elemento in periodo:
                        sub_nombre = cortar_llaves(sub_elemento.tag)

                        if sub_nombre =="startDate":
                            fecha_inicio = sub_elemento.text
                        if sub_nombre == "endDate":
                            fecha_fin = sub_elemento.text
                        if sub_nombre == "instant":
                            fecha_instant = sub_elemento.text

            #Condición 1: ¿Es el id intervalo de tiempo[startDate, endDate]?
            if fecha_inicio and fecha_fin:
                if año_buscado in fecha_inicio or año_buscado in fecha_fin:
                    try:
                        # Calculamos los días de diferencia para asegurar que es anual y no trimestral
                        start_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
                        end_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
                        dias = (end_dt - start_dt).days
                        
                        # Un año real tiene entre 350 y 370 días (contando años bisiestos o cierres flotantes)
                        if 350 <= dias <= 370:
                            if id_contexto not in ids_periodo_anual:
                                ids_periodo_anual.append(id_contexto)
                    except ValueError:
                        # Por si las fechas vienen en otro formato de texto
                        if id_contexto not in ids_periodo_anual:
                            ids_periodo_anual.append(id_contexto)

            # Condición 2: ¿Es un instante de tiempo (Balance: Equity/Liabilities)?
            if fecha_instant:
                if año_buscado in fecha_instant:
                    if id_contexto not in ids_balance_instant:
                        ids_balance_instant.append(id_contexto)

    # Retornamos una lista ordenada: Primero los anuales de periodo, luego los de balance.
    # Esto garantiza que id_buscado[0] y id_buscado[1] tengan lo que Revenues o Assets necesitan sin pisarse.
    todo_ordenado = ids_periodo_anual + ids_balance_instant
    return todo_ordenado