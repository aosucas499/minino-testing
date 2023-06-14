#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import gtk
import appindicator

APPINDICATOR_ID = 'brightness_app_indicator'

def set_brightness(value):
    backlight_dir = '/sys/class/backlight/'

    # Obtener la lista de carpetas en /sys/class/backlight
    backlight_folders = os.listdir(backlight_dir)

    # Buscar la carpeta de brillo válida
    valid_folder = None
    for folder in backlight_folders:
        brightness_file = os.path.join(backlight_dir, folder, 'brightness')
        if os.path.exists(brightness_file):
            valid_folder = folder
            break

    # Verificar si se encontró una carpeta válida
    if valid_folder is None:
        print("No se encontró una carpeta de brillo válida.")
        return

    # Construir la ruta completa al archivo de brillo
    brightness_path = os.path.join(backlight_dir, valid_folder, 'brightness')
    max_brightness_path = os.path.join(backlight_dir, valid_folder, 'max_brightness')

    # Leer el valor máximo de brillo
    with open(max_brightness_path, 'r') as file:
        max_brightness = int(file.read())

    # Calcular el nuevo valor de brillo basado en el porcentaje proporcionado
    new_brightness = int(max_brightness * value / 100)

    # Asegurarse de que el valor de brillo esté dentro del rango válido
    new_brightness = max(1, min(new_brightness, max_brightness))

    # Escribir el nuevo valor de brillo
    with open(brightness_path, 'w') as file:
        file.write(str(new_brightness))

def on_menu_item_activate(menu_item, value):
    set_brightness(value)

def build_menu():
    menu = gtk.Menu()

    # Crea las opciones de ajuste de brillo
    for percent in range(10, 101, 10):
        menu_item = gtk.MenuItem(label='{0}%'.format(percent))
        menu_item.connect('activate', on_menu_item_activate, percent)
        menu.append(menu_item)

    # Agrega una opción de salida
    menu_item_quit = gtk.MenuItem(label='Salir')
    menu_item_quit.connect('activate', gtk.main_quit)
    menu.append(menu_item_quit)

    menu.show_all()
    return menu

def main():
    # Crea el indicador de la aplicación
    indicator = appindicator.Indicator(
        APPINDICATOR_ID,
        os.path.abspath('/usr/share/notify-osd/icons/gedu/status/notification-display-brightness-full-dark.png'),
        appindicator.CATEGORY_APPLICATION_STATUS
    )
    indicator.set_status(appindicator.STATUS_ACTIVE)
    indicator.set_menu(build_menu())

    gtk.main()

if __name__ == '__main__':
    main()

