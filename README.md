# financialStatementAnalyzer
This is a analyzer of Financial Statements, primarily in finance matters.

El objetivo de crear este documento es nada más y menos que generar un lector de datos eficaz rápido que me permita analizar EEFF desde su publicación y con varíos años de datos y antelación:

Nota del día: si los archivos de la SMV presentan fallas, puedes depurarlos y resturarlos con :

-Solo es necesario cambiar el nombre del arhcivo 'buenaventura' por el nombre de los archivos que quieres iterar, en xml, luego pegalo en tu consola.

for anio in {2012..2025}; do
  [ -f "buenaventura${anio}.xml" ] && tr -d '\000' < "buenaventura${anio}.xml" | iconv -f WINDOWS-1252 -t UTF-8 -c > "buenaventura${anio}.xml.tmp" && mv "buenaventura${anio}.xml.tmp" "buenaventura${anio}.xml"
done



Para agregar la documentación, respecto a la importación de datos de SMV y US-GAAP, existe una discrepancia en el código que aun no he podido describir, del todo, ocurre cuando importamos datos con analyzer.py especifiamente en el id_instant, que debe cambiarse su valor de [0] para empresas nacionales de la SMV que usa IFRS, y [1] para las emprsas que usan US-GAAP
ids_instant[0] para IFRS SMV
ids_instant[2] para US-GAAP SEC



-----Excel----
en frontend/app_desktop puedes mostrar o exportar los datos de las empresas, cambiando tan solo una variable, ' def ejectuar_exportacion(self):' es el encargado de exportar el código a excel, si quieres exportar toda la base de datos, quita el comentario "#" de la linea que dice ratios a exportar, ya que lanza o tambien está anlazada a la lista incial de tag que podemos configurar.
O sea que si quieres que exporte TODOS LOS DATOS DE TODAS LAS EMPRESAS DE TODOS LOS TAGS, 
usa ratios_a_exportar =  list(self.base_datos['Casa Grande'][primer_año].keys())
    en vez de  valores_a_mostrar, ya que lo anterior está vinculado a todos los datos
