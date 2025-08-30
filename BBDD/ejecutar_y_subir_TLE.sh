#!/bin/bash

# Navegar al directorio del script
cd "$(dirname "$0")" || exit 1

# Activar entorno virtual
source .venv/bin/activate

# Ejecutar el script Python
python descargar_tle.py

# Nombre del archivo CSV generado por el script
FECHA=$(date +%Y_%m_%d)
FICHERO="TLE_${FECHA}.csv"

# Verificar que el CSV se creó antes de añadirlo
if [ -f "$FICHERO" ]; then
    git add "$FICHERO" descargar_tle.py ejecutar_y_subir_TLE.sh
    git commit -m "Actualización automática de TLE: $FECHA"
    git push origin main
    echo "✅ Archivo $FICHERO subido correctamente a GitHub."
else
    echo "❌ ERROR: El archivo $FICHERO no existe."
    exit 1
fi

