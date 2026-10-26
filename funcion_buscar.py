import xml.etree.ElementTree as ET

def buscar_elemento(nombre_tag, id_buscado, root):
    # 1. SALVAGUARDA: Si el ID es None (porque el año no existe en el XML), evitamos el error y salimos
    if id_buscado is None:
        return None

    for elementos in root.iter():
        elemento_iterado = elementos.tag
        elemento_recortado = None

        if '}' in elemento_iterado:
            recortar = elemento_iterado.split('}')
            elemento_recortado = recortar[-1]
        else: 
            elemento_recortado = elemento_iterado

        # 2. COMPARACIÓN DIRECTA: Comparamos el tag y el ID completo sin usar corchetes [0] o [1]
        if elemento_recortado == nombre_tag and elementos.get('contextRef') == id_buscado:
            if elementos.text is not None:
                try:
                    # Imprimir antes del return (si se pone después, el código nunca llega a leerlo)
                    # print(f"nombre del tag : {nombre_tag} = || {elementos.text} || con id:{elementos.get('contextRef')}")
                    
                    # Convertimos a float primero por si el XML trae decimales (.00) y luego a int
                    return int(float(elementos.text))
                except ValueError:
                    return None
                    
    return None # Si recorrió todo el XML y no hizo match
