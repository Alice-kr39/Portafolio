# generar_pdf_flujo2.py
# Lee el contenido estructurado de contenido_flujo2.py y genera un archivo .pdf
# Reutiliza la clase DocumentoPDF definida en generar_pdf.py (la del Flujo 1)

from generar_pdf import DocumentoPDF
from contenido_flujo2 import (
    TITULO, INTRO, OBJETIVO, ARQUITECTURA, CONFIGURACION_NODOS,
    CODIGO_V1, CODIGO_V1_PROBLEMA, CODIGO_V2, CODIGO_V2_EXPLICACION,
    VALIDACION, VISUALIZACIONES, MEDIDA_DAX, ERRORES, LIMITACIONES,
    STACK_FINAL
)


def construir_pdf():
    pdf = DocumentoPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ---------- Portada / título ----------
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, pdf.limpiar(TITULO))
    pdf.ln(4)

    pdf.etiqueta_valor("Proyecto", INTRO["proyecto"])
    pdf.etiqueta_valor("Stack", INTRO["stack"])
    pdf.etiqueta_valor("Estado", INTRO["estado"])
    pdf.ln(4)

    # ---------- Objetivo ----------
    pdf.titulo_seccion("1. Objetivo del Flujo 2")
    pdf.parrafo(OBJETIVO)

    # ---------- Arquitectura ----------
    pdf.titulo_seccion("2. Arquitectura del flujo")
    pdf.set_font("Courier", "", 9)
    pdf.multi_cell(0, 5, pdf.limpiar(ARQUITECTURA))
    pdf.ln(4)

    # ---------- Configuración de nodos ----------
    pdf.titulo_seccion("3. Configuracion de nodos clave")
    for nodo in CONFIGURACION_NODOS:
        pdf.subtitulo(nodo["nombre"])
        pdf.tabla(
            encabezados=["Parametro", "Valor"],
            filas=nodo["filas"],
            anchos=[60, 130],
        )

    # ---------- Evolución del código ----------
    pdf.titulo_seccion("4. Evolucion del codigo (version 1 a version 2)")
    pdf.subtitulo("Version 1 - fecha de ejecucion (con bug)")
    pdf.set_font("Courier", "", 8)
    pdf.multi_cell(0, 5, pdf.limpiar(CODIGO_V1))
    pdf.ln(2)
    pdf.parrafo("Problema identificado: " + CODIGO_V1_PROBLEMA)

    pdf.subtitulo("Version 2 - fecha del pedido mas reciente (implementada)")
    pdf.set_font("Courier", "", 8)
    pdf.multi_cell(0, 5, pdf.limpiar(CODIGO_V2))
    pdf.ln(2)
    pdf.parrafo("Explicacion del cambio: " + CODIGO_V2_EXPLICACION)

    # ---------- Validación ----------
    pdf.titulo_seccion("5. Validacion con datos reales")
    pdf.parrafo(VALIDACION)

    # ---------- Visualizaciones ----------
    pdf.titulo_seccion("6. Visualizaciones construidas en Power BI")
    pdf.tabla(
        encabezados=["Visual", "Tipo", "Campos"],
        filas=VISUALIZACIONES,
        anchos=[50, 45, 95],
    )
    pdf.subtitulo("Medida DAX implementada")
    pdf.set_font("Courier", "", 9)
    pdf.multi_cell(0, 5, pdf.limpiar(MEDIDA_DAX))
    pdf.ln(4)

    # ---------- Errores ----------
    pdf.titulo_seccion("7. Bitacora de errores y soluciones")
    for titulo_err, sintoma, causa, solucion in ERRORES:
        pdf.subtitulo(titulo_err)
        pdf.parrafo(f"Sintoma: {sintoma}")
        pdf.parrafo(f"Causa: {causa}")
        pdf.parrafo(f"Solucion: {solucion}")
        pdf.ln(2)

    # ---------- Limitaciones ----------
    pdf.titulo_seccion("8. Limitaciones conocidas")
    pdf.tabla(
        encabezados=["Limitacion", "Detalle", "Mejora propuesta"],
        filas=LIMITACIONES,
        anchos=[55, 80, 55],
    )

    # ---------- Stack final ----------
    pdf.titulo_seccion("9. Stack tecnico final del proyecto completo")
    pdf.tabla(
        encabezados=["Etapa", "Herramienta", "Funcion"],
        filas=STACK_FINAL,
        anchos=[55, 55, 80],
    )

    return pdf


if __name__ == "__main__":
    documento = construir_pdf()
    documento.output("documentacion_flujo2.pdf")
    print("Archivo generado: documentacion_flujo2.pdf")
