import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

datos = {
    'horas_estudio': [5-14],
    'calificacion': [4, 15-23]
}

df = pd.DataFrame(datos)

X = df[['horas_estudio']] 
y = df['calificacion']    

modelo = LinearRegression()
modelo.fit(X, y)

horas_prueba = np.array([[5.5]])
prediccion = modelo.predict(horas_prueba)

y_pred = modelo.predict(X)
r2 = r2_score(y, y_pred)          
mse = mean_squared_error(y, y_pred) 
print("=== MODELO DE REGRESIÓN LINEAL (INTELIGENCIA ARTIFICIAL) ===")
print(f"Pendiente (Coeficiente - m): {modelo.coef_:.2f}")
print(f"Intercepto (b): {modelo.intercept_:.2f}")
print(f"Ecuación de la recta: Y = {modelo.coef_:.2f}*X + {modelo.intercept_:.2f}")
print(f"Predicción para 5.5 horas de estudio: {prediccion:.2f} pts")
print("-------------------------------------------------------")
print(f"Evaluación - Coeficiente R²: {r2:.4f} (Ajuste del {r2*100:.1f}%)")
print(f"Evaluación - MSE (Error cuadrático medio): {mse:.2f}")

plt.scatter(X, y, color='blue', label='Datos reales')
plt.plot(X, y_pred, color='red', linewidth=2, label='Recta de regresión')
plt.xlabel('Horas de Estudio')
plt.ylabel('Calificación')
plt.title('Regresión Lineal: Horas vs Calificación')
plt.legend()
plt.grid(True)
plt.show()