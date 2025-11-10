import pandas as pd

archivo = "TLE_ASTROCAST0401_clasificado.csv"
df = pd.read_csv(archivo)

print(f"Archivo '{archivo}' cargado con {len(df)} registros.\n")

df_limpio = df.copy()

columnas_numericas = [
    "Inclinacion (°)",
    "RAAN (°)",
    "Excentricidad",
    "Arg Perigeo (°)",
    "Anomalia Media (°)",
    "Movimiento Medio (rev/día)",
    "Revolucion Epoca"
]

for col in columnas_numericas:
    df_limpio[col] = pd.to_numeric(df_limpio[col], errors="coerce")

print("Vista previa de los valores convertidos:")
print(df_limpio[columnas_numericas].head())
df_limpio.to_csv("TLE_ASTROCAST0401_limpio.csv", index=False)
print("\n Archivo 'TLE_ASTROCAST0401_limpio.csv' guardado correctamente")