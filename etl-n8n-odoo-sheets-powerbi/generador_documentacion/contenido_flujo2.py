# contenido_flujo2.py
# Contenido estructurado de la documentación del Flujo 2: Odoo -> Dashboard -> Power BI
# Mismo patrón que contenido_flujo1.py: separar el CONTENIDO del CODIGO que lo genera

TITULO = "Documentacion Tecnica: ETL Odoo a Dashboard Sheets a Power BI"

INTRO = {
    "proyecto": "Extraccion de KPIs de ventas desde Odoo y visualizacion en Power BI",
    "stack": "n8n Cloud, Odoo Online, Google Sheets, Power BI Desktop",
    "estado": "Funcional, validado con datos reales de fechas distintas",
}

OBJETIVO = """Extraer periodicamente los pedidos de venta registrados en Odoo,
calcular indicadores clave (KPIs) de negocio, y almacenar un historial de
estos KPIs en Google Sheets, que a su vez alimenta un dashboard en Power BI.

Esto representa la etapa final de un pipeline ETL completo: una vez que los
datos transaccionales viven en el ERP (Odoo), se necesita un proceso separado
que los resuma en indicadores de negocio entendibles para gerencia, sin que
cada persona tenga que entrar al ERP a sacar sus propios numeros."""

ARQUITECTURA = """Schedule Trigger (diario, configurable)
        => Custom Resource: sale.order en Odoo (Get Many, Return All: ON)
        => Code (JS): calcula KPIs - total pedidos, total ventas,
           ticket promedio, fecha del pedido mas reciente
        => Append row in sheet (Dashboard_Ventas en Google Sheets)
        => Power BI Desktop (consumidor final, conectado via CSV publicado)"""

CONFIGURACION_NODOS = [
    {
        "nombre": "Custom Resource - sale.order",
        "filas": [
            ("Resource", "Custom Resource"),
            ("Operation", "Get Many"),
            ("Resource Name or ID", "By ID -> sale.order"),
            ("Return All", "ON"),
        ],
    },
    {
        "nombre": "Append row in sheet",
        "filas": [
            ("Resource", "Sheet Within Document"),
            ("Operation", "Append Row"),
            ("Document", "By ID - ID del spreadsheet ETL Ventas Portafolio"),
            ("Sheet", "Dashboard_Ventas"),
        ],
    },
]

CODIGO_V1 = '''const fechaActualizacion = new Date().toISOString().split('T')[0];'''

CODIGO_V1_PROBLEMA = """Esta linea siempre devuelve la fecha del momento en que
se ejecuta el flujo, sin importar cuando ocurrieron realmente los pedidos en
Odoo. Al ejecutar el flujo varias veces el mismo dia durante las pruebas,
todas las filas del dashboard quedaron con la misma fecha, y una grafica de
linea por fecha termino sumando todos los valores en un solo punto en vez de
mostrar una evolucion temporal."""

CODIGO_V2 = '''const pedidos = $input.all();

const totalPedidos = pedidos.length;

const totalVentas = pedidos.reduce((sum, p) => {
  return sum + (p.json.amount_total || 0);
}, 0);

const ticketPromedio = totalPedidos > 0
  ? (totalVentas / totalPedidos).toFixed(2)
  : 0;

// Usa la fecha real del pedido mas reciente en Odoo (date_order),
// en lugar de la fecha de ejecucion del flujo.
const fechasPedidos = pedidos
  .map(p => p.json.date_order)
  .filter(f => f)
  .sort()
  .reverse();

const fechaActualizacion = fechasPedidos.length > 0
  ? fechasPedidos[0].split(' ')[0]
  : new Date().toISOString().split('T')[0];

return [{
  json: {
    fecha_actualizacion: fechaActualizacion,
    total_pedidos: totalPedidos,
    total_ventas_mxn: totalVentas.toFixed(2),
    ticket_promedio: ticketPromedio
  }
}];'''

CODIGO_V2_EXPLICACION = """Ahora la fecha del registro de KPIs corresponde al
pedido de venta mas reciente registrado en Odoo (campo date_order), no al
momento de ejecucion del script. Esto es mas correcto desde el punto de vista
de negocio: un reporte de KPIs debe reflejar cuando ocurrio la actividad
comercial, no cuando se genero el reporte."""

VALIDACION = """Validacion exitosa con datos reales: al agregar pedidos nuevos
en Odoo en fechas posteriores (creando un total acumulado de 51 pedidos a lo
largo de varios dias), el dashboard en Power BI mostro correctamente una
grafica de linea con tendencia descendente real entre fechas distintas,
confirmando que el codigo corregido (version 2) funciona como se esperaba.

KPIs verificados en la version final:
- Total de ventas: $449,860 MXN (acumulado del historial)
- Total de pedidos: 51
- Ticket promedio: $50,400 MXN (promedio de las distintas ejecuciones
  registradas en el historial)"""

VISUALIZACIONES = [
    ("KPI: Total Ventas", "Tarjeta", "total_ventas_mxn"),
    ("KPI: Total Pedidos", "Tarjeta", "total_pedidos"),
    ("KPI: Ticket Promedio", "Tarjeta", "ticket_promedio"),
    ("Evolucion de ventas", "Grafico de lineas", "Eje X: fecha_actualizacion / Eje Y: total_ventas_mxn"),
    ("Pedidos por dia", "Grafico de columnas", "Eje X: fecha_actualizacion / Eje Y: total_pedidos"),
    ("Detalle", "Tabla", "Todas las columnas"),
]

MEDIDA_DAX = "Ventas Promedio Diarias = AVERAGE(Dashboard_Ventas[total_ventas_mxn])"

ERRORES = [
    (
        "Error 1 - Recurso Sales Order no disponible en el nodo Odoo",
        "El listado de Recursos del nodo Odoo no mostraba Sales Order como opcion predefinida.",
        "El modulo instalado en esta instancia de Odoo no expuso ese recurso directamente en el listado estandar del nodo n8n.",
        "Usar Custom Resource con el nombre tecnico del modelo en Odoo (sale.order) en lugar del recurso predefinido.",
    ),
    (
        "Error 2 - No output data returned al consultar pedidos",
        "El nodo Custom Resource devolvia vacio al ejecutar.",
        "No existian pedidos de venta reales en Odoo - el Flujo 1 unicamente habia creado contactos, nunca pedidos.",
        "Crear pedidos de venta manualmente en Odoo asociados a los contactos ya existentes, para tener datos sobre los cuales calcular KPIs.",
    ),
    (
        "Error 3 - fecha_actualizacion interpretada como texto largo en Power BI",
        "La columna de fecha se mostraba como 'lunes, 22 de junio de 2026' en vez de un valor de fecha manipulable.",
        "Power BI infirio el tipo de dato como texto al cargar el CSV publicado.",
        "En el Editor de Power Query, cambiar el tipo de la columna explicitamente a Fecha desde el menu de clic derecho.",
    ),
    (
        "Error 4 - Grafica de linea muestra un solo punto agregado en vez de tendencia",
        "Con varias filas en el historial, la grafica de evolucion de ventas mostraba un unico punto en vez de una serie temporal.",
        "El codigo original (version 1) generaba la misma fecha para todas las ejecuciones del mismo dia, y Power BI suma automaticamente los valores que comparten la misma fecha en el eje X.",
        "Correccion del codigo fuente a la version 2 (usar date_order de Odoo). Verificado exitosamente al capturar pedidos en dias distintos - ver seccion de Validacion.",
    ),
]

LIMITACIONES = [
    (
        "ciudad_top y producto_top con valor fijo",
        "Estos dos KPIs se dejaron como texto fijo 'Ver Odoo' en lugar de calcularse dinamicamente, por alcance del proyecto en su primera version.",
        "Agregar logica en el nodo Code para calcular la ciudad y producto con mas ventas usando agrupacion y conteo sobre las lineas de pedido.",
    ),
    (
        "Actualizacion del dashboard en Power BI es manual",
        "Requiere clic en Actualizar cada vez que se quiere ver el historial mas reciente.",
        "Usar Power BI Service con actualizacion programada, en lugar de Power BI Desktop.",
    ),
]

STACK_FINAL = [
    ("Origen de datos", "Google Sheets", "Captura manual de pedidos entrantes"),
    ("ETL - carga a ERP", "n8n (Flujo 1)", "Crea contactos en Odoo, evita duplicados"),
    ("Sistema ERP", "Odoo Online", "Almacena contactos y pedidos de venta"),
    ("ETL - extraccion de KPIs", "n8n (Flujo 2)", "Calcula indicadores y los registra en Sheets"),
    ("Historial de KPIs", "Google Sheets", "Tabla append-only de metricas por fecha"),
    ("Visualizacion ejecutiva", "Power BI Desktop", "Dashboard con tarjetas, graficas y medidas DAX"),
]
