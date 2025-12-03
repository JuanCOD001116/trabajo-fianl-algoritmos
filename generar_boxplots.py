import pandas as pd
import matplotlib.pyplot as plt

def boxplot_por_punto(df, variable, unidades):
    """Genera gráfica de caja y bigote para visualizar la distribución de la variable por punto."""


    # Asignar unidades específicas
    unidades_var = unidades.values[0]   # Unidad del LMP

    if variable == "Caudal_Ls":
        unidades_var = "L/s"
    elif variable == "Precip_mm_d":
        unidades_var = "mm/d"

    # Crear gráfica de caja y bigote
    plt.figure(figsize=(10, 5))

    df.boxplot(column=variable, by="Punto")


    # Configurar títulos y etiquetas
    plt.title(f"{variable} por Punto", fontsize=14)
    plt.suptitle("")   # Remover título automático

    plt.xlabel("Punto", fontsize=12)
    plt.ylabel(f"{variable} ({unidades_var})", fontsize=12)

    # Establecer límites y cuadrícula
    plt.ylim(0, 600)
    plt.grid(True, linestyle="--", alpha=0.4)

    plt.legend()

    # Guardar figura
    plt.savefig(f"boxplot_{variable}_por_punto.png", dpi=300)
    plt.close()
