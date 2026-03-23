
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datos import df

UMBRAL_MARGEN = 35
UMBRAL_UTILIDAD = 20000

def generar_pdf():
    doc = SimpleDocTemplate("reporte_kpi.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    elementos = []

    # Título
    titulo = Paragraph("Reporte de KPIs Contables", styles['Title'])
    elementos.append(titulo)
    elementos.append(Spacer(1, 20))

    # Tabla
    data = [['Mes', 'Ingresos', 'Gastos', 'Utilidad', 'Margen %']]
    
    for _, row in df.iterrows():
        data.append([
            row['mes'],
            f"${row['ingresos']:,}",
            f"${row['gastos']:,}",
            f"${row['utilidad']:,}",
            f"{row['margen_%']}%"
        ])

    tabla = Table(data)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
        ('GRID',       (0,0), (-1,-1), 1, colors.black),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey]),
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 30))


    from reportlab.platypus import Image

    # Gráfica
    elementos.append(Spacer(1, 20))
    grafica = Image('grafica_kpi.png', width=450, height=300)
    elementos.append(grafica)

    

    # Alertas
    alertas_titulo = Paragraph("⚠️ Alertas", styles['Heading2'])
    elementos.append(alertas_titulo)
    elementos.append(Spacer(1, 10))

    hay_alertas = False
    for _, row in df.iterrows():
        if row['margen_%'] < UMBRAL_MARGEN:
            alerta = Paragraph(f"• {row['mes']}: margen {row['margen_%']}% por debajo del {UMBRAL_MARGEN}%", styles['Normal'])
            elementos.append(alerta)
            hay_alertas = True
        if row['utilidad'] < UMBRAL_UTILIDAD:
            alerta = Paragraph(f"• {row['mes']}: utilidad ${row['utilidad']:,} por debajo de ${UMBRAL_UTILIDAD:,}", styles['Normal'])
            elementos.append(alerta)
            hay_alertas = True

    if not hay_alertas:
        elementos.append(Paragraph("Sin alertas este periodo.", styles['Normal']))

    doc.build(elementos)
    print("✅ reporte_kpi.pdf generado correctamente")

generar_pdf()

