#!/bin/bash

# Navegar al directorio del script
cd "$(dirname "$0")"

# Activar entorno virtual
source .venv/bin/activate

# Ejecutar el script Python
python descargar_tle.py

# Obtener la fecha actual
FECHA=$(date +%Y_%m_%d)
FICHERO="TLE_${FECHA}.csv"

# Añadir solo los archivos relevantes a git (evitando subir .venv/)
git add "$FICHERO" descargar_tle.py ejecutar_y_subir_TLE.sh
git commit -m "Añadir TLE actualizado del día $FECHA"
git push origin main

echo "Archivo $FICHERO subido correctamente a GitHub."
