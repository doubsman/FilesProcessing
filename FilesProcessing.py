#! /usr/bin/python
# coding: utf-8

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, qDebug, QDateTime
from os import walk, rename, path, mkdir, remove, rmdir, startfile
from sys import argv
from codecs import open


class FilesProcessing(QObject):
	"""build list folders name, search youtube and download first video find format mp4."""
						
	def __init__(self, parent=None):
		"""Init."""
		super(FilesProcessing, self).__init__(parent)
		self.parent = parent

	def folder_list_files(self, Cpath, masks=None, nosub=True, exact=None):
		"""Build files list."""
		blacklist = ['desktop.ini', 'Thumbs.db']
		for folderName, subfolders, filenames in walk(Cpath):
			if subfolders and nosub:
				for subfolder in subfolders:
					self.folder_list_files(subfolder, masks, exact)
			for filename in filenames:
				if masks is None:
					# no mask
					if filename not in blacklist:
						yield path.join(folderName, filename)
				else:
					# same
					if exact:
						if filename.lower() in masks:
							if filename not in blacklist:
									yield path.join(folderName, filename)
					else:
						# mask joker
						for xmask in masks:
							if filename[-len(xmask):].lower() in xmask:
								if filename not in blacklist:
									yield path.join(folderName, filename)

	def folder_list_folders(self, Cpath):
		"""Build folders list."""
		return [d for d in listdir(Cpath) if path.isdir(path.join(Cpath, d))]

	def folder_size(self, Cpath):
		"""Calcul folder size."""
		total_size = path.getsize(Cpath)
		for item in listdir(folder):
			itempath = path.join(Cpath, item)
			if path.isfile(itempath):
				total_size += path.getsize(itempath)
			elif path.isdir(itempath):
				total_size += getFolderSize(itempath)
		return total_size

	def build_command_powershell(self, script, *argv):
		"""Build command PowerShell."""
		command = [r'-ExecutionPolicy', 'Unrestricted',
					'-WindowStyle', 'Hidden',
					'-File',
					script]
		for arg in argv:
			command += (arg,)
		return 'powershell.exe', command

	def open_folder(self, Cpath):
		"""Open File Explorer."""
		if platform == "win32":
			self.execute_command('explorer', Cpath)
		elif platform == "darwin":
			self.execute_command('open', Cpath)
		elif platform == 'linux':
			self.execute_command('xdg-open', Cpath)

	def execute_command(self, prog, *argv):
		"""Execut a program no wait, no link."""
		argums = []
		for arg in argv:
			argums += (arg,)
		p = QProcess()
		# print(prog, argums)
		p.startDetached(prog, argums)

	def convertUNC(self, Cpath):
		""" convert path UNC to linux."""
		# open file unc from Linux (mount \HOMERSTATION\_lossLess)
		if (platform == "darwin" or platform == 'linux') and path.startswith(r'\\'):
			Cpath = r""+Cpath.replace('\\\\', '/').replace('\\', '/')
		return Cpath

if __name__ == '__main__':
	app = QApplication(argv)
	if len(argv)>1:
		# prod
		myfolder = argv[1]
	else:
		# test envt
		myfolder = "T:\\work\\Fila Brazillia NT\\\Compilations"
	# class
	BuildProcess = FilesProcessing()

