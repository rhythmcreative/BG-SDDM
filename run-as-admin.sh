#!/bin/bash

# Script para ejecutar BG-SDDM con permisos de administrador

echo "Ejecutando BG-SDDM con permisos de administrador..."
echo "Se requiere contraseña para modificar archivos del sistema."
echo ""

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Ejecutar con sudo
sudo python3 bg_sddm.py

