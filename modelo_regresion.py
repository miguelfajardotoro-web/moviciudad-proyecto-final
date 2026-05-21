import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import numpy as np

df = pd.read_csv("moviciudad_operaciones_limpio.csv", encoding='latin-1')

# Variables predictoras
X = df[["retraso_min", "pasajeros_reportados"]]
# Variable objetivo
y = df["tiempo_viaje_min"]

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
# Crear modelo
modelo = LinearRegression()
# Entrenar modelo
modelo.fit(X_train, y_train)
# Predicciones
y_pred = modelo.predict(X_test)
# Métricas
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Resultados
print("Resultados del modelo de regresión lineal:")
print(f"MAE: {mae:.2f}")

print(f"MSE: {mse:.2f}")

print(f"RMSE: {rmse:.2f}")

print(f"R2: {r2:.2f}")