#!/bin/bash

# Script para desinstalar la configuración sudoers de BG-SDDM

echo "=== Desinstalador de configuración sudoers BG-SDDM ==="
echo "Eliminando configuración que permite ejecutar BG-SDDM sin contraseña..."

SUDOERS_FILE="/etc/sudoers.d/bg-sddm"

if [ -f "$SUDOERS_FILE" ]; then
    sudo rm "$SUDOERS_FILE"
    echo "✓ Archivo sudoers eliminado: $SUDOERS_FILE"
    echo "  Ahora BG-SDDM volverá a pedir contraseña para cambios"
else
    echo "⚠️  No se encontró el archivo sudoers de BG-SDDM"
fi

echo ""
echo "Desinstalación completada."

