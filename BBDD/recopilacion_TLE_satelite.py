import pandas as pd
import os

# Configuracion
dir = "/home/pablo/TFM/BBDD" # Carpeta con todos los ficheros .csv
satellite_name = "ASTROCAST-0401"

# Leer y filtrado
registros_filtrados = []
for arch in os.listdir(dir):
    if arch.endswith(".csv"):
        route = os.path.join(dir,arch)
        df = pd.read_csv(route)
        df_filtrado = df[df["Satellite Name"] == satellite_name].copy()
        if not df_filtrado.empty:
            df_filtrado["Fuente CSV"] = arch
            registros_filtrados.append(df_filtrado)


# Unificar y mostrar resultados
if registros_filtrados:
    df_total = pd.concat(registros_filtrados, ignore_index=True)
    fichero = f"{satellite_name}.csv"
    ruta_salida = os.path.join(dir,fichero)
    df_total.to_csv(ruta_salida, index=False)
    print(f"\nArchivo guardado como: {ruta_salida}")
else:
    print(f"No se encontraron registros para '{satellite_name}'.")


# Parseo de las columnas del .csv generado para nuestro satélite
