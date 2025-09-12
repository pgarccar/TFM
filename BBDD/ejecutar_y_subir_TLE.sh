#!/bin/bash
# Descarga TLE, integra cambios remotos y sube el CSV al repo (vía SSH)

set -Eeuo pipefail

BRANCH="${BRANCH:-main}"
SCRIPT="descargar_tle.py"

# Ir al directorio del script
cd "$(dirname "$0")"

# Comprobaciones básicas
command -v git >/dev/null || { echo "❌ ERROR: git no está instalado."; exit 1; }
command -v python3 >/dev/null || { echo "❌ ERROR: python3 no está instalado."; exit 1; }
git rev-parse --is-inside-work-tree >/dev/null || { echo "❌ ERROR: este directorio no es un repo Git."; exit 1; }

# Forzar remoto por SSH si aún es HTTPS
ORIGIN_URL="$(git remote get-url origin)"
if [[ "$ORIGIN_URL" =~ ^https://github\.com/([^/]+)/([^/]+)\.git$ ]]; then
  USER="${BASH_REMATCH[1]}"; REPO="${BASH_REMATCH[2]}"
  git remote set-url origin "git@github.com:${USER}/${REPO}.git"
fi

# Asegurar rama
git checkout "$BRANCH"

# Crear/activar venv y deps
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -c "import pandas,requests" 2>/dev/null || pip install -U pip pandas requests

# Integrar cambios remotos antes de generar y subir
git fetch origin "$BRANCH"
git pull --rebase --autostash origin "$BRANCH"

# Ejecutar script de descarga
python "$SCRIPT"

# Nombre de archivo (UTC para alinear con el script Python)
FECHA="$(date -u +%Y_%m_%d)"
FICHERO="TLE_${FECHA}.csv"

if [ ! -f "$FICHERO" ]; then
  echo "❌ ERROR: no se generó $FICHERO."
  exit 1
fi

# Añadir y commitear si hay cambios
git add "$FICHERO" "$SCRIPT" "$(basename "$0")"
if git diff --cached --quiet; then
  echo "ℹ️ No hay cambios que subir (nada que commitear)."
  exit 0
fi

git commit -m "Actualización automática de TLE: $FECHA"

# Push con verificación real
if git push origin "$BRANCH"; then
  echo "✅ Archivo $FICHERO subido correctamente a GitHub."
else
  echo "❌ ERROR: falló el push (revisa autenticación SSH o conflictos)."
  exit 1
fi

