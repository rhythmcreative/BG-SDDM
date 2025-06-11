# BG-SDDM 🚀

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/GTK-4.0-green?style=for-the-badge&logo=gtk&logoColor=white" alt="GTK4"/>
  <img src="https://img.shields.io/badge/Arch-Linux-1793D1?style=for-the-badge&logo=arch-linux&logoColor=white" alt="Arch Linux"/>
  <img src="https://img.shields.io/badge/License-Open_Source-brightgreen?style=for-the-badge" alt="License"/>
</div>

<div align="center">
  <h2>🎨 Modern GTK4 Background Manager for SDDM Astronaut Theme</h2>
  <p>Una aplicación elegante y moderna con interfaz gráfica para cambiar fácilmente el fondo de pantalla del tema SDDM Astronaut.</p>
</div>

---

## ✨ Características Principales

- 🎭 **Interfaz Moderna**: Diseñada con GTK4 y libadwaita para una experiencia nativa
- 🖼️ **Vista Previa Intuitiva**: Visualiza todas las imágenes disponibles en una galería elegante
- ➕ **Gestión de Imágenes**: Añade, visualiza y gestiona fondos fácilmente
- 🔄 **Actualización Automática**: Configuración instantánea sin reiniciar servicios
- 📱 **Integración Completa**: Compatible con Rofi, menús de aplicaciones y terminal
- 💾 **Respaldo Inteligente**: Backup automático de configuraciones anteriores
- ⚡ **Rendimiento Optimizado**: Carga rápida de miniaturas y navegación fluida

---

## 📋 Requisitos del Sistema

### Sistema Operativo
- **Arch Linux** (recomendado)
- **Distribuciones basadas en Arch** (Manjaro, EndeavourOS, etc.)
- **Otras distribuciones Linux** con acceso a GTK4

### Dependencias Esenciales
| Paquete | Descripción | Instalación |
|---------|-------------|-------------|
| `gtk4` | Framework de interfaz gráfica | `sudo pacman -S gtk4` |
| `libadwaita` | Biblioteca de componentes modernos | `sudo pacman -S libadwaita` |
| `python-gobject` | Bindings de Python para GObject | `sudo pacman -S python-gobject` |
| `sddm-astronaut-theme` | Tema SDDM compatible | [Instalación manual](https://github.com/rhythmcreative/sddm-astronaut-theme) |

### 🚀 Instalación Rápida de Dependencias

**Para Arch Linux / Manjaro:**
```bash
sudo pacman -S gtk4 libadwaita python-gobject
```

**Para Ubuntu / Debian:**
```bash
sudo apt install libgtk-4-1 libadwaita-1-0 python3-gi
```

**Para Fedora:**
```bash
sudo dnf install gtk4 libadwaita python3-gobject
```

---

## 🛠️ Instalación

### Método 1: Instalación Automática (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/rhythmcreative/BG-SDDM.git
cd BG-SDDM

# Ejecutar el instalador automático
chmod +x install.sh
./install.sh
```

### Método 2: Instalación Manual

```bash
# 1. Descargar o clonar el proyecto
git clone https://github.com/rhythmcreative/BG-SDDM.git
cd BG-SDDM

# 2. Hacer ejecutable el script principal
chmod +x bg_sddm.py

# 3. Instalar el archivo .desktop
mkdir -p ~/.local/share/applications
cp bg-sddm.desktop ~/.local/share/applications/

# 4. Actualizar base de datos de aplicaciones
update-desktop-database ~/.local/share/applications/
```

### Verificación de Instalación

```bash
# Verificar dependencias
python3 -c "import gi; gi.require_version('Gtk', '4.0'); gi.require_version('Adw', '1'); print('✅ Dependencias OK')"

# Verificar tema SDDM
ls /usr/share/sddm/themes/sddm-astronaut-theme/ && echo "✅ Tema SDDM encontrado"
```

---

## 🎮 Uso de la Aplicación

### 🚀 Métodos de Lanzamiento

#### 1️⃣ Desde Rofi (Recomendado)
```bash
# Abre Rofi con tu combinación configurada
Super + A  # este es en mi caso
# Busca: "BG-SDDM"
# Presiona Enter
```

#### 2️⃣ Desde Terminal
```bash
# Modo de solo lectura (vista previa)
python3 ~/BG-SDDM/bg_sddm.py

# Modo administrador (modificar configuración)
sudo python3 ~/BG-SDDM/bg_sddm.py

# Ejecución con script helper
./run-as-admin.sh  # Incluye elevación automática de permisos
```

#### 3️⃣ Desde Menú de Aplicaciones
- **KDE**: Menú → Configuración del Sistema → BG-SDDM
- **GNOME**: Actividades → "BG-SDDM"
- **Hyprland/i3**: Lanzador de aplicaciones → "BG-SDDM"

### 🎨 Guía de Uso Detallada

#### 📂 Navegación de Imágenes
- **Vista de Galería**: Todas las imágenes se muestran en una cuadrícula elegante
- **Ubicación**: `/usr/share/sddm/themes/sddm-astronaut-theme/Backgrounds/`
- **Formatos Soportados**: PNG, JPG, JPEG, WEBP, BMP
- **Previsualización**: Miniaturas automáticas con información del archivo

#### 🖱️ Acciones Principales
| Acción | Método | Descripción |
|--------|--------|-------------|
| **Cambiar Fondo** | Clic en imagen | Aplica inmediatamente el fondo seleccionado |
| **Añadir Imagen** | Botón "+" | Abre selector de archivos para nuevas imágenes |
| **Actualizar Lista** | Botón 🔄 | Refresca la galería tras cambios manuales |
| **Vista Detallada** | Clic derecho | Muestra información completa del archivo |

#### ⚙️ Configuración Avanzada
- **Backup Automático**: Se crea `theme1.conf.backup` antes de cambios
- **Validación**: Verificación automática de formato e integridad
- **Logs**: Información detallada en terminal para depuración

---

## 📁 Estructura del Proyecto

```
BG-SDDM/
├── 🐍 bg_sddm.py          # Aplicación principal GTK4
├── 🖥️ bg-sddm.desktop     # Integración con sistema (menús)
├── 🔧 install.sh          # Instalador automático
├── ⚡ run-as-admin.sh     # Helper para ejecución con permisos
├── 📚 README.md           # Documentación completa
└── 📋 requirements.txt    # Dependencias Python (opcional)
```

### 🎯 Archivos de Sistema Gestionados

| Archivo | Ubicación | Función |
|---------|-----------|----------|
| **Configuración Principal** | `/usr/share/sddm/themes/sddm-astronaut-theme/Themes/theme1.conf` | Configuración activa del tema |
| **Directorio de Imágenes** | `/usr/share/sddm/themes/sddm-astronaut-theme/Backgrounds/` | Almacén de fondos disponibles |
| **Backup de Configuración** | `theme1.conf.backup` | Respaldo automático anterior |
| **Archivo Desktop** | `~/.local/share/applications/bg-sddm.desktop` | Integración con lanzadores |
---

## 🔧 Características Técnicas

### 🏗️ Arquitectura
- **Lenguaje**: Python 3.8+
- **Framework GUI**: GTK4 + libadwaita
- **Patrón de Diseño**: Model-View-Controller (MVC)
- **Gestión de Imágenes**: GdkPixbuf con cache optimizado
- **Configuración**: Parser INI nativo de Python

### ⚡ Optimizaciones
- **Carga Asíncrona**: Miniaturas se cargan en segundo plano
- **Cache Inteligente**: Evita recargas innecesarias
- **Gestión de Memoria**: Liberación automática de recursos
- **Validación Robusta**: Verificación de integridad de archivos

### 🔒 Seguridad
- **Validación de Rutas**: Prevención de directory traversal
- **Verificación de Permisos**: Comprobación antes de modificaciones
- **Backup Automático**: Recuperación ante errores
- **Logs Seguros**: Información sin datos sensibles

---

## 🛠️ Solución de Problemas

### ❌ Problemas Comunes y Soluciones

#### 🔐 **Error de Permisos**
```bash
# Problema: "Permission denied" al modificar configuración
# Solución: Ejecutar con permisos elevados
sudo python3 ~/BG-SDDM/bg_sddm.py

# O usar el script helper incluido
./run-as-admin.sh
```

#### 📱 **Aplicación No Aparece en Rofi/Menús**
```bash
# 1. Verificar instalación del archivo .desktop
ls ~/.local/share/applications/bg-sddm.desktop

# 2. Reinstalar archivo .desktop
cp bg-sddm.desktop ~/.local/share/applications/

# 3. Actualizar base de datos de aplicaciones
update-desktop-database ~/.local/share/applications/

# 4. Limpiar cache de rofi (si usas rofi)
rm -rf ~/.cache/rofi
```

#### 🐍 **Dependencias Faltantes**
```bash
# Error: ModuleNotFoundError: No module named 'gi'
# Solución para Arch Linux:
sudo pacman -S gtk4 libadwaita python-gobject

# Solución para Ubuntu/Debian:
sudo apt install libgtk-4-1 libadwaita-1-0 python3-gi

# Verificar instalación:
python3 -c "import gi; print('✅ GI instalado correctamente')"
```

#### 🎨 **Tema SDDM No Encontrado**
```bash
# Error: Directorio del tema no existe
# Verificar instalación del tema:
ls /usr/share/sddm/themes/sddm-astronaut-theme/

# Si no existe, instalar tema desde:
# https://github.com/rhythmcreative/sddm-astronaut-theme
```

#### 🖼️ **Imágenes No Se Muestran**
```bash
# Verificar permisos del directorio
ls -la /usr/share/sddm/themes/sddm-astronaut-theme/Backgrounds/

# Verificar formatos soportados (PNG, JPG, JPEG, WEBP, BMP)
file /usr/share/sddm/themes/sddm-astronaut-theme/Backgrounds/*

# Recargar aplicación o usar botón de actualizar
```

### 🔍 **Modo Debug**

```bash
# Ejecutar con información detallada
GTK_DEBUG=interactive python3 bg_sddm.py

# Logs adicionales
G_MESSAGES_DEBUG=all python3 bg_sddm.py
```

---

## 🤝 Contribuir al Proyecto

### 🐛 **Reportar Bugs**
1. **Verificar** que el bug no esté ya reportado
2. **Incluir** información del sistema:
   ```bash
   echo "Sistema: $(uname -a)"
   echo "Python: $(python3 --version)"
   echo "GTK: $(pkg-config --modversion gtk4)"
   ```
3. **Describir** pasos para reproducir el problema
4. **Adjuntar** logs si es posible

### ✨ **Sugerir Características**
- 🎨 Nuevos temas o estilos
- 🔧 Mejoras en la interfaz
- ⚡ Optimizaciones de rendimiento
- 🌐 Soporte para más distribuciones

### 🔧 **Desarrollo**
```bash
# Fork del repositorio
git clone https://github.com/tu-usuario/BG-SDDM.git
cd BG-SDDM

# Crear rama para tu característica
git checkout -b feature/nueva-caracteristica

# Hacer cambios y commit
git add .
git commit -m "feat: añadir nueva característica"

# Push y crear Pull Request
git push origin feature/nueva-caracteristica
```

### 📋 **Estándares de Código**
- **PEP 8**: Estilo de código Python
- **Type Hints**: Tipado estático recomendado
- **Docstrings**: Documentación en funciones
- **Tests**: Incluir tests para nuevas características

---

## 🚀 Roadmap

### 📅 **Próximas Características**
- [ ] 🌙 **Modo Oscuro/Claro**: Seguir tema del sistema
- [ ] 🔄 **Auto-rotación**: Cambio automático de fondos
- [ ] ☁️ **Soporte en la Nube**: Integración con servicios online
- [ ] 🎨 **Editor de Temas**: Personalización avanzada
- [ ] 📱 **Versión Web**: Interfaz web para gestión remota
- [ ] 🔌 **Plugins**: Sistema de extensiones

### 🎯 **Versiones Planeadas**
- **v2.0**: Refactorización completa con nuevas características
- **v2.1**: Soporte multi-tema
- **v2.2**: Integración con gestores de ventanas populares

---

## ⚖️ Licencia

```
MIT License

Copyright (c) 2024 RhythmCreative

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 💬 Contacto y Enlaces

- **🐙 Repositorio**: [github.com/rhythmcreative/BG-SDDM](https://github.com/rhythmcreative/BG-SDDM)
- **🎨 Tema SDDM**: [sddm-astronaut-theme](https://github.com/rhythmcreative/sddm-astronaut-theme)
- **🏠 HyprDots**: [hyprdots](https://github.com/rhythmcreative/hyprdots)

---

## 🙏 Agradecimientos

- **GTK Team**: Por el increíble framework GTK4
- **GNOME Project**: Por libadwaita y las herramientas de desarrollo
- **Python Community**: Por las librerías y documentación
- **SDDM Project**: Por el gestor de pantalla extensible
- **Arch Linux**: Por el ecosistema de desarrollo robusto

---

<div align="center">
  <h3>✨ Hecho con ❤️ por RhythmCreative ✨</h3>
  <p>Si este proyecto te ha sido útil, ¡considera darle una ⭐!</p>
</div>
