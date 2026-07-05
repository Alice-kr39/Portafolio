

# generar_pdf.py
# Lee el contenido estructurado de contenido_flujo1.py y genera un archivo .pdf

from fpdf import FPDF
from contenido_flujo1 import (
    TITULO, INTRO, OBJETIVO, ARQUITECTURA, CREDENCIALES,
    ESTRUCTURA_DATOS, ERRORES, LIMITACIONES, RESULTADO, STACK_FINAL
)


class DocumentoPDF(FPDF):
    """
    Clase propia que hereda de FPDF.
    Aquí definimos cómo se ven los encabezados y el cuerpo del texto,
    para no repetir el mismo formato una y otra vez.
    """

    def limpiar(self, texto):
        """
        Reemplaza caracteres especiales (flechas, guiones largos, acentos
        problemáticos) por equivalentes simples compatibles con la fuente
        básica del PDF (Helvetica/Courier, codificación latin-1).
        """
        reemplazos = {
            "\u2192": "->",   # →
            "\u2190": "<-",   # ←
            "\u2014": "-",    # —  (guion largo)
            "\u2013": "-",    # –  (guion medio)
            "\u2018": "'", "\u2019": "'",   # comillas tipográficas simples
            "\u201c": '"', "\u201d": '"',   # comillas tipográficas dobles
            "\u2026": "...",  # puntos suspensivos
        }
        for original, simple in reemplazos.items():
            texto = texto.replace(original, simple)
        return texto

    def titulo_seccion(self, texto):
        """Imprime un título de sección con estilo (negrita, tamaño grande)."""
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(20, 20, 20)
        self.multi_cell(0, 8, self.limpiar(texto))
        self.ln(2)

    def subtitulo(self, texto):
        """Imprime un subtítulo (un poco más pequeño que el título de sección)."""
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 7, self.limpiar(texto))
        self.ln(1)

    def parrafo(self, texto):
        """Imprime texto normal de párrafo."""
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, self.limpiar(texto))
        self.ln(2)

    def etiqueta_valor(self, etiqueta, valor):
        """Imprime una línea tipo 'Etiqueta: valor' con la etiqueta en negrita."""
        self.set_font("Helvetica", "B", 10)
        self.write(6, self.limpiar(f"{etiqueta}: "))
        self.set_font("Helvetica", "", 10)
        self.write(6, self.limpiar(valor))
        self.ln(8)

    def tabla(self, encabezados, filas, anchos):
        """
        Dibuja una tabla simple.
        encabezados: lista de textos para la primera fila
        filas: lista de tuplas con los datos
        anchos: lista de anchos de columna en mm (debe sumar ~190 para hoja carta)
        """
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(230, 230, 230)
        for encabezado, ancho in zip(encabezados, anchos):
            self.cell(ancho, 7, self.limpiar(encabezado), border=1, fill=True)
        self.ln()

        self.set_font("Helvetica", "", 9)
        for fila in filas:
            for valor, ancho in zip(fila, anchos):
                # Convertimos a texto por si llega un número
                self.cell(ancho, 7, self.limpiar(str(valor)), border=1)
            self.ln()
        self.ln(4)


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
    pdf.titulo_seccion("1. Objetivo del proyecto")
    pdf.parrafo(OBJETIVO)

    # ---------- Arquitectura ----------
    pdf.titulo_seccion("2. Arquitectura del flujo")
    pdf.set_font("Courier", "", 9)
    pdf.multi_cell(0, 5, pdf.limpiar(ARQUITECTURA))
    pdf.ln(4)

    # ---------- Credenciales ----------
    pdf.titulo_seccion("3. Configuración de credenciales")
    for cred in CREDENCIALES:
        pdf.subtitulo(cred["nombre"])
        pdf.tabla(
            encabezados=["Campo", "Valor"],
            filas=cred["filas"],
            anchos=[60, 130],
        )

    # ---------- Estructura de datos ----------
    pdf.titulo_seccion("4. Estructura de datos de origen (Google Sheets)")
    pdf.tabla(
        encabezados=["Columna", "Tipo", "Ejemplo"],
        filas=ESTRUCTURA_DATOS,
        anchos=[60, 50, 80],
    )

    # ---------- Errores ----------
    pdf.titulo_seccion("5. Bitácora de errores y soluciones")
    for titulo_err, sintoma, causa, solucion in ERRORES:
        pdf.subtitulo(titulo_err)
        pdf.parrafo(f"Síntoma: {sintoma}")
        pdf.parrafo(f"Causa: {causa}")
        pdf.parrafo(f"Solución: {solucion}")
        pdf.ln(2)

    # ---------- Limitaciones ----------
    pdf.titulo_seccion("6. Limitaciones conocidas")
    pdf.tabla(
        encabezados=["Limitación", "Impacto", "Mitigación", "Solución propuesta"],
        filas=LIMITACIONES,
        anchos=[55, 30, 50, 55],
    )

    # ---------- Resultado ----------
    pdf.titulo_seccion("7. Resultado verificado")
    pdf.parrafo(RESULTADO)

    # ---------- Stack final ----------
    pdf.titulo_seccion("8. Stack técnico final")
    pdf.tabla(
        encabezados=["Componente", "Herramienta", "Plan usado"],
        filas=STACK_FINAL,
        anchos=[70, 60, 60],
    )

    return pdf


if __name__ == "__main__":
    documento = construir_pdf()
    documento.output("documentacion_flujo1.pdf")
    print("Archivo generado: documentacion_flujo1.pdf")