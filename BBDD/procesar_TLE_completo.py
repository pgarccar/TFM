import pandas as pd
import glob
import os
from datetime import datetime, timedelta

def combinar_tle(sat_name="ASTROCAST-0401"):
    
    archivos_csv = glob.glob("TLE_2025_*.csv")
    datos_sat = []

    for archivo in archivos_csv:
        try:
            df = pd.read_csv(archivo)
            df_filtrado = df[df["Satellite Name"] == sat_name]
            if not df_filtrado.empty:
                print(f"{len(df_filtrado)} filas encontradas en {archivo}")
                datos_sat.append(df_filtrado)
        except Exception as e:
            print(f"Error al leer {archivo}: {e}")


    if not datos_sat:
        print(f"No se encontraron TLEs del satelite {sat_name}.")
        return None
    
    df_combinado = pd.concat(datos_sat, ignore_index=True)
    salida = f"TLE_{sat_name.replace('-','')}_todos.csv"
    df_combinado.to_csv(salida, index=False)
    print(f"Archivo combinado guardado como '{salida}' ({len(df_combinado)} registros).\n")
    return salida


def clasificar_tle(archivo_entrada):
    df = pd.read_csv(archivo_entrada)
    resultados = []

    for _, fila in df.iterrows():
        linea1,linea2 = fila["TLE Line 1"], fila["TLE Line 2"]

        #Extraemos cada uno de los elementos del TLE
        #==========LINEA 1===========
        num_linea_1 = linea1[0:1].strip()
        norad_id_1 = linea1[2:7].strip()
        clasificacion = linea1[7:8].strip()
        designacion_int = linea1[9:17].strip()
        epoca = linea1[18:32].strip()
        primera_derivada = linea1[33:43].strip()
        segunda_derivada = linea1[44:52].strip()
        bstar = linea1[53:61].strip()
        tipo_ephemerides = linea1[62:63].strip()
        checksum_1 = linea1[-1].strip()

        #==========LINEA 2===========
        num_linea_2 = linea2[0:1].strip()
        norad_id_2 = linea2[2:7].strip()
        inclinacion = linea2[8:16].strip()
        raan = linea2[17:25].strip()
        excentricidad = linea2[26:33].strip()
        arg_perigeo = linea2[34:42].strip()
        anomalia_media = linea2[43:51].strip()
        movimiento_medio = linea2[52:63].strip()
        revolucion_epoca = linea2[63:68].strip()
        checksum_2 = linea2[-1].strip()

        #Guardamos los resultados en el dataset
        resultados.append({
            "Satellite Name": fila["Satellite Name"],
            # --- Línea 1 ---
            "Num Linea 1": num_linea_1,
            "NORAD_ID_1": norad_id_1,
            "Clasificacion": clasificacion,
            "Designacion Internacional": designacion_int,
            "Epoca": epoca,
            "1ra Derivada": primera_derivada,
            "2da Derivada": segunda_derivada,
            "BSTAR": bstar,
            "Tipo Elemento": tipo_ephemerides,
            "Checksum 1": checksum_1,
            # --- Línea 2 ---
            "Num Linea 2": num_linea_2,
            "NORAD_ID_2": norad_id_2,
            "Inclinacion (°)": inclinacion,
            "RAAN (°)": raan,
            "Excentricidad": f"0.{excentricidad}",
            "Arg Perigeo (°)": arg_perigeo,
            "Anomalia Media (°)": anomalia_media,
            "Movimiento Medio (rev/día)": movimiento_medio,
            "Revolucion Epoca": revolucion_epoca,
            "Checksum 2": checksum_2
        })

    df_resultado = pd.DataFrame(resultados)
    salida = archivo_entrada.replace("_todos.csv", "_clasificado.csv")
    df_resultado.to_csv(salida, index=False)
    print(f"Archivo '{salida}' generado correctamente con {len(df_resultado)} ")
    return salida


def limpiar_tle(archivo_entrada):
    df = pd.read_csv(archivo_entrada)

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
        df[col] = pd.to_numeric(df[col], errors="coerce")

    salida = archivo_entrada.replace("_clasificado.csv", "_limpio.csv")
    df.to_csv(salida, index=False)
    print(f"Archivo '{salida}' guardado correctamente.\n")
    return salida

def normalizar_epoca(archivo_entrada):
    df = pd.read_csv(archivo_entrada)
    fechas = []

    for valor in df["Epoca"]:
        try:
            valor = str(valor).strip()
            anio = int(valor[:2])
            dia_fraccional = float(valor[2:])
            anio_completo = 2000 + anio if anio < 57 else 1900 + anio
            fecha = datetime(anio_completo,1,1) + timedelta(days=dia_fraccional-1)
            fechas.append(fecha)
        except Exception as e:
            fechas.append(None)

    df["Fecha UTC"] = fechas

    salida = archivo_entrada.replace("_limpio.csv", "_normalizado.csv")
    df.to_csv(salida, index=False)
    print(f"Archivo '{salida}' guardado correctamente con columna 'Fecha UTC'.\n")
    return salida

def main():
    print("Iniciando procesado completo del satelite ASTROCAST-0401\n")
    combinado = combinar_tle()

    if combinado:
        clasificado = clasificar_tle(combinado)
        limpio = limpiar_tle(clasificado)
        normalizado = normalizar_epoca(limpio)

        print("\n Proceso completado correctamente")
        print(f"Archivos generados:\n- {combinado}\n- {clasificado}\n- {limpio}\n- {normalizado}")



if __name__ == "__main__":
    main()