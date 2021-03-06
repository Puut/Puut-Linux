Puut-Linux
==========

The Puut Client for Linux. It works with [python](http://www.python.org/) and has a GTK binding via [pygtk](http://www.pygtk.org/)
Puut is a service for sharing screenshots, like [puush](http://puush.me), but self-hosted, so you keep the screenshots in a safe place.

Installation
------------

There are a few dependecies for running `puut.py` successfully:

* `python` : obviously
* `pygtk` : for GTK binding
* `python-keybinder` : for creating system wide key hooks
* `python-requests` : for easy interaction with the server
* `xclip` : for copying link to clipboard
* `scrot` : for taking the screenshots
* `libnotify-bin` : for showing desktop notifications
* A [Puut server](https://github.com/Puut/Puut-Server)

You can install all dependencies by running
`sudo apt-get install python python-keybinder python-requests xclip scrot libnotify-bin`
in a terminal

Maybe you need to install `pygtk` manually

Configuration
-------------

There sometimes is a weird error that the script is unable to create the config file, if so, paste this into `~/.puut/puut.conf`:

	
	#This is the puut config file

	#The puut server address:
	serverAddress = "http://add.server.here:port"

	#your puut credentials:
	user = "username"
	password = "123456"
	#Keybindings:
	#You can create new keybindings by adding them to the array and then adding the command parameters
	keys = ["<Ctrl>1","<Ctrl>2","<Ctrl>3"]
	params = ["--multidisp","--focused","--select"]

Run Puut Client for the first time by typing `python puut.py` in a terminal. It creates the neccesary configuration files for you. You should now see a blue arrow in your notification bar. Then open `~/.puut/puut.conf` in your favorite text editor (or right-click the icon and select `Settings` for opening it in `gedit`). The config file is python code and you have to enter the server name and user credentials as set up for your server.

Standard key bindings:
* `<Ctrl>1` : Full screenshot (even multi-monitor)
* `<Ctrl>2` : Just the active window
* `<Ctrl>3` : Select the area by clicking & dragging with the mouse


You can also edit the keybindings, by changing the `keys` and `params` array.
Each key has it's according `scrot` params in the `params` array at the same position.

There will be a GUI for configuration later

Usage
-----

Usage is pretty straight forward: Simply press the specified keys (see configuration) (and maybe select screen area) and the screenshot will be taken and uploaded to the server. You will see a notification indicating success and the link is also copied to your clipboard.

If you would like to use Puut frequently, you may want to add it to your list of startup applications. How to do this is very distro dependend, e.g in Ubuntu use `Startup Applications` to start Puut after user login. **Do not start Puut before user login, it won't work**

