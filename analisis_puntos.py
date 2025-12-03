import pandas as pd
import matplotlib.pyplot as plt


def graficar_variable_en_puntos(df, puntos, variable, limite, c, unidades):
    """Genera una gráfica comparando todos los puntos a través de las campañas (análisis temporal)."""
    
    # Extraer LMP si existe
    tiene_limite = False
    if not limite.empty:
        lmp = float(limite.values[0])     # Valor numérico
        unidades = unidades.values[0]     # Unidades del LMP
        tiene_limite = True

    # Asignar unidades específicas
    if variable == "Caudal_Ls":
        unidades = "L/s"
    elif variable == "Precip_mm_d":
        unidades = "mm/d"
    else:
        unidades = "mg/L"

    # Crear una sola figura para todos los puntos
    plt.figure(figsize=(12, 6))

    # Colores para diferenciar puntos
    colores = ['blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    
    # Graficar cada punto en la misma gráfica
    for idx, punto in enumerate(puntos):
        # Filtrar datos del punto actual
        p = df[df["Punto"] == punto][["Campaña", variable, "TipoSistema", "Punto"]].sort_values("Campaña")

        x = p["Campaña"]
        y = p[variable]

        # Graficar línea para este punto
        color = colores[idx % len(colores)]
        plt.plot(x, y, marker="o", linestyle="-", label=f"{punto}", color=color, linewidth=2)

        # Marcar valores que superan el LMP para este punto
        if tiene_limite:
            fuera = p[p[variable] > lmp]
            if not fuera.empty:
                plt.scatter(
                    fuera["Campaña"], fuera[variable],
                    s=150, facecolors='none', edgecolors='red',
                    linewidth=2.5, zorder=5
                )

    # Agregar línea del LMP si existe
    if tiene_limite:
        plt.axhline(
            lmp, linestyle="--", linewidth=2, color="red",
            label=f"LMP máximo = {lmp} {unidades}"
        )
        # Añadir marcador para puntos fuera del límite en la leyenda
        plt.scatter([], [], s=150, facecolors='none', edgecolors='red', 
                   linewidth=2.5, label="Fuera del límite")

    # Configurar títulos y etiquetas
    tipo_sistema = df[df["Punto"].isin(puntos)]["TipoSistema"].iloc[0]
    plt.title(f"Análisis Temporal: {variable} ({unidades}) - Sistema {tipo_sistema}", fontsize=14)
    plt.xlabel("Campaña", fontsize=12)
    plt.ylabel(f"{variable} ({unidades})", fontsize=12)
    plt.ylim(0, 550)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend(fontsize=10, loc='best')

    # Guardar figura
    plt.savefig(f"fig_{variable}_Temporal_{tipo_sistema}.png", dpi=300, bbox_inches='tight')
    plt.close()
