import pandas as pd

archivo = "TLE_2025_11_06.csv"

#Leemos el .csv
df = pd.read_csv(archivo)

#Guardamos resultados en este array
resultados = []

#Recorremos cada satelite
for index, fila in df.iterrows():
    linea1 = fila["TLE Line 1"]
    linea2 = fila["TLE Line 2"]

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

#Convertimos resultados en DataFrame
df_resultado = pd.DataFrame(resultados)

#Guardamos el nuevo .csv
df_resultado.to_csv("TLE_clasificado.csv", index=False)
print("Archivo TLE_clasificado.csv generado correctamente")


#Vista previa del contenido del nuevo .csv
print("Vista previa del nuevo archivo generado")
print(df_resultado.head())