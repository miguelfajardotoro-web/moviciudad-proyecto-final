#Proyecto Final MoviCiudad SPA
#Limpiexa de datos y análisis exploratorio
#Autor: Miguel Fajardo Toro

#Importamos las librerías necesarias
import pandas as pd
import numpy as np
#Librerías para visualización de datos y analisis exploratorio
import matplotlib.pyplot as plt
import seaborn as sns   
#1. Cargar archivo CSV y explorar datos
#Cargamos el archivo CSV con los datos de MoviCiudad en un DataFrame de Pandas
df = pd.read_csv("moviciudad_operaciones_bruto_SET_A.csv", encoding='latin-1')

print("Datos cargados correctamente. Las primeras filas del DataFrame son:")
print(df.head())

print("\nInformación general del DataFrame:")
print(df.info())

#2. Limpieza de datos categoricos   
#Corregir acentos dañados
df["tipo_dia"] = df["tipo_dia"].replace({"HÃ¡bil": "Hábil","SÃ¡bado": "Sábado"})
#Normalizar columna turno
df["turno"] = df["turno"].replace({"MÃ¡nana": "Mañana","M": "Mañana","TARDE": "Tarde","NOCHE": "Noche"})
    
#3. Limpiar rutas convertir a mayusculas
df["ruta"] = df["ruta"].str.upper()
#corregir errores comunes
df["ruta"] = df["ruta"].replace({
    "R 03": "R-03", "R-1": "R-01", "R-07 ": "R-07",
    "R-02": "R-02", "R-03": "R-03", "R-04": "R-04", "R-05": "R-05",
    "R-06": "R-06", "R-07": "R-07","R-01": "R-01", "R-02": "R-02"})

#4. Limpieza fecha y hora-Convertir la columna "fecha" a formato datetime    
df["fecha_registro"] = pd.to_datetime(df["fecha_registro"], errors='coerce')
#convertir la columna "hora" a formato datetime
df["hora_salida"] = pd.to_datetime(df["hora_salida"], format="%H:%M:%S", errors='coerce').dt.time

#5. Limpieza de variables numéricas-Eliminar texto min
df["retraso_min"] = df["retraso_min"].astype(str).str.replace(" min", "", regex=False)
#Reemplazar coma decimal por punto
df["tiempo_viaje_min"] = df["tiempo_viaje_min"].astype(str).str.replace(",", ".", regex=False)
# Convertir columnas numéricas
columnas_numericas = ["tiempo_viaje_min", "retraso_min", "pasajeros_reportados"]
for col in columnas_numericas:
   df[col] = pd.to_numeric(df[col], errors='coerce')

#6.DETECCIÓN DE VALORES FALTANTES
print("\nValores nulos por columna:")
print(df.isnull().sum())

#7. TRATAMIENTO DE VALORES FALTANTES
#reemplazar valores nulos en columnas numéricas por la media
df["tiempo_viaje_min"] = df["tiempo_viaje_min"].fillna(df["tiempo_viaje_min"].median())
#reemplazar valores nulos en columnas numéricas por la media
df["retraso_min"] = df["retraso_min"].fillna(df["retraso_min"].median())
#reemplazar valores nulos en columnas numéricas por la media
df["pasajeros_reportados"] = df["pasajeros_reportados"].fillna(df["pasajeros_reportados"].median())

#Completar turnos vacios con el turno más frecuente
df["turno"] = df["turno"].fillna("Desconocido")

#8.LIMINAR DUPLICADOS
duplicados = df.duplicated().sum()
print(f"\nNúmero de filas duplicadas: {duplicados}")
df = df.drop_duplicates()

#9. DETECCIÓN DE OUTLIERS
#Valores externos en tiempo de viaje
outliers_tiempo = df[df["tiempo_viaje_min"] > 120]
print(f"\nNúmero de outliers en tiempo de viaje: {len(outliers_tiempo)}")

#10 estructura de datos final 
# Crear nuevas columnas útiles
order_es = {"Monday": "Lunes","Tuesday": "Martes","Wednesday": "Miércoles","Thursday": "Jueves",
            "Friday": "Viernes","Saturday": "Sábado","Sunday": "Domingo"}
df["dia_semana"] = df["fecha_registro"].dt.day_name().map(order_es)

order_dia = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

df["dia_semana"] = pd.Categorical(df["dia_semana"], categories=order_dia, ordered=True)

#ordenar columnas
df = df[["id_formulario","fecha_registro", "dia_semana", "hora_salida", "ruta", "tipo_dia",
          "tiempo_viaje_min", "retraso_min", "pasajeros_reportados"]] 

#11. exportar el DataFrame limpio a un nuevo archivo Excel
df.to_excel("moviciudad_operaciones_limpio.xlsx", index=False)
#exportar el DataFrame limpio a un nuevo archivo CSV
df.to_csv("moviciudad_operaciones_limpio.csv", index=False, encoding='latin-1')

print("\nLimpieza de datos completada.")
print("El DataFrame limpio se ha exportado a:")
print("moviciudad_operaciones_limpio.xlsx")
print("moviciudad_operaciones_limpio.csv")
#12. Estadisticas descriptivas
print("\nEstadísticas descriptivas del DataFrame limpio:")
estadisticas = df[
   ["tiempo_viaje_min", "retraso_min", "pasajeros_reportados"]].describe()

print(estadisticas)

#guardar estadisticas descriptivas en un archivo de texto
estadisticas.to_excel("estadisticas_descriptivas.xlsx", index=True)

#13. detección de outliers con boxplot metodo IQR
q1 = df["tiempo_viaje_min"].quantile(.25)
q3 = df["tiempo_viaje_min"].quantile(.75)
iqr = q3 - q1
limite_inferior = q1 - (1.5 * iqr)
limite_superior = q3 + (1.5 * iqr)
outliers_iqr = df[(df["tiempo_viaje_min"] < limite_inferior) | (df["tiempo_viaje_min"] > limite_superior)]

print(outliers_iqr[["id_formulario","ruta","tiempo_viaje_min"]])

print(f"\nNúmero de outliers detectados con el método IQR: {len(outliers_iqr)}")

#14. Matriz de correlación

correlacion = df[["tiempo_viaje_min", "retraso_min", "pasajeros_reportados"]].corr()

print("\nMatriz de correlación:")
print(correlacion)
correlacion.to_excel("matriz_correlacion.xlsx", index=True)
#15 Mapa de calor de la matriz de correlación Heartmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlacion, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Mapa de calor de la matriz de correlación")
plt.savefig("mapa_calor_correlacion.png")
plt.show()