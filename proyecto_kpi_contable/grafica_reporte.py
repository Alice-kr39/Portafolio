
import pandas as pd 
import matplotlib.pyplot as plt


data = {
    'mes': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
    'ingresos': [50000, 62000, 58000, 71000, 65000, 80000],
    'gastos':   [30000, 35000, 40000, 38000, 42000, 45000],
    'utilidad': [20000, 27000, 18000, 33000, 23000, 35000]
}



"""
Eje X — siempre la categoría o tiempo (mes, día, año, producto...)
Eje Y — siempre los valores numéricos (ingresos, gastos, ventas...)

 los números son como los valores de la matriz, si aparece otro key de diccionario
 Sería otra fila de la matriz, otra línea en la gráfica.


"""

df = pd.DataFrame(data)

# Crear el gráfico
plt.plot(df['mes'], df['ingresos'], marker='o', color='blue', linestyle='-', linewidth=2, label='Ingresos')
plt.plot(df['mes'], df['gastos'], marker='o', color='red', linestyle='-', linewidth=2, label='Gastos')
plt.plot(df['mes'], df['utilidad'], marker='o', color='green', linestyle='-', linewidth=2, label='Utilidad')

# Personalizar
plt.title("Gráfico Lineal Básico", fontsize=14)
plt.xlabel("Eje X", fontsize=12)
plt.ylabel("Eje Y", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.savefig('grafica_kpi.png', dpi=150, bbox_inches='tight')

# Mostrar
plt.show()

