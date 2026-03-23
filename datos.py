#analisis contabilidad-finanzas

import pandas as pd

# Dataset ficticio de ingresos y gastos mensuales
data = {
    'mes': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
    'ingresos': [50000, 62000, 58000, 71000, 65000, 80000],
    'gastos':   [30000, 35000, 40000, 38000, 42000, 45000]
}

df = pd.DataFrame(data)

# Calcular utilidad
df['utilidad'] = df['ingresos'] - df['gastos']

# Calcular margen de utilidad %
df['margen_%'] = ((df['utilidad'] / df['ingresos']) * 100).round(2)

print(df)

#EL DATA SET ES CREADO LIMPIO 
