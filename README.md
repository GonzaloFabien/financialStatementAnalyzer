# financialStatementAnalyzer
This is a analyzer of Financial Statements, primarily in finance matters.

El objetivo de crear este documento es nada más y menos que generar un lector de datos eficaz rápido que me permita analizar EEFF desde su publicación y con varíos años de datos y antelación:

Nota del día: si los archivos de la SMV presentan fallas, puedes depurarlos y resturarlos con :

-Solo es necesario cambiar el nombre del arhcivo 'buenaventura' por el nombre de los archivos que quieres iterar, en xml, luego pegalo en tu consola.

for anio in {2012..2025}; do
  [ -f "buenaventura${anio}.xml" ] && tr -d '\000' < "buenaventura${anio}.xml" | iconv -f WINDOWS-1252 -t UTF-8 -c > "buenaventura${anio}.xml.tmp" && mv "buenaventura${anio}.xml.tmp" "buenaventura${anio}.xml"
done
