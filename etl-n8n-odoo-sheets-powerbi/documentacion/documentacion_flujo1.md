# Documentación Técnica: ETL Google Sheets → Odoo con n8n

**Proyecto:** Automatización de creación de clientes desde pedidos de venta  
**Stack:** n8n Cloud, Odoo Online (Community), Google Sheets  
**Estado:** Flujo 1 completo y funcional, con limitación conocida documentada

## 1. Objetivo del proyecto

Construir un pipeline ETL (Extract, Transform, Load) que:
1. Extrae filas nuevas de un Google Sheet de pedidos
2. Transforma verificando si el cliente ya existe en el sistema ERP
3. Carga el contacto en Odoo si no existe, y marca la fila como procesada en Sheets

Esto demuestra el flujo típico de integración entre una fuente de datos manual
(hoja de cálculo) y un sistema ERP, usando una herramienta de automatización
low-code (n8n) como orquestador.

## 2. Arquitectura del flujo

```
Schedule Trigger (cada hora / manual para pruebas)
        -> Get row(s) in sheet (lee filas donde estatus = "nuevo")
        -> Get many contacts en Odoo (busca por email_cliente, Always Output Data: ON)
        -> IF1: {{ $json.id }} does not exist
               true  -> Update row in sheet directo (cliente ya existia)
               false -> Create a contact (Odoo) -> Update row in sheet
```

## 3. Configuración de credenciales

### Google Sheets OAuth2

| Campo | Valor |
|---|---|
| Tipo de credencial | Google Sheets OAuth2 API |
| Método de autenticación | Sign in with Google (OAuth2) |
| Permisos | Lectura y escritura de Sheets |

### Odoo API Key

| Campo | Valor |
|---|---|
| Tipo de credencial | Odoo API (API Key) |
| Host URL | https://[subdominio].odoo.com |
| Database | Mismo nombre que el subdominio (con guiones) |
| User | Email del usuario administrador de Odoo |
| Password | API Key generada desde Preferencias -> API Keys |

## 4. Estructura de datos de origen (Google Sheets)

| Columna | Tipo | Ejemplo |
|---|---|---|
| fecha_pedido | fecha | 2024-11-08 |
| nombre_cliente | texto | Julian Cauich |
| email_cliente | texto | julian@ejemplo.com |
| telefono | número | 9993458914 |
| producto | texto | Mouse inalámbrico |
| cantidad | número | 2 |
| precio_unitario | número | 350 |
| total | número | 700 |
| ciudad | texto | Mérida |
| estatus | texto (control) | nuevo / procesado |

## 5. Bitácora de errores y soluciones

### Error 1 — Autenticación con Odoo vía Google

**Síntoma:** Odoo no aceptaba la contraseña ni enviaba correo de restablecimiento.

**Causa:** La cuenta se había creado usando 'Sign in with Google', por lo que nunca existió una contraseña tradicional asociada.

**Solución:** Iniciar sesión siempre con el botón 'Entrar con Google' en lugar de email/contraseña.

### Error 2 — Recurso 'Contact' no aparece en el nodo Odoo

**Síntoma:** El selector de Recurso en el nodo Odoo solo mostraba Activity, Custom Resource, Opportunity — no Contact.

**Causa:** El módulo de Ventas (Sales) de Odoo no estaba instalado en la base de datos; sin él, el modelo de Contactos no está expuesto correctamente.

**Solución:** Instalar el módulo Sales desde Apps en Odoo. Esto activa Contactos como dependencia automática.

### Error 3 — Google Sheets no encuentra el documento por nombre

**Síntoma:** El selector 'From list' no mostraba el Google Sheet, aunque existía.

**Causa:** El nombre del documento contenía un guion largo (—), un carácter que el buscador de n8n no interpretaba correctamente.

**Solución:** Cambiar a selección 'By ID' y usar el ID del documento extraído directamente de la URL de Google Sheets.

### Error 4 — 'Invalid input for name: required but not set'

**Síntoma:** El nodo Create a contact fallaba al ejecutar aunque el campo Nombre tenía una expresión escrita.

**Causa:** El nodo anterior (Get row(s) in sheet) estaba en estado Deactivated, un toggle de encendido/apagado distinto al botón de ejecución.

**Solución:** Activar el nodo mediante el ícono de encendido/apagado (no el botón de play) antes de ejecutar el flujo completo.

### Error 5 — 'evaluated to a falsy value: a.ok(nodeExists)'

**Síntoma:** Error al ejecutar el flujo completo, sin mensaje claro de causa.

**Causa:** Un nodo (Create a contact) había quedado desconectado del resto del flujo tras una edición previa del canvas.

**Solución:** Verificar visualmente que todos los nodos tengan líneas de conexión completas en el canvas antes de ejecutar.

### Error 6 — Filtro no encuentra filas con estatus 'nuevo' pese a verse correctas

**Síntoma:** El nodo Get row(s) in sheet devolvía 'No output data' aunque la celda mostraba visualmente 'nuevo'.

**Causa:** Caracteres invisibles en la celda (espacios de no separación, saltos de línea ocultos), probablemente introducidos al copiar/pegar texto.

**Solución:** Borrar el contenido de la celda y escribirlo manualmente, carácter por carácter, en lugar de pegarlo.

### Error 7 — 'No output data' en Get many contacts detiene el flujo completo

**Síntoma:** Cuando el contacto buscado no existía en Odoo, el flujo se detenía por completo en ese nodo en lugar de continuar hacia el IF.

**Causa:** Comportamiento por defecto de n8n: un nodo sin datos de salida detiene la ejecución del flujo.

**Solución:** Activar la opción 'Always Output Data' en Settings del nodo Get many contacts, para que el flujo continúe hacia el IF.

### Error 8 — Contactos duplicados en Odoo

**Síntoma:** Varios contactos (Ana García, Luis Pérez, Carla López, etc.) aparecían dos veces en Odoo.

**Causa:** Durante las pruebas, el flujo se ejecutó varias veces sin el nodo IF correctamente conectado.

**Solución:** Eliminación manual de duplicados en Odoo. Preventivo: no ejecutar el flujo completo hasta confirmar que el IF está bien conectado.

### Error 9 — Condiciones del IF invertidas

**Síntoma:** Un cliente nuevo se marcaba como 'procesado' en Sheets pero nunca se creaba en Odoo.

**Causa:** La rama true del IF (condición 'does not exist') estaba conectada a Update row, y la rama false a Create a contact — al revés.

**Solución:** Intercambiar las conexiones: true -> Update row / false -> Create a contact -> Update row.

### Error 10 (limitación no resuelta) — 'Multiple matches found'

**Síntoma:** Al haber dos o más filas con estatus 'nuevo' simultáneamente, el nodo Create a contact fallaba con error de múltiples coincidencias.

**Causa:** Cuando el flujo procesa múltiples items en paralelo, las referencias cruzadas entre nodos ($('Node').item) pierden la asociación correcta con los datos originales de Sheets.

**Solución:** Solución identificada para próxima iteración: insertar un nodo SplitInBatches con tamaño de lote = 1 después de Get row(s) in sheet, para procesar cada fila de forma aislada. No implementado en esta versión por restricción de tiempo; el flujo funciona confiablemente procesando un registro nuevo a la vez.

## 6. Limitaciones conocidas

| Limitación | Impacto | Mitigación actual | Solución propuesta |
|---|---|---|---|
| Procesamiento de múltiples filas simultáneas | Alto — no escala para uso real con muchos pedidos por hora | Ejecutar el flujo una vez por cada registro nuevo | Nodo SplitInBatches con tamaño de lote = 1 |
| Sin manejo de errores de red/timeout hacia Odoo | Medio | Reintento manual | Activar 'Retry On Fail' en nodos críticos |
| No valida formato de email antes de crear contacto | Bajo | Ninguna | Nodo de validación antes de Create a contact |

## 7. Resultado verificado

Prueba funcional exitosa con el registro Julian Cauich
(email: julian@ejemplo.com):

1. Fila con estatus "nuevo" detectada correctamente por el filtro
2. Búsqueda en Odoo confirmó que el contacto no existía (Always Output
   Data permitió continuar)
3. IF correctamente evaluó la condición y dirigió a la rama de creación
4. Contacto creado exitosamente en Odoo con nombre, email, teléfono y ciudad
5. Fila en Sheets actualizada de "nuevo" a "procesado"

Prueba de no-duplicación exitosa: al reenviar un cliente ya existente
(Ana García) con estatus "nuevo", el flujo detectó la coincidencia en
Odoo y NO creó un registro duplicado, marcando la fila como procesada
directamente.

## 8. Stack técnico final

| Componente | Herramienta | Plan usado |
|---|---|---|
| Orquestación / ETL | n8n Cloud | Trial 14 días (Pro) |
| ERP / destino de datos | Odoo Online | Community (gratuito) |
| Origen de datos | Google Sheets | Cuenta personal Gmail |
| Autenticación Sheets | OAuth2 | — |
| Autenticación Odoo | API Key | — |
