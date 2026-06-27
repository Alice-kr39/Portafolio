

# generar_markdown.py
# Lee el contenido estructurado de contenido_flujo1.py y genera un archivo .md

from contenido_flujo1 import (
    TITULO, INTRO, OBJETIVO, ARQUITECTURA, CREDENCIALES,
    ESTRUCTURA_DATOS, ERRORES, LIMITACIONES, RESULTADO, STACK_FINAL
)


def generar_markdown():
    """Construye el contenido completo del archivo Markdown como un string."""
    lineas = []

    # Título principal
    lineas.append(f"# {TITULO}\n")

    # Introducción
    lineas.append(f"**Proyecto:** {INTRO['proyecto']}  ")
    lineas.append(f"**Stack:** {INTRO['stack']}  ")
    lineas.append(f"**Estado:** {INTRO['estado']}\n")

    # Objetivo
    lineas.append("## 1. Objetivo del proyecto\n")
    lineas.append(OBJETIVO + "\n")

    # Arquitectura
    lineas.append("## 2. Arquitectura del flujo\n")
    lineas.append("```")
    lineas.append(ARQUITECTURA)
    lineas.append("```\n")

    # Credenciales
    lineas.append("## 3. Configuración de credenciales\n")
    for cred in CREDENCIALES:
        lineas.append(f"### {cred['nombre']}\n")
        lineas.append("| Campo | Valor |")
        lineas.append("|---|---|")
        for campo, valor in cred["filas"]:
            lineas.append(f"| {campo} | {valor} |")
        lineas.append("")

    # Estructura de datos
    lineas.append("## 4. Estructura de datos de origen (Google Sheets)\n")
    lineas.append("| Columna | Tipo | Ejemplo |")
    lineas.append("|---|---|---|")
    for columna, tipo, ejemplo in ESTRUCTURA_DATOS:
        lineas.append(f"| {columna} | {tipo} | {ejemplo} |")
    lineas.append("")

    # Errores
    lineas.append("## 5. Bitácora de errores y soluciones\n")
    for titulo, sintoma, causa, solucion in ERRORES:
        lineas.append(f"### {titulo}\n")
        lineas.append(f"**Síntoma:** {sintoma}\n")
        lineas.append(f"**Causa:** {causa}\n")
        lineas.append(f"**Solución:** {solucion}\n")

    # Limitaciones
    lineas.append("## 6. Limitaciones conocidas\n")
    lineas.append("| Limitación | Impacto | Mitigación actual | Solución propuesta |")
    lineas.append("|---|---|---|---|")
    for limitacion, impacto, mitigacion, propuesta in LIMITACIONES:
        lineas.append(f"| {limitacion} | {impacto} | {mitigacion} | {propuesta} |")
    lineas.append("")

    # Resultado
    lineas.append("## 7. Resultado verificado\n")
    lineas.append(RESULTADO + "\n")

    # Stack final
    lineas.append("## 8. Stack técnico final\n")
    lineas.append("| Componente | Herramienta | Plan usado |")
    lineas.append("|---|---|---|")
    for componente, herramienta, plan in STACK_FINAL:
        lineas.append(f"| {componente} | {herramienta} | {plan} |")
    lineas.append("")

    # Unimos todas las líneas con salto de línea
    return "\n".join(lineas)


if __name__ == "__main__":
    contenido = generar_markdown()

    # Guardamos el resultado en un archivo .md
    with open("documentacion_flujo1.md", "w", encoding="utf-8") as f:
        f.write(contenido)

    print("Archivo generado: documentacion_flujo1.md")