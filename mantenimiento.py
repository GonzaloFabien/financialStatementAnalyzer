import xml.etree.ElementTree as ET

def obtener_context_id_por_año(root, año_buscado):
    """
    Busca en los <context> del XML el ID que corresponda al año especificado
    para un periodo de tipo "duration" (desde el 1 de enero al 31 de diciembre).
    """
    # XBRL usa un namespace estándar para los contextos (generalmente xbrli)
    año_str = str(año_buscado)
    id_er = None
    id_bg = None


    # Buscamos de forma genérica ignorando el prefijo para evitar conflictos
    for context in root.findall('.//{*}context'):
        context_id = context.get('id')
        period = context.find('.//{*}period')

        if period is not None:
            start_ = period.find('.//{*}startDate')
            end_ = period.find('.//{*}endDate')
            
            if start_ is not None and end_ is not None:
                # Modificado: Evitamos agarrar trimestres (Q1, Q2) asegurando que el rango sea de casi un año
                if año_str in start_.text and año_str in end_.text and "-01-" in start_.text:
                    id_er = context_id
            
            # Buscar instante (Balance General)
            instant = period.find('.//{*}instant')
            if instant is not None and año_str in instant.text:
                id_bg = context_id
                
    return {"ER": id_er, "BG": id_bg}

#Genramos un test para ver si realmente funciona:

#root_anual = ET.parse("../data_xml/cartavio2017.xml").getroot()
#print(obtener_context_id_por_año(root_anual, "2017"))