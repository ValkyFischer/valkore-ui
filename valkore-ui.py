import json
import logging
import os
import webbrowser
from urllib.request import urlopen

import tools

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from modules.logger.logger import Logger, UiLogger
from modules.config.config import Config


# User Interface
class CONFIGui(tk.Frame):
	def __init__(self, master=None, config=None):
		super().__init__(master)
		self.pack()

		self.cfg = config
		self.modules = tools.loadModules()

		lookup = urlopen("https://valky.dev/api/valkore/")
		self.whitelist = json.loads(lookup.read())

		self.tabControl = ttk.Notebook(self.master)
		self.tab1 = ttk.Frame(self.tabControl)  # Logs
		self.tab2 = ttk.Frame(self.tabControl)  # My Modules
		self.tab3 = ttk.Frame(self.tabControl)  # Get Modules
		self.tab4 = ttk.Frame(self.tabControl)  # Settings
		self.tab99 = ttk.Frame(self.tabControl)  # About

		self.icon_world = tk.PhotoImage(file='modules/valkore-ui/data/world.png')
		self.icon_start = tk.PhotoImage(file='modules/valkore-ui/data/start.png')
		self.icon_download = tk.PhotoImage(file='modules/valkore-ui/data/download.png')

		# Labelframe - Logs
		self.lfLogs = tk.LabelFrame(self.tab1, text="Console Logs")
		self.lfLogs.pack(fill="both", expand="yes", padx=5, pady=5)
		# Labelframe - Modules
		self.lfModules = tk.LabelFrame(self.tab2, text="My Valkore Modules")
		self.lfModules.pack(fill="both", expand="yes", padx=5, pady=5)
		# Labelframe - Get Modules
		self.lfGetModules = tk.LabelFrame(self.tab3, text="Get More Valkore Modules")
		self.lfGetModules.pack(fill="both", expand="yes", padx=5, pady=5)
		# Labelframe - Settings
		self.lfSettings = tk.LabelFrame(self.tab4, text="Valkore Settings")
		self.lfSettings.pack(fill="both", expand="yes", padx=5, pady=5)
		# Labelframe - About
		self.lfAbout = tk.LabelFrame(self.tab99, text=f"{self.cfg['VKore']['name']} | v{self.cfg['VKore']['version']} | ..a project by VALKYTEQ")
		self.lfAbout.pack(fill="both", expand="yes", padx=5, pady=5)

		# Head Image
		self.headImage()

		# Build Tabs and Fill Content
		self.tabs()
		self.tabAbout()
		self.tabLogs()
		self.tabModules()
		self.tabGetModules()
		self.tabSettings()

		# initialize ui logger
		self.log = Logger(path="modules/logger/config.ini", name="valkore-load", widget=self.log_widget)
		self.logy = None


	def headImage(self):
		self._logoPath = tk.PhotoImage(file="modules/valkore-ui/data/long.png")
		self._logoLabel = tk.Label(self)
		self._logoLabel["image"] = self._logoPath
		self._logoLabel.grid(row=0)

	def tabs(self):
		self.tabControl.add(self.tab1, text='Logs')
		self.tabControl.add(self.tab2, text='My Modules')
		self.tabControl.add(self.tab3, text='Get More Modules')
		self.tabControl.add(self.tab4, text='Settings')
		self.tabControl.add(self.tab99, text='About')
		self.tabControl.pack(expand=1, fill="both")

	# Tab 99 - About
	def tabAbout(self):
		self._rootPath = tk.Label(self.lfAbout)
		self._rootPath["text"] = "\nDESCRIPTION:\n" + self.cfg['VKore']['description'] + "\n" + \
									  "\nVERSION:\n" + self.cfg['VKore']['version'] + "\n" + \
									  "\nAUTHOR:\n" + self.cfg['VKore']['author'] + "\n"
		self._rootPath["width"] = 100
		self._rootPath.grid(row=5)

		self._logoPathAbout = tk.PhotoImage(file="modules/valkore-ui/data/projects.png")
		self._logoLabelAbout = tk.Label(self.lfAbout)
		self._logoLabelAbout["image"] = self._logoPathAbout
		self._logoLabelAbout.grid(row=10)

		self._rootPathTitle = tk.Label(self.lfAbout)
		self._rootPathTitle["text"] = "\nCONTACT:\nhttps://valky.dev/\nhttps://valkyteq.com/\n"
		self._rootPathTitle["width"] = 100
		self._rootPathTitle.grid(row=15)

	def tabLogs(self):
		self.log_widget = ScrolledText(self.lfLogs, height=25, width=100, font=("consolas", "10", "normal"))
		self.log_widget.pack()

	def tabModules(self):
		# go through all modules
		if len(self.modules) > 0:
			i = 1
			for module, cfg in self.modules.items():

				vers = tk.Label(self.lfModules, text=f"{cfg['VKore']['name']}", width=20, anchor="w")
				vers.grid(row=i, column=1)

				vers = tk.Label(self.lfModules, text=f"v{cfg['VKore']['version']}", width=10, anchor="w")
				vers.grid(row=i, column=2)

				desc = tk.Label(self.lfModules, text=f"{cfg['VKore']['description']}", width=60, anchor="w")
				desc.grid(row=i, column=3)

				button = ttk.Button(self.lfModules, image=self.icon_world, command=lambda s=module: self.showModule(s))
				button.grid(row=i, column=4)

				if 'interface' in cfg['VKore'] and cfg['VKore']['interface'] is True:
					button = ttk.Button(self.lfModules, image=self.icon_start, command=lambda s=module: self.startModule(s))
					button.grid(row=i, column=5)

				i = i + 1

	def tabGetModules(self):
		if len(self.whitelist) > 0:
			i = 1
			for module, info in self.whitelist.items():

				vers = tk.Label(self.lfGetModules, text=f"{info['name']}", width=20, anchor="w")
				vers.grid(row=i, column=1)

				vers = tk.Label(self.lfGetModules, text=f"v{info['version']}", width=10, anchor="w")
				vers.grid(row=i, column=2)

				desc = tk.Label(self.lfGetModules, text=f"{info['description']}", width=60, anchor="w")
				desc.grid(row=i, column=3)

				button = ttk.Button(self.lfGetModules, image=self.icon_world, command=lambda s=module: self.showModule(s))
				button.grid(row=i, column=4)

				if not os.path.isdir(f"./modules/{module}"):
					button = ttk.Button(self.lfGetModules, image=self.icon_download, command=lambda s=module: self.getModule(s))
					button.grid(row=i, column=5)

				i = i + 1


	def tabSettings(self):
		pass

	def sendLog(self, log: str|tuple):
		if self.logy is None:
			log_handler = UiLogger(self.log_widget)
			self.logy = logging.getLogger("valkore-ui")
			self.logy.addHandler(log_handler)
		self.logy.info(log)

	def getLogWidget(self):
		return self.log_widget

	def showModule(self, m):
		self.sendLog(f"'{m}' Show Web")
		webbrowser.open(self.whitelist[m]['link'][:-4])

	def startModule(self, m):
		self.sendLog(f"'{m}' Start")
		tools.runModule(modlue=m, logger=self.logy)

	def refreshModules(self):
		self.modules = None
		self.modules = tools.loadModules()
		self.tabModules()

	def getModule(self, module):
		self.sendLog(f"'{module}' Download")
		tools.getModule(module=module, logger=self.logy, whitelist=self.whitelist)
		self.refreshModules()

		self.logy.info(f"{module}: Checking for dependencies")
		if tools.getDependency(self.modules[module], module, self.logy):
			self.logy.info(f"{module}: Dependencies up to date")
		else:
			self.logy.info(f"{module}: Error in dependencies!")


def load():

	root = tk.Tk()

	cfg = Config(path="modules/valkore-ui/config.ini").readConfig()
	root.iconbitmap('modules/valkore-ui/data/valkore.ico')
	root.title(f"{cfg['VKore']['name']} | v{cfg['VKore']['version']} | ..a project by VALKYTEQ")
	root.resizable(False, False)

	return CONFIGui(master=root, config=cfg)
