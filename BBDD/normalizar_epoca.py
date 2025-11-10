import pandas as pd
from datetime import datetime, timedelta


archivo = "TLE_ASTROCAST0401_limpio.csv"

df = pd.read_csv(archivo)

print(f"Archivo '{archivo}' cargado con {len(df)} registros.\n")

fechas = []

for valor in df["Epoca"]:
    try:
        valor = str(valor).strip()
        anio = int(valor[:2])
        dia_fraccional = float(valor[2:])

        anio_completo = 2000 + anio if anio < 57 else 1900 + anio

        fecha_base = datetime(anio_completo,1,1) + timedelta(days=dia_fraccional-1)
        fechas.append(fecha_base)
    except Exception as e:
        fechas.append(None)
        print(f"Error al convertir '{valor}': {e}")

df["Fecha UTC"] = fechas

salida = "TLE_ASTROCAST0401_normalizado.csv"
df.to_csv(salida, index=False)

print(f"Archivo '{salida}' guardado correctamente con columna 'Fecha UTC'.\n")
print("Vista previa")
print(df[["Epoca", "Fecha UTC"]].head())
