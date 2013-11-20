#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from os.path import expanduser
import keybinder
from subprocess import call
from time import sleep, time
import requests
import sys


class PuutClient:
	

	def hotkeyFired(self, data=None):
		self.timestamp = str(time()).split(".")[0]
		self.cmd = "scrot /tmp/puut-"+self.timestamp+".png " + self.config["params"][data]
		sleep(0.2) #wait for keyboard to be available again
		call(self.cmd.split())
		sleep(0.2) #wait for image to be saved
		self.upload_file()
		clipboard = gtk.clipboard_get()
		clipboard.set_text(self.imagePath)
		clipboard.store()
		call(["notify-send", "Puut: Image uploaded", self.imagePath + "\nLink was copied into clipboard"])
		

	def upload_file(self):
		image = {"image": (open("/tmp/puut-"+self.timestamp+".png","rb"))}
		headers = {'accept': 'application/json'}
		r = requests.post(self.config["serverAddress"]+"/upload", auth=(self.config["user"],self.config["password"]),files=image,headers=headers)
		print(r.text)
		self.imagePath = self.config["serverAddress"]+"/" + r.text.split(":")[1].split("\"")[1] + ".png"

	def right_click_event(self, icon, button, time):
		menu = gtk.Menu()
		about = gtk.MenuItem("About")
		settings = gtk.MenuItem("Settings")
		quit = gtk.MenuItem("Quit")
        
		about.connect("activate", self.show_about_dialog)
		quit.connect("activate", gtk.main_quit)
		settings.connect("activate", self.openSettings)
        
		menu.append(settings)
		menu.append(about)
		menu.append(quit)
        
		menu.show_all()
        
		menu.popup(None, None, gtk.status_icon_position_menu, button, time, self.statusicon)

	def openSettings(self, widget):
		call(["gedit",self.configFile])

	def setupPuut(self):
		if not os.path.exists("~/.puut"):
    			os.makedirs("~/.puut")
		self.cnfFile = open(self.configFile, 'a')
		self.cnfFile.write("#This is the puut config file\n\n#The puut server address:\nserverAddress = \"http://add.server.here:port\"\n\n#your puut credentials:\nuser = \"username\"\npassword = \"123456\"\n")
		self.cnfFile.write("#Keybindings:\n#You can create new keybindings by adding them to the array and then adding the command parameters\n")	
		self.cnfFile.write("keys = [\"<Ctrl><Shift>1\",\"<Ctrl><Shift>2\",\"<Ctrl><Shift>3\"]\nparams = [\"--multidisp\",\"--focused\",\"--select\"]\n")	

	def show_about_dialog(self, widget):
		#Sows a simple about dialog
		about_dialog = gtk.AboutDialog()

		about_dialog.set_destroy_with_parent(True)
		about_dialog.set_name("Puut Linux Client")
		about_dialog.set_version("0.2 beta")
		about_dialog.set_authors(["Ole Wehrmeyer"])
        		
		about_dialog.run()
		about_dialog.destroy()

	def delete_event(self, widget, event, data=None):
		return False

	def destroy(self, widget, data=None):
		gtk.main_quit()

	def __init__(self):
		#try loading the config file
		# if it doesn't exist, create one
		try:
			self.configFile = expanduser("~") + "/.puut/puut.conf"
			#load configuration
			self.config = {}
			exec(open(self.configFile).read(),self.config)
		except IOError:
			self.setupPuut()
			call(["notify-send", "Puut: Setup config", "Setup your user data at '~/.puut/puut.conf'"])
			sys.exit(1)

		#testing if server & credentials are correct
		r = requests.get(self.config["serverAddress"] + "/info", auth=(self.config["user"],self.config["password"]))
		if not (r.text=="PUUT"):
			call(["notify-send", "Puut: Server error", "Contacting the server was unsuccessful, are credentials and server correct?\nResponse was: "+ r.text])
			sys.exit(1)		
		
		#setting up keyhooks
		for self.idx, self.val in enumerate(self.config["keys"]):
			keybinder.bind(self.val, self.hotkeyFired, self.idx) 

		#setup GTK Status icon
		self.statusicon = gtk.StatusIcon()
		self.statusicon.set_from_file("icon.png") 
		self.statusicon.connect("popup-menu", self.right_click_event)
		self.statusicon.set_tooltip("StatusIcon Example")
		

	def main(self):
		gtk.main()

if __name__ == "__main__":
	client= PuutClient()
	client.main()
