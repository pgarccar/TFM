import pandas as pd
import glob
import os

satellite_name = "ASTROCAST-0401"

archivos_csv = glob.glob("TLE_2025*.csv")

datos_sat = []

for archivo in archivos_csv:
    try:
        df = pd.read_csv(archivo)
        df_filtrado = df[df["Satellite Name"] == satellite_name]
        if not df_filtrado.empty:
            print(f"{len(df_filtrado)} filas encontradas en {archivo}")
            datos_sat.append(df_filtrado)
    except Exception as e:
        print(f"Error al leer {archivo}: {e}")


if datos_sat:
    df_combinado = pd.concat(datos_sat, ignore_index=True)
    salida = f"TLE_{satellite_name.replace('-', '')}_todos.csv"
    df_combinado.to_csv(salida, index=False)
    print(f"Archivo combinado guardado como '{salida}' ({len(df_combinado)} registros totales)")
else:
    print(f"No se encontraron TLEs del satelite {satellite_name}")