#! /bin/env python3
import gi
import subprocess # to execute appropriate scripts/programs
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

btnsize="32" # change this to change the size of button icons.

APP_NAME="TabletPC_Applet_Menu"

class TabletApplet(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Tablet Controls")
        self.set_wmclass(APP_NAME,APP_NAME)

#        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(vbox)

#        button=Gtk.Button(label="Window Switcher")
        button=Gtk.Button()
        img=Gtk.Image.new_from_file('icons/winswitch_'+btnsize+'.png')
        button.add(img)
        button.connect("clicked", self.winList)
        vbox.pack_start(button, True, True, 0)
        
        button=Gtk.Button(label="\nKeyboard\n")
        button.connect("clicked", self.toggleKeybd)
        vbox.pack_start(button, True, True, 0)

#       touch digitizer on/off
        button=Gtk.Button(label="\nTouch\n")
        button.connect("clicked", self.toggleTouch)
        vbox.pack_start(button, True, True, 0)

#       unclutter on/off
        button=Gtk.Button(label="Unclutter")
        button.connect("clicked", self.toggleUnclutter)
        vbox.pack_start(button, True, True, 0)

#       brightness up
        button=Gtk.Button()
        img=Gtk.Image.new_from_file('icons/brightness-up_'+btnsize+'.png')
        button.add(img)
        button.connect("clicked", self.brtUp)
        vbox.pack_start(button, True, True, 0)

#       brightness down
        button=Gtk.Button()
        img=Gtk.Image.new_from_file('icons/brightness-down_'+btnsize+'.png')
        button.add(img)
        button.connect("clicked", self.brtDown)
        vbox.pack_start(button, True, True, 0)

#       calibrate
        button=Gtk.Button(label="\n Calibrate \n")
        button.connect("clicked", self.calib)
        vbox.pack_start(button, True, True, 0)

        button=Gtk.Button(label=" ✖ ")
        button.connect("clicked", Gtk.main_quit)
        vbox.pack_start(button, True, True, 0)
#        self.add(self.btnKeybd)
#        self.add(self.btnTouch)
#        self.add(self.btnExit)

    def toggleKeybd(self, widget):
        subprocess.run("osk-toggle")

    def toggleTouch(self, widget):
        subprocess.run("touchscreen-toggle")

    def winList(self, widget):
        subprocess.run(["FvwmCommand", "WindowList Root c c CurrentDesk"])

    def brtUp(self, widget):
        subprocess.run("brightup_acpi")

    def brtDown(self, widget):
        subprocess.run("brightdown_acpi")
        
    def toggleUnclutter(self, widget):
        subprocess.run("uc-toggle")

    def calib():
        subprocess.run("calib")

win=TabletApplet()
win.connect("destroy", Gtk.main_quit)
scr=Gdk.Display.get_default().get_default_screen()
# very wm specific hardcoded geometry stuff here
win.move(0, scr.get_height() - (win.get_size().height) / 2 + 32)
#print(scr.get_height())
#print(win.get_scale_factor())
win.show_all()
Gtk.main()
