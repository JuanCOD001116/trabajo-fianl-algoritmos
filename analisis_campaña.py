import pandas as pd
import matplotlib.pyplot as plt

def graficar_variable_en_campañas(df, campañas, variable):
    """Genera una gráfica comparando todas las campañas en todos los puntos (análisis espacial)."""
    
    # Determinar unidades según la variable
    if variable == "Caudal_Ls":
        unidades_var = "L/s"
    elif variable == "Precip_mm_d":
        unidades_var = "mm/d"
    else:
        unidades_var = "mg/L"  # Para DBO5, DQO, SST, Ntot, Ptot

    # Crear una sola figura para todas las campañas
    plt.figure(figsize=(12, 6))

    # Colores para diferenciar campañas
    colores = ['blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive']
    
    # Graficar cada campaña en la misma gráfica
    for idx, campaña in enumerate(campañas):
        # Filtrar datos de la campaña actual
        p = df[df["Campaña"] == campaña][["Campaña", variable, "TipoSistema", "Punto"]].sort_values("Punto")

        x = p["Punto"]
        y = p[variable]

        # Graficar línea para esta campaña
        color = colores[idx % len(colores)]
        plt.plot(x, y, marker="o", linestyle="-", label=f"{campaña}", color=color, linewidth=2)

    # Configurar títulos y etiquetas
    plt.title(f"Análisis Espacial: {variable} ({unidades_var}) - Todas las Campañas",
              fontsize=14)

    plt.xlabel("Punto", fontsize=12)
    plt.ylabel(f"{variable} ({unidades_var})", fontsize=12)
    plt.legend(fontsize=10, loc='best')
    plt.grid(True, linestyle="--", alpha=0.4)

    # Establecer límites del eje Y
    plt.ylim(0, 550)

    # Guardar figura
    plt.savefig(f"fig_{variable}_Espacial_TodasCampañas.png", dpi=300, bbox_inches='tight')
    plt.close()