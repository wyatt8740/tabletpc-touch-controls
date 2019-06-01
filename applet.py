#! /bin/env python3
import gi
import subprocess # to execute appropriate scripts/programs
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject

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
        button.set_tooltip_text("Window Switcher")
        button.connect("clicked", self.winList)
        vbox.pack_start(button, True, True, 0)
        
        button=Gtk.Button()
        img=Gtk.Image.new_from_file('icons/keyboard_'+btnsize+'.png')
        button.add(img)
        button.set_tooltip_text("Toggle on-screen keyboard")
        button.connect("clicked", self.toggleKeybd)
        vbox.pack_start(button, True, True, 0)

#       touch digitizer on/off
        button=Gtk.Button()
        img=Gtk.Image.new_from_file('icons/touch_'+btnsize+'.png')
        button.add(img)
        button.set_tooltip_text("Turn touch digitizer on and off")
        button.connect("clicked", self.toggleTouch)
        vbox.pack_start(button, True, True, 0)

#       unclutter on/off
        button=Gtk.Button()
        img=Gtk.Image.new_from_file('icons/unclutter_'+btnsize+'.png')
        button.add(img)
        button.set_tooltip_text("Turn 'unclutter' on and off")
        button.connect("clicked", self.toggleUnclutter)
        vbox.pack_start(button, True, True, 0)

#       brightness down
        button=Gtk.Button()
        img=Gtk.Image.new_from_file('icons/brightness-down_'+btnsize+'.png')
        button.add(img)
        button.set_tooltip_text("Lower brightness")
        button.connect("clicked", self.brtDown)
        vbox.pack_start(button, True, True, 0)

#       brightness up
        button=Gtk.Button()
        img=Gtk.Image.new_from_file('icons/brightness-up_'+btnsize+'.png')
        button.add(img)
        button.set_tooltip_text("Raise brightness")
        button.connect("clicked", self.brtUp)
        vbox.pack_start(button, True, True, 0)
        
##       automatically calibrate
#        button=Gtk.Button()
#        img=Gtk.Image.new_from_file('icons/calibreset_'+btnsize+'.png')
#        button.add(img)
#        button.set_tooltip_text("Automatically fix digitizer calibration")
#        button.connect("clicked", self.calib)
#        vbox.pack_start(button, True, True, 0)

#       calibrate
        button=HoldButton()
        img=Gtk.Image.new_from_file('icons/calib_'+btnsize+'.png')
        button.add(img)
        button.set_tooltip_text("Fix digitizer calibration")
        button.connect("clicked", self.calib)
#        button.connect("held", self.calibManual)
        button.connect("held", self.spawnCalibMenu)
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

    def calib(self, widget):
        subprocess.run("calib")

    def calibManual(self, widget):
        subprocess.run("wacomCalib1")

    def spawnCalibMenu(self, widget):
        winCalib.show_all()
        
class HoldButton(Gtk.Button):

    __gsignals__ = { 'held' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ()) }

    def __init__(self, label=None, stock=None, use_underline=True):
        Gtk.Button.__init__(self, label, stock, use_underline)
        self.connect('pressed', HoldButton.h_pressed)
        self.connect('clicked', HoldButton.h_clicked)
        self.timeout_id = None

    def h_clicked(self):
        if self.timeout_id:
            GObject.source_remove(self.timeout_id)
            self.timeout_id = None
        else:
            self.stop_emission('clicked')

    def h_pressed(self):
        self.timeout_id = GObject.timeout_add(750, HoldButton.h_timeout, self)

    def h_timeout(self):
        self.timeout_id = None
        self.emit('held')
#        print("HELD BUTTON DOWN")
        return False

class TabletApplet_CalibMenu(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Calibration")
        self.set_wmclass(APP_NAME,APP_NAME)

#        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(vbox)

        button=Gtk.Button(label=" ✖ ")
        button.connect("clicked", self.closeCalibMenu)
        vbox.pack_start(button, True, True, 0)

#       automatically calibrate
        button=Gtk.Button()
        img=Gtk.Image.new_from_file('icons/calibreset_'+btnsize+'.png')
        button.add(img)
        button.set_tooltip_text("Automatically fix digitizer calibration with preset values")
        button.connect("clicked", self.calib)
        vbox.pack_start(button, True, True, 0)

#       calibrate
        button=Gtk.Button()
        img=Gtk.Image.new_from_file('icons/calib_'+btnsize+'.png')
        button.add(img)
        button.set_tooltip_text("Fix digitizer stylus calibration")
        button.connect("clicked", self.calibManual)
        vbox.pack_start(button, True, True, 0)

#       calibrate touch
        button=Gtk.Button()
        img=Gtk.Image.new_from_file('icons/calibtouch_'+btnsize+'.png')
        button.add(img)
        button.set_tooltip_text("Fix digitizer calibration for touch")
        button.connect("clicked", self.calibManualTouch)
        vbox.pack_start(button, True, True, 0)

    def calib(self, widget):
        subprocess.run("calib")

    def calibManual(self, widget):
        subprocess.run("wacomCalibStylus")

    def calibManualTouch(self, widget):
        subprocess.run("wacomCalibTouch")

    def closeCalibMenu(self, widget):
        self.hide()
    
win=TabletApplet()
win.connect("destroy", Gtk.main_quit)
winCalib=TabletApplet_CalibMenu()
winCalib.connect("destroy", winCalib.closeCalibMenu)
scr=Gdk.Display.get_default().get_default_screen()
# very wm specific hardcoded geometry stuff here
win.move(0, scr.get_height() - (win.get_size().height) / 2 + 40)
#print(scr.get_height())
#print(win.get_scale_factor())
win.show_all()
Gtk.main()
