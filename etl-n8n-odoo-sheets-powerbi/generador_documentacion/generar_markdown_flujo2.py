# generar_markdown_flujo2.py
# Lee el contenido estructurado de contenido_flujo2.py y genera un archivo .md

from contenido_flujo2 import (
    TITULO, INTRO, OBJETIVO, ARQUITECTURA, CONFIGURACION_NODOS,
    CODIGO_V1, CODIGO_V1_PROBLEMA, CODIGO_V2, CODIGO_V2_EXPLICACION,
    VALIDACION, VISUALIZACIONES, MEDIDA_DAX, ERRORES, LIMITACIONES,
    STACK_FINAL
)


def generar_markdown():
    lineas = []

    lineas.append(f"# {TITULO}\n")

    lineas.append(f"**Proyecto:** {INTRO['proyecto']}  ")
    lineas.append(f"**Stack:** {INTRO['stack']}  ")
    lineas.append(f"**Estado:** {INTRO['estado']}\n")

    lineas.append("## 1. Objetivo del Flujo 2\n")
    lineas.append(OBJETIVO + "\n")

    lineas.append("## 2. Arquitectura del flujo\n")
    lineas.append("```")
    lineas.append(ARQUITECTURA)
    lineas.append("```\n")

    lineas.append("## 3. Configuracion de nodos clave\n")
    for nodo in CONFIGURACION_NODOS:
        lineas.append(f"### {nodo['nombre']}\n")
        lineas.append("| Parametro | Valor |")
        lineas.append("|---|---|")
        for parametro, valor in nodo["filas"]:
            lineas.append(f"| {parametro} | {valor} |")
        lineas.append("")

    lineas.append("## 4. Evolucion del codigo (version 1 a version 2)\n")
    lineas.append("### Version 1 - fecha de ejecucion (con bug)\n")
    lineas.append("```javascript")
    lineas.append(CODIGO_V1)
    lineas.append("```\n")
    lineas.append(f"**Problema identificado:** {CODIGO_V1_PROBLEMA}\n")

    lineas.append("### Version 2 - fecha del pedido mas reciente (implementada)\n")
    lineas.append("```javascript")
    lineas.append(CODIGO_V2)
    lineas.append("```\n")
    lineas.append(f"**Explicacion del cambio:** {CODIGO_V2_EXPLICACION}\n")

    lineas.append("## 5. Validacion con datos reales\n")
    lineas.append(VALIDACION + "\n")

    lineas.append("## 6. Visualizaciones construidas en Power BI\n")
    lineas.append("| Visual | Tipo | Campos |")
    lineas.append("|---|---|---|")
    for visual, tipo, campos in VISUALIZACIONES:
        lineas.append(f"| {visual} | {tipo} | {campos} |")
    lineas.append("")

    lineas.append("### Medida DAX implementada\n")
    lineas.append("```")
    lineas.append(MEDIDA_DAX)
    lineas.append("```\n")

    lineas.append("## 7. Bitacora de errores y soluciones\n")
    for titulo_err, sintoma, causa, solucion in ERRORES:
        lineas.append(f"### {titulo_err}\n")
        lineas.append(f"**Sintoma:** {sintoma}\n")
        lineas.append(f"**Causa:** {causa}\n")
        lineas.append(f"**Solucion:** {solucion}\n")

    lineas.append("## 8. Limitaciones conocidas\n")
    lineas.append("| Limitacion | Detalle | Mejora propuesta |")
    lineas.append("|---|---|---|")
    for limitacion, detalle, propuesta in LIMITACIONES:
        lineas.append(f"| {limitacion} | {detalle} | {propuesta} |")
    lineas.append("")

    lineas.append("## 9. Stack tecnico final del proyecto completo\n")
    lineas.append("| Etapa | Herramienta | Funcion |")
    lineas.append("|---|---|---|")
    for etapa, herramienta, funcion in STACK_FINAL:
        lineas.append(f"| {etapa} | {herramienta} | {funcion} |")
    lineas.append("")

    return "\n".join(lineas)


if __name__ == "__main__":
    contenido = generar_markdown()

    with open("documentacion_flujo2.md", "w", encoding="utf-8") as f:
        f.write(contenido)

    print("Archivo generado: documentacion_flujo2.md")
