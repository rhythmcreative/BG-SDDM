#!/bin/bash

# Script de instalación para BG-SDDM

echo "=== Instalador BG-SDDM ==="
echo "Configurando aplicación para cambiar background de SDDM..."

# Verificar que existe el directorio del tema SDDM
if [ ! -d "/usr/share/sddm/themes/sddm-astronaut-theme" ]; then
    echo "Error: No se encontró el tema SDDM en /usr/share/sddm/themes/sddm-astronaut-theme"
    echo "Asegúrate de que el tema esté instalado."
    exit 1
fi

# Crear directorio .local/share/applications si no existe
mkdir -p ~/.local/share/applications

# Copiar archivo .desktop
cp bg-sddm.desktop ~/.local/share/applications/
echo "✓ Archivo .desktop instalado en ~/.local/share/applications/"

# Hacer ejecutable el script principal
chmod +x bg_sddm.py
echo "✓ Script principal hecho ejecutable"

# Verificar dependencias de Python
echo "Verificando dependencias..."

python3 -c "import gi; gi.require_version('Gtk', '4.0'); gi.require_version('Adw', '1')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Faltan dependencias de GTK4/libadwaita"
    echo "En Arch Linux, instala: sudo pacman -S gtk4 libadwaita python-gobject"
else
    echo "✓ Dependencias de GTK4/libadwaita encontradas"
fi

# Actualizar base de datos de aplicaciones
update-desktop-database ~/.local/share/applications/ 2>/dev/null

echo ""
echo "=== Instalación completada ==="
echo "Puedes ejecutar la aplicación de las siguientes formas:"
echo "1. Desde terminal: python3 $(pwd)/bg_sddm.py"
echo "2. Desde Rofi: busca 'BG-SDDM'"
echo "3. Desde el menú de aplicaciones"
echo ""
echo "Nota: Para modificar archivos del sistema, ejecuta con permisos de administrador:"
echo "sudo python3 $(pwd)/bg_sddm.py"
echo ""

