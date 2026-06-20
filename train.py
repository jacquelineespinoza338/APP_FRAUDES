import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

# Leer datos
df = pd.read_json("transacciones.json")

# Convertir países a números
paises = {
    "México":0,
    "Estados Unidos":1,
    "Canadá":2,
    "España":3,
    "Rusia":4,
    "Nigeria":5
}

df["pais"] = df["pais"].map(paises)

X = df[["monto","pais","hora","transacciones_dia"]]

y = df["fraude"]

modelo = RandomForestClassifier(n_estimators=100, random_state=42)

modelo.fit(X,y)

joblib.dump(modelo,"modelo.pkl")

print("Modelo entrenado correctamente")
