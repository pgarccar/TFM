import requests
from datetime import datetime, timezone
import pandas as pd

# URL con los TLE
url = "https://celestrak.org/NORAD/elements/gp.php?INTDES=2023-001"

# Descargar los datos
response = requests.get(url)
tle_text = response.text.strip().splitlines()

# Parseo de los datos (nombre + líneas TLE)
satellite_data = []
for i in range(0, len(tle_text), 3):
    name = tle_text[i].strip()
    line1 = tle_text[i+1].strip()
    line2 = tle_text[i+2].strip()
    satellite_data.append([name, line1, line2])

# Guardar en CSV con formato TLE_AAAA_MM_DD.csv
today = datetime.now(timezone.utc).strftime("%Y_%m_%d")
filename = f"TLE_{today}.csv"
df = pd.DataFrame(satellite_data, columns=["Satellite Name", "TLE Line 1", "TLE Line 2"])
df.to_csv(filename, index=False)

print(f"Archivo guardado como {filename}")
