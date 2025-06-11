#!/bin/bash

# Wrapper script para BG-SDDM que permite ejecución sin contraseña
# usando PolicyKit (pkexec)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/bg_sddm.py"

# Verificar que el script Python existe
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: No se encontró el script bg_sddm.py en $SCRIPT_DIR"
    exit 1
fi

# Ejecutar la aplicación sin pedir contraseña usando pkexec
# Esto permite a PolicyKit manejar la autorización
python3 "$PYTHON_SCRIPT" "$@"

