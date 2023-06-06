#!/usr/bin/python

# Appindicator para controlar el brillo de los dispositivos DDA
# Basado en la aplicacion indicator-brightness de Erwin Rohde
#
# Copyright (c) 2014 Luis Sanchez Bejarano
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>

import gobject
import gtk
import appindicator
import subprocess
import re
#import dbus
#import dbus.service
#from dbus.mainloop.glib import DBusGMainLoop

#Granularidad del controlador
grad = 10

iconos = {
	10: "/usr/share/notify-osd/icons/gedu/status/notification-display-brightness-full-dark.png",
	9: "/usr/share/notify-osd/icons/gedu/status/notification-display-brightness-full-dark.png",
	8: "/usr/share/notify-osd/icons/gedu/status/notification-display-brightness-high-dark.png",
	7: "/usr/share/notify-osd/icons/gedu/status/notification-display-brightness-high-dark.png",
	6: "/usr/share/notify-osd/icons/gedu/status/notification-display-brightness-medium-dark.png",
	5: "/usr/share/notify-osd/icons/gedu/status/notification-display-brightness-medium-dark.png",
	4: "/usr/share/notify-osd/icons/gedu/status/notification-display-brightness-low-dark.png",
	3: "/usr/share/notify-osd/icons/gedu/status/notification-display-brightness-low-dark.png",
	2: "/usr/share/notify-osd/icons/gedu/status/notification-display-brightness-off-dark.png",
	1: "/usr/share/notify-osd/icons/gedu/status/notification-display-brightness-off-dark.png",
	0: "/usr/share/notify-osd/icons/gedu/status/notification-gpm-brightness-lcd-invalid.png",
}

#class DBusObject(dbus.service.Object):

	#@dbus.service.method(dbus_interface='com.ubuntu.indicator.brightness', in_signature='', out_signature='')
	#def bajar_brillo(self):
		#bajar_brillo()

	#@dbus.service.method(dbus_interface='com.ubuntu.indicator.brightness', in_signature='', out_signature='')
	#def subir_brillo(self):
		#subir_brillo()

def update_brightness_indicator():
	crear_indicador_brillo(ind)

def restaurar_brillo_cero():
	brillo_actual = obtener_brillo_actual()
	if brillo_actual == 0:
		ajustar_brillo("1")

def obtener_brillo_actual():
    with open('/sys/class/backlight/intel_backlight/brightness', 'r') as archivo:
        brillo_actual = int(archivo.read())
    return brillo_actual

def obtener_max_brillo():
    with open('/sys/class/backlight/intel_backlight/max_brightness', 'r') as archivo:
        max_brillo = int(archivo.read())
    return max_brillo

def subir_brillo(porcentaje):
    brillo_actual = obtener_brillo_actual()
    max_brillo = obtener_max_brillo()
    nuevo_brillo = min(brillo_actual + int(max_brillo * porcentaje / 100), max_brillo)
    ajustar_brillo(nuevo_brillo)

def bajar_brillo(porcentaje):
    brillo_actual = obtener_brillo_actual()
    nuevo_brillo = max(brillo_actual - int(brillo_actual * porcentaje / 100), 0)
    ajustar_brillo(nuevo_brillo)

def ajustar_brillo(porcentaje):
    max_brillo = obtener_max_brillo()
    nuevo_brillo = int(max_brillo * porcentaje / 100)
    nuevo_brillo = min(max(nuevo_brillo, 0), max_brillo)
    with open('/sys/class/backlight/intel_backlight/brightness', 'w') as archivo:
        archivo.write(str(nuevo_brillo))

def menu_item_response(mi, var):
	print "LLAMADA A EJECUTAR"
	val = re.sub('[^\d]', '', var)
	ajustar_brillo(val)

def crear_indicador_brillo(ind):
	menu = gtk.Menu()
	brillo_actual = obtener_brillo_actual()
	max_brillo = obtener_max_brillo()
	if max_brillo == 0:
		menu_items = gtk.MenuItem("Controlador no disponible")
		menu_items.set_sensitive(False)
		ind.set_icon("/usr/share/notify-osd/icons/gnome/scalable/status/notification-gpm-brightness-lcd-invalid.svg")
		menu.append(menu_items)
		menu_items.show()
	else:
		for i in range(grad, 0, -1):
			item = "%d" % i
			if i == brillo_actual:
				item = u"%d \u2022" % i
				ind.set_icon(iconos[i])
			menu_items = gtk.MenuItem(item)
			menu.append(menu_items)
			menu_items.connect("activate", menu_item_response, item)
			menu_items.show()

	ind.set_menu(menu)

def scroll_wheel_icon(mi, m, event):
	if int(event) == int(gtk.gdk.SCROLL_DOWN):
		bajar_brillo()
	elif int(event) == int(gtk.gdk.SCROLL_UP):
		subir_brillo()

##
# Bloque principal del indicator
#

ind = appindicator.Indicator ("indicator-brightness", iconos[obtener_brillo_actual()], appindicator.CATEGORY_HARDWARE)
ind.set_status (appindicator.STATUS_ACTIVE)
ind.set_label("Brillo")
ind.connect("scroll-event", scroll_wheel_icon)
restaurar_brillo_cero()

if __name__ == "__main__":
	crear_indicador_brillo(ind)
	
	# Arrancar servicio DBus, esperando senales de subida y bajada de brillo
	#dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	#session_bus = dbus.SessionBus()
	#name = dbus.service.BusName("com.ubuntu.indicator.brightness", session_bus)
	#object = DBusObject(session_bus, "/adjust")

	# Atender las subidas y bajadas de brillo con las teclas para actualizar el indicador
	#session_bus.add_signal_receiver(update_brightness_indicator, dbus_interface = "org.gnome.SettingsDaemon.Power.Screen", signal_name = "Changed")

	
	gtk.main()
