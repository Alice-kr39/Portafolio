

def verificar_kpis(df, umbral_margen=35, umbral_utilidad=20000):
    print("\n📊 REPORTE DE KPIs\n")
    
    for _, row in df.iterrows():
        print(f"📅 {row['mes']}")
        print(f"   Ingresos:  ${row['ingresos']:,}")
        print(f"   Gastos:    ${row['gastos']:,}")
        print(f"   Utilidad:  ${row['utilidad']:,}")
        print(f"   Margen:    {row['margen_%']}%")
        
        # Alerta margen bajo
        if row['margen_%'] < umbral_margen:
            print(f"   ⚠️  Alerta: margen por debajo del {umbral_margen}%")
        
        # Alerta utilidad baja
        if row['utilidad'] < umbral_utilidad:
            print(f"   ⚠️  Alerta: utilidad por debajo de ${umbral_utilidad:,}")
        
        print()
        