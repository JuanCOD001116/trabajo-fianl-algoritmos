# Importar librerías necesarias
import pandas as pd
import matplotlib.pyplot as plt
from analisis_puntos import graficar_variable_en_puntos 
from analisis_campaña import graficar_variable_en_campañas
from generar_boxplots import boxplot_por_punto
from funcion_auxiliar import obtener_limite_unidad

## Punto 1: Carga y preparación de datos

# Cargar datos desde Excel
df=pd.read_excel("VillaVerde_WaterSystemData.xlsx", sheet_name="Datos")
lmp=pd.read_excel("VillaVerde_WaterSystemData.xlsx", sheet_name="Limites")

# Seleccionar columnas relevantes
variables=['Punto','Caudal_Ls','Precip_mm_d','DBO5_mgL','DQO_mgL','SST_mgL','Ntot_mgL', 'Ptot_mgL', 'Campaña','TipoSistema']
df=df[variables]

# Variables numéricas para análisis estadístico
var_cols=['Caudal_Ls','Precip_mm_d','DBO5_mgL','DQO_mgL','SST_mgL','Ntot_mgL', 'Ptot_mgL']

## Punto 2: Estadísticas descriptivas por agrupación

# Calcular estadísticas por sistema y punto
variable_sistema = (
    df
    .groupby(["TipoSistema", "Punto"])[var_cols]
    .agg(["min", "max", "mean", "std"])
)

# Calcular estadísticas por punto y campaña
variable_campa = (
    df
    .groupby(["Punto", "Campaña"])[var_cols]
    .agg(["min", "max", "mean", "std"])
)

# Exportar resultados a Excel
writer = pd.ExcelWriter("Resultados_VillaVerde_Grupo01.xlsx")

variable_sistema.to_excel(writer, sheet_name="Variables Por Sistema_Punto")
variable_campa .to_excel(writer, sheet_name=" Variables por Campaña")

writer.close()


## Punto 3: Generación de gráficas

variables_clave = ['DBO5_mgL','DQO_mgL','SST_mgL']

# Graficar variables para puntos de agua potable (solo Caudal y Precipitación)
puntos_potable = df[df["TipoSistema"] == "Potable"]["Punto"].unique()
variables_potable = ['Caudal_Ls', 'Precip_mm_d']

for variable in variables_potable:
    limite, unidad = obtener_limite_unidad(lmp, variable, "Potable")
    graficar_variable_en_puntos(df, puntos_potable, variable, limite, "blue", unidad)


# Graficar variables para puntos de río
puntos_rio = df[df["TipoSistema"] == "Rio"]["Punto"].unique()

for variable in variables_clave:
    limite, unidad = obtener_limite_unidad(lmp, variable, "Rio")
    graficar_variable_en_puntos(df, puntos_rio, variable, limite, "blue", unidad)

# Graficar variables para puntos de agua residual
puntos_residuales = df[df["TipoSistema"] == "Residual"]["Punto"].unique()

for variable in variables_clave:
    limite, unidad = obtener_limite_unidad(lmp, variable, "Residual")
    graficar_variable_en_puntos(df, puntos_residuales, variable, limite, "green", unidad)

# Graficar variables por campaña
campañas = df.Campaña.unique().tolist()

for var in variables_clave:
    graficar_variable_en_campañas(df, campañas, var)
print("Gráficas de líneas generadas.")

# Generar gráficas de caja y bigote
for var in variables_clave:
    limite, unidad = obtener_limite_unidad(lmp, var, "Residual")
    boxplot_por_punto(df, var, limite, unidad)
print("Graficas de caja y bigote generadas.")


## Punto 4: Análisis de cumplimiento de LMP

# Convertir el dataframe de formato ancho → largo
variables = [col for col in df.columns if col not in ["Campaña", "Punto", "TipoSistema"]]

# se convierte en fila las columnas con su nombre en "Variable" y su valor en "Valor"
df_long = df.melt(
    id_vars=["Campaña", "Punto", "TipoSistema"],  # Columnas que se mantienen fijas
    value_vars=variables,                          # Columnas a transformar en filas
    var_name="Variable",                           # Nombre de la nueva columna con nombres de variables
    value_name="Valor"                             # Nombre de la nueva columna con los valores
)

# Unir con la tabla de límites máximos permisibles (LMP)
df_merged = df_long.merge(
    lmp[["Variable", "TipoSistema", "LMP_max"]],
    on=["Variable", "TipoSistema"],
    how="left"
)

# Identificar superaciones del LMP
df_merged["Supera_LMP"] = df_merged["Valor"] > df_merged["LMP_max"]

# Calcular porcentaje de exceso respecto al límite
# Formula: ((Valor - LMP) / LMP) * 100
# Si el valor es menor al LMP, el porcentaje será negativo (cumplimiento)
# Si el valor es mayor al LMP, el porcentaje será positivo (exceso)
df_merged["Porcentaje_Exceso"] = ((df_merged["Valor"] - df_merged["LMP_max"]) / df_merged["LMP_max"] * 100).round(2)

# Exportar resultados a Excel
with pd.ExcelWriter("analisis_calidad_agua.xlsx") as writer:
    df_merged.to_excel(writer, sheet_name="Analisis_Completo", index=False)

print("Archivo generado: analisis_calidad_agua.xlsx")