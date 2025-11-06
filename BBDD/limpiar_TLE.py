import pandas as pd

archivo = "TLE_clasificado.csv"

df = pd.read_csv(archivo)

print(f"Archivo '{archivo}' cargado con {len(df)}' registros. \n")


df_limpio = df.copy()

#Pasamos a formato numericos las columnas necesarias
columnas_numericas = [
    "Inclinacion (°)",
    "RAAN (°)",
    "Excentricidad",
    "Arg Perigeo (°)",
    "Anomalia Media (°)",
    "Movimiento Medio (rev/día)",
]

#Pasamos las columnas a tipo float
for col in columnas_numericas:
    df_limpio[col] = pd.to_numeric(df_limpio[col], errors="coerce")

#Mostramos los resultados y guardamos
print("Vista previa de los valores convertidos:")
print(df_limpio[columnas_numericas].head())
df_limpio.to_csv("TLE_limpio.csv", index=False)
print("\n Archivo 'TLE_limio.csv' guardado correctamente")
