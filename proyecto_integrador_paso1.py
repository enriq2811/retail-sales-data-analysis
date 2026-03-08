import pandas as pd
import os
import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import ttest_ind
plt.rcParams["figure.figsize"] = (10, 6)


# Carpeta donde está el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# crear carpeta de gráficos
plots_dir = os.path.join(script_dir, "plots")
os.makedirs(plots_dir, exist_ok=True)

# Ruta del archivo CSV
file_path = os.path.join(script_dir, "Ventas_Tienda.csv")

print("Ruta del archivo:", file_path)

# Leer CSV
df = pd.read_csv(file_path, encoding="utf-8")

print("\nPrimeras 5 filas:")
print(df.head())

print("\nDimensiones del dataset:")
print(df.shape)

print("\nColumnas:")
print(df.columns.tolist())

print("\nTipos de datos:")
print(df.dtypes)

print("\nValores nulos por columna:")
print(df.isnull().sum())

print("\nInformación general:")
df.info()

# Estadísticos descriptivos de variables numéricas
print("\nEstadísticos descriptivos:")
print(df.describe())

# Estadísticos descriptivos incluyendo variable booleana/categórica
print("\nEstadísticos descriptivos ampliados:")
print(df.describe(include="all"))

# Ventas totales del año
total_ventas_anuales = df["Total_Sales"].sum()

print("\nVentas totales del año:")
print(total_ventas_anuales)

# Promedio de ventas semanales
promedio_ventas = df["Total_Sales"].mean()

print("\nPromedio de ventas semanales:")
print(promedio_ventas)

# Desviación estándar de ventas
desviacion_ventas = df["Total_Sales"].std()

print("\nDesviación estándar de ventas:")
print(desviacion_ventas)

# Diccionario para nombres de tiendas
store_names = {
    1: "Munich",
    2: "Dubai",
    3: "London",
    4: "New York"
}

# Crear columna con nombre de tienda
df["Store_Name"] = df["Store"].map(store_names)

# Promedio de ventas por tienda
ventas_por_tienda = df.groupby("Store_Name")["Total_Sales"].mean()

print("\nPromedio de ventas por tienda:")
print(ventas_por_tienda)

# Separar ventas por tienda
ventas_munich = df[df["Store_Name"] == "Munich"]["Total_Sales"]
ventas_dubai = df[df["Store_Name"] == "Dubai"]["Total_Sales"]
ventas_london = df[df["Store_Name"] == "London"]["Total_Sales"]
ventas_newyork = df[df["Store_Name"] == "New York"]["Total_Sales"]

# ANOVA de una vía
f_stat, p_value = stats.f_oneway(
    ventas_munich,
    ventas_dubai,
    ventas_london,
    ventas_newyork
)

print("\nANOVA entre tiendas")
print("F-statistic:", f_stat)
print("p-value:", p_value)

# Renombrar columnas de departamentos
df = df.rename(columns={
    "MarkDown1": "Automotive",
    "MarkDown2": "Home",
    "MarkDown3": "Women_Clothing",
    "MarkDown4": "Men_Clothing",
    "MarkDown5": "Electronics"
})

print("\nColumnas después de renombrar:")
print(df.columns)

# Promedio de ventas por departamento
promedios_departamentos = df[
    ["Automotive","Home","Women_Clothing","Men_Clothing","Electronics"]
].mean()

print("\nPromedio de ventas por departamento:")
print(promedios_departamentos)

# ANOVA entre departamentos
f_stat_dep, p_value_dep = stats.f_oneway(
    df["Automotive"],
    df["Home"],
    df["Women_Clothing"],
    df["Men_Clothing"],
    df["Electronics"]
)

print("\nANOVA entre departamentos")
print("F-statistic:", f_stat_dep)
print("p-value:", p_value_dep)

# Promedio de ventas por tienda y departamento
ventas_tienda_departamento = df.groupby("Store_Name")[[
    "Automotive",
    "Home",
    "Women_Clothing",
    "Men_Clothing",
    "Electronics"
]].mean()

print("\nPromedio de ventas por tienda y departamento:")
print(ventas_tienda_departamento)

# Separar ventas en semanas festivas y no festivas
ventas_festivas = df[df["IsHoliday"] == True]["Total_Sales"]
ventas_no_festivas = df[df["IsHoliday"] == False]["Total_Sales"]

print("\nPromedio ventas semanas festivas:", ventas_festivas.mean())
print("Promedio ventas semanas no festivas:", ventas_no_festivas.mean())

t_stat, p_value = ttest_ind(ventas_festivas, ventas_no_festivas)

print("\nT-test semanas festivas vs no festivas")
print("t-statistic:", t_stat)
print("p-value:", p_value)

# Seleccionar variables relevantes
variables_correlacion = df[[
    "Total_Sales",
    "Temperature",
    "CPI",
    "Unemployment"
]]

# Calcular matriz de correlación
correlation_matrix = variables_correlacion.corr()

print("\nMatriz de correlación:")
print(correlation_matrix)

# Variables independientes (predictores)
X = df[["Temperature", "CPI", "Unemployment"]]

# Variable dependiente
y = df["Total_Sales"]

# Agregar constante para el modelo
X = sm.add_constant(X)

# Ajustar modelo de regresión
model = sm.OLS(y, X).fit()

# Mostrar resultados
print("\nResultados de la regresión:")
print(model.summary())

# Gráfico 1: Ventas promedio por tienda
ventas_por_tienda = df.groupby("Store_Name")["Total_Sales"].mean()

plt.figure(figsize=(10, 6))
plt.bar(ventas_por_tienda.index, ventas_por_tienda.values)
plt.title("Promedio de Ventas por Tienda")
plt.xlabel("Tienda")
plt.ylabel("Ventas Promedio")
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "ventas_por_tienda.png"), dpi=300, bbox_inches="tight")
plt.show()

# Gráfico 2: Ventas promedio por departamento
promedios_departamentos = df[
    ["Automotive", "Home", "Women_Clothing", "Men_Clothing", "Electronics"]
].mean()

plt.figure(figsize=(10, 6))
plt.bar(promedios_departamentos.index, promedios_departamentos.values)
plt.title("Promedio de Ventas por Departamento")
plt.xlabel("Departamento")
plt.ylabel("Ventas Promedio")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "ventas_por_departamento.png"), dpi=300, bbox_inches="tight")
plt.show()

# Gráfico 3: Ventas promedio en semanas festivas vs no festivas
ventas_por_festivo = df.groupby("IsHoliday")["Total_Sales"].mean()

labels = ["No festiva", "Festiva"]

plt.figure(figsize=(8, 6))
plt.bar(labels, ventas_por_festivo.values)
plt.title("Ventas Promedio: Semanas Festivas vs No Festivas")
plt.xlabel("Tipo de semana")
plt.ylabel("Ventas Promedio")
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "ventas_festivas_vs_no_festivas.png"), dpi=300, bbox_inches="tight")
plt.show()