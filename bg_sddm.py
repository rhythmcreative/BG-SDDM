#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, GLib, Gio, Gdk, GdkPixbuf, Pango
import os
import shutil
import subprocess
import sys
from pathlib import Path
import tempfile

# For additional functionalities
import json
from datetime import datetime
import urllib.parse
from PIL import Image, ImageStat
import colorsys
import numpy as np
from sklearn.cluster import KMeans
import webcolors

class SDDMBackgroundChanger(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.rhythmcreative.bg-sddm')
        self.theme_path = '/usr/share/sddm/themes/sddm-astronaut-theme'
        self.backgrounds_path = f'{self.theme_path}/Backgrounds'
        self.config_path = f'{self.theme_path}/Themes/theme1.conf'
        self.current_theme_colors = {
            'primary': '#1a1a1a',
            'secondary': '#2d2d2d', 
            'accent': '#4CAF50',
            'text': '#e0e0e0'
        }
        self.css_provider = None
        self.setup_css()
        
    def extract_colors_from_image(self, image_path):
        """Extract dominant colors from an image"""
        try:
            # Open and resize image for faster processing
            with Image.open(image_path) as img:
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize for faster processing
                img.thumbnail((150, 150))
                
                # Get image data as numpy array
                img_array = np.array(img)
                pixels = img_array.reshape(-1, 3)
                
                # Use KMeans to find dominant colors
                kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
                kmeans.fit(pixels)
                
                # Get the colors and their frequencies
                colors = kmeans.cluster_centers_.astype(int)
                
                # Sort by frequency (cluster size)
                labels = kmeans.labels_
                label_counts = np.bincount(labels)
                dominant_colors = [colors[i] for i in np.argsort(label_counts)[::-1]]
                
                # Convert to hex
                hex_colors = ['#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b)) for r, g, b in dominant_colors]
                
                return self.generate_theme_from_colors(hex_colors)
                
        except Exception as e:
            print(f"Error extracting colors: {e}")
            return self.get_default_theme()
    
    def generate_theme_from_colors(self, colors):
        """Generate a theme from extracted colors"""
        # Get the most dominant color
        primary_color = colors[0]
        
        # Convert to HSL for better color manipulation
        rgb = tuple(int(primary_color[i:i+2], 16) for i in (1, 3, 5))
        h, l, s = colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        
        # Generate complementary colors
        # Dark background
        dark_l = max(0.05, l * 0.1)  # Very dark version
        dark_rgb = colorsys.hls_to_rgb(h, dark_l, s)
        dark_color = '#{:02x}{:02x}{:02x}'.format(
            int(dark_rgb[0] * 255), int(dark_rgb[1] * 255), int(dark_rgb[2] * 255)
        )
        
        # Medium background  
        medium_l = max(0.1, l * 0.2)  # Dark version
        medium_rgb = colorsys.hls_to_rgb(h, medium_l, s)
        medium_color = '#{:02x}{:02x}{:02x}'.format(
            int(medium_rgb[0] * 255), int(medium_rgb[1] * 255), int(medium_rgb[2] * 255)
        )
        
        # Accent color (brighter version)
        accent_l = min(0.7, l * 1.5)
        accent_rgb = colorsys.hls_to_rgb(h, accent_l, min(1.0, s * 1.2))
        accent_color = '#{:02x}{:02x}{:02x}'.format(
            int(accent_rgb[0] * 255), int(accent_rgb[1] * 255), int(accent_rgb[2] * 255)
        )
        
        # Text color (high contrast)
        text_color = '#e0e0e0' if l < 0.5 else '#2c3e50'
        
        return {
            'primary': dark_color,
            'secondary': medium_color,
            'accent': accent_color,
            'text': text_color,
            'original': primary_color
        }
    
    def get_default_theme(self):
        """Get default theme colors"""
        return {
            'primary': '#1a1a1a',
            'secondary': '#2d2d2d', 
            'accent': '#4CAF50',
            'text': '#e0e0e0'
        }
    
    def apply_dynamic_theme(self, colors):
        """Apply dynamic theme based on extracted colors"""
        self.current_theme_colors = colors
        
        # Update CSS with new colors
        css = f"""
        /* Main window styling */
        window {{
            background-color: {colors['primary']};
        }}
        
        /* Header bar styling */
        headerbar {{
            background: {colors['secondary']};
            color: white;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        headerbar button {{
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 6px;
            color: white;
        }}
        
        headerbar button:hover {{
            background: rgba(255,255,255,0.2);
        }}
        
        /* Main content area */
        .main-content {{
            background: {colors['secondary']};
            border-radius: 12px;
            margin: 20px;
            color: {colors['text']};
        }}
        
        /* Image containers */
        .image-container {{
            background: {colors['secondary']};
            border-radius: 12px;
            margin: 8px;
            padding: 12px;
        }}
        
        .image-container:hover {{
            background-color: {colors['accent']};
            background-image: linear-gradient(rgba(255,255,255,0.1), rgba(255,255,255,0.1));
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        
        .image-container.current {{
            border: 3px solid {colors['accent']};
        }}
        
        /* Flow box styling */
        flowbox {{
            background: transparent;
        }}
        
        flowboxchild {{
            background: transparent;
            border-radius: 12px;
            margin: 4px;
        }}
        
        flowboxchild:selected {{
            background: rgba(102,126,234,0.1);
        }}
        
        /* Status bar */
        .status-bar {{
            background: {colors['secondary']};
            border-radius: 8px;
            padding: 8px 12px;
            color: {colors['text']};
        }}
        
        /* Scrolled window */
        scrolledwindow {{
            background: transparent;
        }}
        
        /* Text elements */
        label {{
            color: {colors['text']};
        }}
        
        .dim-label {{
            color: {colors['text']};
            opacity: 0.7;
        }}
        
        /* Image labels */
        .image-label {{
            color: {colors['text']};
        }}
        
        .current-label {{
            color: {colors['accent']};
            font-weight: bold;
        }}
        
        /* Buttons */
        button.add-button {{
            background: {colors['accent']};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: bold;
        }}
        
        button.add-button:hover {{
            background: {colors['accent']};
            opacity: 0.8;
        }}
        
        /* Delete button styling */
        .delete-button {{
            background: rgba(255, 71, 87, 0.9);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 6px;
            font-size: 14px;
            font-weight: normal;
            opacity: 0.0;
            margin: 4px;
        }}
        
        .image-container:hover .delete-button {{
            opacity: 1.0;
        }}
        
        .delete-button:hover {{
            background: rgba(255, 71, 87, 0.9);
            color: white;
            border: none;
            opacity: 1.0;
        }}
        
        .delete-button:active {{
            background: rgba(255, 55, 66, 1.0);
            color: white;
        }}
        
        /* Drag and drop styling */
        .drop-target {{
            border: 3px dashed {colors['accent']};
            border-radius: 8px;
            background-color: rgba(0, 0, 0, 0.1);
        }}
        
        .drag-highlight {{
            background-color: rgba(100, 150, 255, 0.2);
        }}
        """
        
        # Apply the new CSS
        if self.css_provider:
            screen = Gdk.Screen.get_default()
            style_context = Gtk.StyleContext()
            style_context.remove_provider_for_screen(screen, self.css_provider)
        
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_data(css.encode())
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    
    def setup_css(self):
        """Setup initial CSS styling for the application"""
        # Apply default theme initially
        self.apply_dynamic_theme(self.current_theme_colors)
        
    def do_activate(self):
        self.win = SDDMWindow(application=self)
        self.win.show_all()

class SDDMWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title('SDDM Background Changer')
        self.set_default_size(900, 700)
        self.set_resizable(True)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.theme_path = '/usr/share/sddm/themes/sddm-astronaut-theme'
        self.backgrounds_path = f'{self.theme_path}/Backgrounds'
        self.config_path = f'{self.theme_path}/Themes/theme1.conf'
        
        # Configuration and settings
        self.config_file = os.path.expanduser('~/.config/bg-sddm/settings.json')
        self.load_app_settings()
        
        self.setup_ui()
        self.load_backgrounds()
        
        # Apply dynamic theme based on current background
        self.apply_initial_theme()
        
    def load_app_settings(self):
        """Load application settings from config file"""
        self.settings = {
            'window_width': 900,
            'window_height': 700,
            'grid_columns': 4,
            'last_used_theme': self.theme_path,
            'preview_size': 160
        }
        
        try:
            config_dir = os.path.dirname(self.config_file)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)
                
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    saved_settings = json.load(f)
                    self.settings.update(saved_settings)
                    
        except Exception as e:
            print(f"Error loading settings: {e}")
            
    def save_app_settings(self):
        """Save application settings to config file"""
        try:
            # Update current window size
            width, height = self.get_size()
            self.settings['window_width'] = width
            self.settings['window_height'] = height
            
            config_dir = os.path.dirname(self.config_file)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)
                
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
                
        except Exception as e:
            print(f"Error saving settings: {e}")
            
    def apply_initial_theme(self):
        """Apply dynamic theme based on current background when app starts"""
        try:
            current_bg = self.get_current_background()
            if current_bg:
                image_path = os.path.join(self.backgrounds_path, current_bg)
                if os.path.exists(image_path):
                    app = self.get_application()
                    colors = app.extract_colors_from_image(image_path)
                    app.apply_dynamic_theme(colors)
                    print(f"Debug - Applied initial theme from {current_bg}: {colors}")
        except Exception as e:
            print(f"Error applying initial theme: {e}")
        
    def setup_ui(self):
        # Header bar
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.set_title('SDDM Background Changer')
        self.set_titlebar(header_bar)
        
        # Add image button
        add_button = Gtk.Button()
        add_button.set_image(Gtk.Image.new_from_icon_name('list-add-symbolic', Gtk.IconSize.BUTTON))
        add_button.set_tooltip_text('Añadir nueva imagen')
        add_button.connect('clicked', self.on_add_image_clicked)
        header_bar.pack_start(add_button)
        
        # Refresh button
        refresh_button = Gtk.Button()
        refresh_button.set_image(Gtk.Image.new_from_icon_name('view-refresh-symbolic', Gtk.IconSize.BUTTON))
        refresh_button.set_tooltip_text('Actualizar lista')
        refresh_button.connect('clicked', self.on_refresh_clicked)
        header_bar.pack_start(refresh_button)
        
        # Settings button
        settings_button = Gtk.Button()
        settings_button.set_image(Gtk.Image.new_from_icon_name('preferences-system-symbolic', Gtk.IconSize.BUTTON))
        settings_button.set_tooltip_text('Configuración')
        settings_button.connect('clicked', self.on_settings_clicked)
        header_bar.pack_end(settings_button)
        
        # About button
        about_button = Gtk.Button()
        about_button.set_image(Gtk.Image.new_from_icon_name('help-about-symbolic', Gtk.IconSize.BUTTON))
        about_button.set_tooltip_text('Acerca de')
        about_button.connect('clicked', self.on_about_clicked)
        header_bar.pack_end(about_button)
        
        # Main content
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        main_box.set_margin_top(12)
        main_box.set_margin_bottom(12)
        main_box.set_margin_start(12)
        main_box.set_margin_end(12)
        
        # Title and description
        title_label = Gtk.Label()
        title_label.set_markup('<span size="large" weight="bold">Cambiar Background de SDDM</span>')
        title_label.set_halign(Gtk.Align.START)
        main_box.pack_start(title_label, False, False, 0)
        
        desc_label = Gtk.Label()
        desc_label.set_text('Selecciona una imagen para cambiar el fondo de la pantalla de login')
        desc_label.set_halign(Gtk.Align.START)
        style_context = desc_label.get_style_context()
        style_context.add_class('dim-label')
        main_box.pack_start(desc_label, False, False, 0)
        
        # Scrolled window for image grid
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        
        # Flow box for images
        self.flow_box = Gtk.FlowBox()
        self.flow_box.set_valign(Gtk.Align.START)
        self.flow_box.set_max_children_per_line(4)
        self.flow_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.flow_box.connect('child-activated', self.on_image_selected)
        
        # Setup drag and drop for the flow_box
        self.setup_drag_and_drop()
        
        scrolled.add(self.flow_box)
        main_box.pack_start(scrolled, True, True, 0)
        
        # Status bar
        self.status_label = Gtk.Label()
        self.status_label.set_text('Listo')
        self.status_label.set_halign(Gtk.Align.START)
        style_context = self.status_label.get_style_context()
        style_context.add_class('dim-label')
        main_box.pack_start(self.status_label, False, False, 0)
        
        self.add(main_box)
        
    def load_backgrounds(self):
        """Cargar todas las imágenes del directorio de backgrounds"""
        print("Debug - load_backgrounds() called")
        
        # Limpiar flow box
        for child in self.flow_box.get_children():
            self.flow_box.remove(child)
            
        try:
            if not os.path.exists(self.backgrounds_path):
                self.show_error_dialog('No se encontró el directorio de backgrounds')
                return
                
            # Obtener fondo actual
            current_bg = self.get_current_background()
            print(f"Debug - Current background: {current_bg}")
            
            # Cargar imágenes
            image_files = []
            for file in os.listdir(self.backgrounds_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_files.append(file)
                    
            image_files.sort()
            print(f"Debug - Found {len(image_files)} image files")
            
            for image_file in image_files:
                print(f"Debug - Adding image: {image_file}, is_current: {image_file == current_bg}")
                self.add_image_to_grid(image_file, image_file == current_bg)
                
            # Asegurar que el flow_box se muestre
            self.flow_box.show_all()
                
            status_text = f'Cargadas {len(image_files)} imágenes'
            if current_bg:
                status_text += f' - Actual: {current_bg}'
            self.status_label.set_text(status_text)
            
        except Exception as e:
            error_msg = f'Error al cargar imágenes: {str(e)}'
            print(f"Debug - {error_msg}")
            self.show_error_dialog(error_msg)
    
    def setup_drag_and_drop(self):
        """Setup drag and drop functionality"""
        # Set up the flow_box as a drop target
        self.flow_box.drag_dest_set(
            Gtk.DestDefaults.ALL,
            [],
            Gdk.DragAction.COPY
        )
        
        # Add target for files
        target_list = Gtk.TargetList.new([])
        target_list.add_uri_targets(0)
        target_list.add_text_targets(1)
        self.flow_box.drag_dest_set_target_list(target_list)
        
        # Connect drag and drop signals
        self.flow_box.connect('drag-data-received', self.on_drag_data_received)
        self.flow_box.connect('drag-motion', self.on_drag_motion)
        self.flow_box.connect('drag-leave', self.on_drag_leave)
        
    def on_drag_motion(self, widget, drag_context, x, y, time):
        """Handle drag motion over the widget"""
        # Add visual feedback
        style_context = widget.get_style_context()
        style_context.add_class('drag-highlight')
        
        # Accept the drag
        Gdk.drag_status(drag_context, Gdk.DragAction.COPY, time)
        return True
        
    def on_drag_leave(self, widget, drag_context, time):
        """Handle drag leave"""
        # Remove visual feedback
        style_context = widget.get_style_context()
        style_context.remove_class('drag-highlight')
        
    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        """Handle dropped data"""
        # Remove visual feedback
        style_context = widget.get_style_context()
        style_context.remove_class('drag-highlight')
        
        # Get the dropped data
        uris = data.get_uris()
        
        if uris:
            for uri in uris:
                # Convert URI to local path
                file_path = GLib.filename_from_uri(uri)[0]
                
                # Check if it's an image file
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    self.add_dropped_image(file_path)
                else:
                    self.show_error_dialog(f'Archivo no válido: {os.path.basename(file_path)}\nSolo se permiten imágenes.')
        
        # Finish the drag
        Gtk.drag_finish(drag_context, True, False, time)
        
    def add_dropped_image(self, source_path):
        """Add a dropped image to the backgrounds folder"""
        try:
            filename = os.path.basename(source_path)
            dest_path = os.path.join(self.backgrounds_path, filename)
            
            # Check if file already exists
            if os.path.exists(dest_path):
                dialog = Gtk.MessageDialog(
                    transient_for=self,
                    modal=True,
                    message_type=Gtk.MessageType.QUESTION,
                    buttons=Gtk.ButtonsType.YES_NO,
                    text=f'La imagen "{filename}" ya existe.\n¿Deseas reemplazarla?'
                )
                response = dialog.run()
                dialog.destroy()
                
                if response != Gtk.ResponseType.YES:
                    return
            
            # Copy the file
            try:
                shutil.copy2(source_path, dest_path)
                self.status_label.set_text(f'Imagen añadida: {filename}')
                self.load_backgrounds()
                
            except PermissionError:
                # Try using pkexec for copying file
                if self.try_pkexec_copy(source_path, dest_path):
                    self.status_label.set_text(f'Imagen añadida: {filename}')
                    self.load_backgrounds()
                else:
                    self.show_error_dialog('Error de permisos. No se pudo copiar la imagen.')
                    
        except Exception as e:
            self.show_error_dialog(f'Error al añadir imagen: {str(e)}')
            
    def add_image_to_grid(self, filename, is_current=False):
        """Añadir una imagen al grid"""
        image_path = os.path.join(self.backgrounds_path, filename)
        
        # Main container
        main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        main_container.set_size_request(180, 160)
        
        # Image container with overlay for delete button
        image_overlay = Gtk.Overlay()
        
        # Imagen
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_path, 160, 90, True)
            image = Gtk.Image.new_from_pixbuf(pixbuf)
        except:
            # Si no se puede cargar la imagen, mostrar icono
            image = Gtk.Image.new_from_icon_name('image-x-generic', Gtk.IconSize.DIALOG)
            
        image.set_size_request(160, 90)
        image_overlay.add(image)
        
        # Delete button (only if not current background)
        if not is_current:
            delete_button = Gtk.Button()
            delete_button.set_label('×')
            delete_button.set_tooltip_text(f'Eliminar {filename}')
            delete_button.set_size_request(24, 24)
            delete_button.get_style_context().add_class('delete-button')
            delete_button.set_halign(Gtk.Align.END)
            delete_button.set_valign(Gtk.Align.START)
            delete_button.set_margin_top(4)
            delete_button.set_margin_end(4)
            delete_button.connect('clicked', self.on_delete_image, filename)
            image_overlay.add_overlay(delete_button)
        
        main_container.pack_start(image_overlay, False, False, 0)
        
        # Label con nombre
        label = Gtk.Label()
        label.set_text(filename)
        label.set_ellipsize(3)  # Pango.EllipsizeMode.END
        label.set_max_width_chars(20)
        main_container.pack_start(label, False, False, 0)
        
        # Indicador de imagen actual
        if is_current:
            current_label = Gtk.Label()
            current_label.set_markup('<span color="#4CAF50" weight="bold">● Actual</span>')
            main_container.pack_start(current_label, False, False, 0)
        
        # Setup hover effect
        self.setup_hover_effect(main_container)
            
        # Guardar filename como data
        main_container.filename = filename
        
        self.flow_box.add(main_container)
        
    def setup_hover_effect(self, container):
        """Setup hover effect for image containers"""
        # Add CSS class for styling
        container.get_style_context().add_class('image-container')
        
        # Connect mouse events
        container.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK | 
                           Gdk.EventMask.LEAVE_NOTIFY_MASK)
        container.connect('enter-notify-event', self.on_image_enter)
        container.connect('leave-notify-event', self.on_image_leave)
        
    def on_image_enter(self, widget, event):
        """Handle mouse enter on image"""
        # The hover effect is handled by CSS, but we can add additional logic here if needed
        return False
        
    def on_image_leave(self, widget, event):
        """Handle mouse leave on image"""
        # The hover effect is handled by CSS, but we can add additional logic here if needed
        return False
        
    def on_delete_image(self, button, filename):
        """Handle image deletion"""
        # Confirm deletion
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text=f'¿Estás seguro de que quieres eliminar "{filename}"?'
        )
        dialog.format_secondary_text('Esta acción no se puede deshacer.')
        
        response = dialog.run()
        dialog.destroy()
        
        if response == Gtk.ResponseType.YES:
            self.delete_background_image(filename)
            
    def delete_background_image(self, filename):
        """Delete a background image"""
        try:
            image_path = os.path.join(self.backgrounds_path, filename)
            
            # Check if this is the current background
            current_bg = self.get_current_background()
            if filename == current_bg:
                self.show_error_dialog('No puedes eliminar el fondo de pantalla actual.\nPrimero cambia a otro fondo.')
                return
            
            # Try to delete directly first
            try:
                os.remove(image_path)
                self.status_label.set_text(f'Imagen eliminada: {filename}')
                self.load_backgrounds()
                
            except PermissionError:
                # Try using pkexec for deletion
                if self.try_pkexec_delete(image_path):
                    self.status_label.set_text(f'Imagen eliminada: {filename}')
                    self.load_backgrounds()
                else:
                    self.show_error_dialog('Error de permisos. No se pudo eliminar la imagen.')
                    
        except Exception as e:
            self.show_error_dialog(f'Error al eliminar imagen: {str(e)}')
            
    def try_pkexec_delete(self, file_path):
        """Try to delete file using pkexec"""
        try:
            result = subprocess.run([
                'pkexec', 'rm', file_path
            ], capture_output=True, text=True)
            
            return result.returncode == 0
        except Exception as e:
            print(f"pkexec delete failed: {e}")
            return False
        
    def get_current_background(self):
        """Obtener el fondo actual del archivo de configuración"""
        try:
            with open(self.config_path, 'r') as f:
                content = f.read()
                
            for line in content.split('\n'):
                if line.strip().startswith('Background=') and not 'DimBackground' in line and not 'CropBackground' in line and not 'HaveFormBackground' in line:
                    bg_path = line.split('=', 1)[1].strip().strip('"')
                    # Extraer solo el nombre del archivo
                    filename = os.path.basename(bg_path)
                    print(f"Debug - Current background from config: {filename}")
                    return filename
                    
        except Exception as e:
            print(f'Error al leer configuración: {e}')
            
        return None
        
    def on_image_selected(self, flow_box, child):
        """Manejar selección de imagen"""
        container = child.get_child()
        filename = getattr(container, 'filename', None)
        
        if filename:
            self.change_background(filename)
            
    def change_background(self, filename):
        """Cambiar el fondo en el archivo de configuración"""
        try:
            # Extraer colores de la imagen seleccionada y aplicar tema dinámico
            image_path = os.path.join(self.backgrounds_path, filename)
            if os.path.exists(image_path):
                app = self.get_application()
                colors = app.extract_colors_from_image(image_path)
                app.apply_dynamic_theme(colors)
                print(f"Debug - Applied dynamic theme from {filename}: {colors}")
            
            # Leer archivo actual
            with open(self.config_path, 'r') as f:
                content = f.read()
                
            # Reemplazar línea de background
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('Background=') and not 'DimBackground' in line and not 'CropBackground' in line and not 'HaveFormBackground' in line:
                    lines[i] = f'Background="Backgrounds/{filename}"'
                    break
                    
            # Escribir archivo modificado
            new_content = '\n'.join(lines)
            
            # Intentar escribir directamente primero
            try:
                # Crear respaldo
                backup_path = f'{self.config_path}.backup'
                shutil.copy2(self.config_path, backup_path)
                
                # Escribir nueva configuración
                with open(self.config_path, 'w') as f:
                    f.write(new_content)
                    
                self.status_label.set_text(f'Fondo cambiado a: {filename} - Tema aplicado automáticamente')
                
                # Recargar en el hilo principal usando GLib.idle_add
                GLib.idle_add(self.load_backgrounds)
                
                # Mostrar diálogo de confirmación
                self.show_success_dialog(f'El fondo se ha cambiado a "{filename}".\nEl tema de la aplicación se ha adaptado automáticamente.\nReinicia SDDM para ver los cambios.')
                
            except PermissionError:
                # Try using pkexec for privilege escalation
                if self.try_pkexec_write(new_content):
                    self.status_label.set_text(f'Fondo cambiado a: {filename}')
                    GLib.idle_add(self.load_backgrounds)
                    self.show_success_dialog(f'El fondo se ha cambiado a "{filename}".\nReinicia SDDM para ver los cambios.')
                else:
                    self.show_error_dialog('Error de permisos. No se pudo escribir el archivo de configuración.')
                    
        except Exception as e:
            self.show_error_dialog(f'Error al cambiar fondo: {str(e)}')
            print(f'Debug - Error details: {e}')
            
    def on_add_image_clicked(self, button):
        """Abrir diálogo para añadir nueva imagen"""
        dialog = Gtk.FileChooserDialog(
            title='Seleccionar imagen',
            parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        
        dialog.add_button('Cancelar', Gtk.ResponseType.CANCEL)
        dialog.add_button('Añadir', Gtk.ResponseType.OK)
        
        # Filtro para imágenes
        filter_images = Gtk.FileFilter()
        filter_images.set_name('Imágenes')
        filter_images.add_mime_type('image/png')
        filter_images.add_mime_type('image/jpeg')
        filter_images.add_mime_type('image/jpg')
        dialog.add_filter(filter_images)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            if filename:
                source_path = filename
                filename = os.path.basename(source_path)
                dest_path = os.path.join(self.backgrounds_path, filename)
                
                try:
                    # Copiar archivo
                    shutil.copy2(source_path, dest_path)
                    self.status_label.set_text(f'Imagen añadida: {filename}')
                    self.load_backgrounds()
                    
                except PermissionError:
                    # Try using pkexec for copying file
                    if self.try_pkexec_copy(source_path, dest_path):
                        self.status_label.set_text(f'Imagen añadida: {filename}')
                        self.load_backgrounds()
                    else:
                        self.show_error_dialog('Error de permisos. No se pudo copiar la imagen.')
                except Exception as e:
                    self.show_error_dialog(f'Error al añadir imagen: {str(e)}')
                    
        dialog.destroy()
        
        
    def on_refresh_clicked(self, button):
        """Actualizar lista de imágenes"""
        self.load_backgrounds()
        
    def show_error_dialog(self, message):
        """Mostrar diálogo de error"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.set_title('Error')
        dialog.run()
        dialog.destroy()
        
    def show_success_dialog(self, message):
        """Mostrar diálogo de éxito"""
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message
        )
        dialog.set_title('Éxito')
        dialog.run()
        dialog.destroy()
        
    def try_pkexec_write(self, content):
        """Try to write file using pkexec"""
        try:
            # Create temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.conf') as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            
            # Use pkexec to copy the temporary file
            result = subprocess.run([
                'pkexec', 'cp', tmp_path, self.config_path
            ], capture_output=True, text=True)
            
            # Clean up
            os.unlink(tmp_path)
            
            return result.returncode == 0
        except Exception as e:
            print(f"pkexec write failed: {e}")
            return False
            
    def try_pkexec_copy(self, source, dest):
        """Try to copy file using pkexec"""
        try:
            result = subprocess.run([
                'pkexec', 'cp', source, dest
            ], capture_output=True, text=True)
            
            return result.returncode == 0
        except Exception as e:
            print(f"pkexec copy failed: {e}")
            return False

    def on_settings_clicked(self, button):
        """Show settings dialog"""
        dialog = SettingsDialog(self)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            # Apply settings
            dialog.apply_settings()
            self.save_app_settings()
            self.load_backgrounds()
            
        dialog.destroy()
        
    def on_about_clicked(self, button):
        """Show about dialog"""
        about = Gtk.AboutDialog()
        about.set_transient_for(self)
        about.set_modal(True)
        about.set_program_name('SDDM Background Changer')
        about.set_version('2.0.0')
        about.set_comments('Una aplicación moderna para cambiar el fondo de SDDM')
        about.set_website('https://github.com/rhythmcreative/bg-sddm')
        about.set_website_label('GitHub')
        about.set_authors(['RhythmCreative'])
        about.set_copyright('Copyright © 2024 RhythmCreative')
        about.set_license_type(Gtk.License.MIT_X11)
        
        # Set icon (if available)
        try:
            about.set_logo_icon_name('preferences-desktop-wallpaper')
        except:
            pass
        
        about.run()
        about.destroy()
        
    def on_destroy(self, widget):
        """Handle window close"""
        self.save_app_settings()
        Gtk.main_quit()

class SettingsDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title='Configuración', parent=parent, modal=True)
        self.set_default_size(400, 300)
        self.set_resizable(False)
        
        self.parent = parent
        
        # Add buttons
        self.add_button('Cancelar', Gtk.ResponseType.CANCEL)
        self.add_button('Aplicar', Gtk.ResponseType.OK)
        
        # Content area
        content = self.get_content_area()
        content.set_spacing(12)
        content.set_margin_top(12)
        content.set_margin_bottom(12)
        content.set_margin_start(12)
        content.set_margin_end(12)
        
        # Grid columns setting
        grid_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        grid_label = Gtk.Label('Columnas en la cuadrícula:')
        grid_label.set_halign(Gtk.Align.START)
        
        self.grid_spin = Gtk.SpinButton()
        self.grid_spin.set_range(2, 8)
        self.grid_spin.set_increments(1, 1)
        self.grid_spin.set_value(parent.settings.get('grid_columns', 4))
        
        grid_box.pack_start(grid_label, False, False, 0)
        grid_box.pack_end(self.grid_spin, False, False, 0)
        content.pack_start(grid_box, False, False, 0)
        
        # Preview size setting
        size_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        size_label = Gtk.Label('Tamaño de vista previa:')
        size_label.set_halign(Gtk.Align.START)
        
        self.size_spin = Gtk.SpinButton()
        self.size_spin.set_range(80, 300)
        self.size_spin.set_increments(10, 20)
        self.size_spin.set_value(parent.settings.get('preview_size', 160))
        
        size_box.pack_start(size_label, False, False, 0)
        size_box.pack_end(self.size_spin, False, False, 0)
        content.pack_start(size_box, False, False, 0)
        
        # Theme path setting
        theme_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        theme_label = Gtk.Label('Ruta del tema SDDM:')
        theme_label.set_halign(Gtk.Align.START)
        
        self.theme_entry = Gtk.Entry()
        self.theme_entry.set_text(parent.theme_path)
        
        theme_button = Gtk.Button('Seleccionar...')
        theme_button.connect('clicked', self.on_select_theme_path)
        
        theme_path_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        theme_path_box.pack_start(self.theme_entry, True, True, 0)
        theme_path_box.pack_start(theme_button, False, False, 0)
        
        theme_box.pack_start(theme_label, False, False, 0)
        theme_box.pack_start(theme_path_box, False, False, 0)
        content.pack_start(theme_box, False, False, 0)
        
        self.show_all()
        
    def on_select_theme_path(self, button):
        """Select theme path"""
        dialog = Gtk.FileChooserDialog(
            title='Seleccionar directorio del tema',
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER
        )
        
        dialog.add_button('Cancelar', Gtk.ResponseType.CANCEL)
        dialog.add_button('Seleccionar', Gtk.ResponseType.OK)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            if path:
                self.theme_entry.set_text(path)
                
        dialog.destroy()
        
    def apply_settings(self):
        """Apply the settings"""
        self.parent.settings['grid_columns'] = int(self.grid_spin.get_value())
        self.parent.settings['preview_size'] = int(self.size_spin.get_value())
        
        # Update theme path if changed
        new_theme_path = self.theme_entry.get_text()
        if new_theme_path != self.parent.theme_path:
            self.parent.theme_path = new_theme_path
            self.parent.backgrounds_path = f'{new_theme_path}/Backgrounds'
            self.parent.config_path = f'{new_theme_path}/Themes/theme1.conf'
            self.parent.settings['last_used_theme'] = new_theme_path
        
        # Update flow box
        self.parent.flow_box.set_max_children_per_line(self.parent.settings['grid_columns'])

def main():
    """Main function to run the application"""
    # Initialize GTK
    Gtk.init()
    
    app = SDDMBackgroundChanger()
    return app.run()

def check_environment():
    """Check if the environment is suitable for running the GUI application"""
    if os.environ.get('DISPLAY') is None:
        print("Warning: DISPLAY environment variable is not set.")
        print("You might need to run this in a graphical environment.")
        return False
    return True

if __name__ == '__main__':
    if not check_environment():
        print("Environment check failed. Trying to continue anyway...")
    
    exit_code = main()
    sys.exit(exit_code)

