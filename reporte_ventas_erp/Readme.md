
# Reporte de Ventas — Estructura ERP

![Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)

Plantilla de reporte de ventas construida sobre datos simulados 
con estructura tipo ERP. Separa la fuente de datos del análisis, 
usando fórmulas dinámicas (SUMIFS/COUNTIFS) que se actualizan 
solo al agregar nuevas ventas.

## Contenido
- `Datos_ERP`: registros de venta (fecha, vendedor, producto, monto)
- `Resumen`: KPIs, ventas por categoría, top productos, ranking de vendedores

## Metodología
Los datos y el análisis viven en hojas separadas para que la 
fuente nunca se modifique por accidente y el reporte se pueda 
reconstruir sin riesgo.

