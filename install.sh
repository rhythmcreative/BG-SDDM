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

echo "Instalando dependencias del sistema..."

# Instalar dependencias de Arch Linux
echo "Instalando paquetes de Python y dependencias..."
sudo pacman -S --needed python-pip python-pipx python-scikit-learn python-numpy python-gobject gtk3 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Paquetes del sistema instalados correctamente"
else
    echo "⚠️  Error instalando algunos paquetes del sistema"
fi

# Instalar dependencias de Python con pip
echo "Instalando dependencias de Python con pip..."
pip install --user Pillow webcolors 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Dependencias de Python instaladas correctamente"
else
    echo "⚠️  Error instalando algunas dependencias de Python"
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
echo "Verificando dependencias de Python..."

python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Faltan dependencias de GTK3/python-gobject"
    echo "En Arch Linux, instala: sudo pacman -S gtk3 python-gobject"
else
    echo "✓ Dependencias de GTK3/python-gobject encontradas"
fi

python3 -c "import PIL, numpy, sklearn, webcolors" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Faltan algunas dependencias de Python"
    echo "Instalando con pip: pip install --user Pillow numpy scikit-learn webcolors"
    pip install --user Pillow numpy scikit-learn webcolors
else
    echo "✓ Todas las dependencias de Python encontradas"
fi

# Hacer ejecutable el archivo .desktop
chmod +x ~/.local/share/applications/bg-sddm.desktop
echo "✓ Archivo .desktop hecho ejecutable"

# Actualizar base de datos de aplicaciones
update-desktop-database ~/.local/share/applications/ 2>/dev/null

echo ""
echo "=== Instalación completada ==="
echo "Todas las dependencias han sido instaladas:"
echo "  - python-pip, python-pipx, python-scikit-learn, python-numpy"
echo "  - python-gobject, gtk3"
echo "  - Pillow, webcolors (via pip)"
echo ""
echo "Puedes ejecutar la aplicación de las siguientes formas:"
echo "1. Desde terminal: python3 $(pwd)/bg_sddm.py"
echo "2. Desde Rofi: busca 'BG-SDDM'"
echo "3. Desde el menú de aplicaciones"
echo ""
echo "Nota: Para modificar archivos del sistema, ejecuta con permisos de administrador:"
echo "sudo python3 $(pwd)/bg_sddm.py"
echo ""
