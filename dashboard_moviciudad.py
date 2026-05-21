import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
#importar directorio para guardar graficos
os.makedirs("graficos", exist_ok=True)

# Cargar el DataFrame limpio

df = pd.read_csv("moviciudad_operaciones_limpio.csv", encoding='latin-1')
"""
# Gráfico 1: Distribución de tiempos de viaje por ruta
plt.figure(figsize=(10, 6))

#Contar la cantidad de operaciones por ruta

sns.histplot(df["tiempo_viaje_min"], bins=30, kde=True)
plt.title("Distribución del tiempo de viaje")
plt.xlabel("Tiempo de viaje (minutos)")
plt.ylabel("Frecuencia")    
# Guardar el gráfico en la carpeta "graficos"
plt.savefig("graficos/distribucion_tiempo_viaje.png")
# Mostrar el gráfico
plt.show()

#Grafico 2: Promedio de tiempo por ruta
plt.figure(figsize=(10, 6))
promedio_ruta = df.groupby("ruta")["tiempo_viaje_min"].mean().sort_values(ascending=False)

# Crear un gráfico de barras para el promedio de tiempo por ruta
sns.barplot(x=promedio_ruta.index, y=promedio_ruta.values, palette="viridis")
plt.title("Promedio de tiempo de viaje por ruta")
plt.xlabel("Ruta")
plt.ylabel("Promedio de tiempo de viaje (minutos)")
# Guardar el gráfico en la carpeta "graficos"
plt.savefig("graficos/promedio_tiempo_viaje_ruta.png", dpi=300)
plt.show()  # ver el gráfico y cerrar la figura para liberar memoria
"""
#Grafico 3: Gráfico 3: Retrasos por tipo de día
plt.figure(figsize=(8, 6))
sns.boxplot(x="tipo_dia", y="retraso_min", data=df)
plt.title("Retrasos por tipo de día")
plt.xlabel("Tipo de día")
plt.ylabel("Retraso (minutos)")
# Guardar el gráfico en la carpeta "graficos"
plt.savefig("graficos/retrasos_tipo_dia.png")   
plt.show()  # Cerrar la figura actual para liberar memoria

""""
#Gráfico 4: Correlación entre variables
plt.figure(figsize=(8, 6))
correlacion = df[
    ["tiempo_viaje_min", "retraso_min", "pasajeros_reportados"]
    ].corr()

sns.heatmap(correlacion, annot=True, cmap="coolwarm", vmin=-1, vmax=1)

plt.title("Mapa de calor de la matriz de correlación")
# Guardar el gráfico en la carpeta "graficos"
plt.savefig("graficos/correlacion_tiempo_retraso.png")
plt.show()  # Cerrar la figura actual para liberar memoria


#Dashboard interactivo con Plotly
fig = px.scatter(df, x="tiempo_viaje_min", y="retraso_min", color="tipo_dia",
                 title="Relación entre tiempo de viaje y retraso por tipo de día",
                 labels={"tiempo_viaje_min": "Tiempo de viaje (minutos)", "retraso_min": "Retraso (minutos)"})  
fig.show()

#Exportar dataset limpio a Excel
df.to_excel("moviciudad_procesado.xlsx", index=False)

print("Archivo Excel exportado correctamente")

"""
