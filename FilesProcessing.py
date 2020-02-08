#! /usr/bin/python
# coding: utf-8

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, qDebug, QDateTime, QProcess
from os import walk, rename, path, mkdir, remove, rmdir, startfile, listdir
from sys import argv,platform
from codecs import open


class FilesProcessing(QObject):
	"""build list folders name, search youtube and download first video find format mp4."""
						
	def __init__(self, parent=None):
		"""Init."""
		super(FilesProcessing, self).__init__(parent)
		self.parent = parent
		self.blacklist = ['desktop.ini', 'Thumbs.db']
		self.listfolders = None
		self.listfiles = None
		self.sizefoler = None

	def folder_list_files(self, Cpath, boolsubfolders=True, masks=None, exact=None):
		"""Build files list."""
		self.listfiles = []
		for folderName, subfolders, filenames in walk(Cpath):
			if subfolders and subfolders:
				for subfolder in subfolders:
					self.folder_list_files(subfolder, boolsubfolders, masks, exact)
			for filename in filenames:
				if masks is None:
					# no mask
					if filename not in self.blacklist:
						self.listfiles.append(path.join(folderName, filename))
				else:
					# same
					if exact:
						if filename.lower() in masks:
							if filename not in self.blacklist:
									self.listfiles.append(path.join(folderName, filename))
					else:
						# mask joker *.
						for xmask in masks:
							if filename[-len(xmask):].lower() in xmask:
								if filename not in self.blacklist:
									self.listfiles.append(path.join(folderName, filename))
			if not boolsubfolders:
				break
		return self.listfiles

	def folder_list_folders(self, Cpath):
		"""Build folders list."""
		self.listfolders = [d for d in listdir(Cpath) if path.isdir(path.join(Cpath, d))]
		return self.listfolders

	def folder_size(self, Cpath,  boolsubfolders=True):
		"""Calcul folder size."""
		total_size = path.getsize(Cpath)
		for item in listdir(Cpath):
			itempath = path.join(Cpath, item)
			if path.isfile(itempath):
				total_size += path.getsize(itempath)
			elif path.isdir(itempath) and boolsubfolders:
				total_size += self.folder_size(itempath)
		return total_size

	def open_folder(self, Cpath):
		"""Open File Explorer."""
		if platform == "win32":
			self.execute_command('explorer', Cpath)
		elif platform == "darwin":
			self.execute_command('open', Cpath)
		elif platform == 'linux':
			self.execute_command('xdg-open', Cpath)

	def open_file(self, file):
		"""Open programme association with file."""
		startfile(file)

	def execute_command(self, prog, *argv):
		"""Execut a program no wait, no link."""
		argums = []
		for arg in argv:
			argums += (arg,)
		p = QProcess()
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
		myfolder = r"D:\WorkDev\DBAlbumsTEST\TECHNO\Download"
	# class
	BuildProcess = FilesProcessing()
	#listfolders = BuildProcess.folder_list_folders(myfolder)
	#variable CLASS BuildProcess.listfolders
	#listfiles = BuildProcess.folder_list_files(myfolder, False)
	#variable CLASS BuildProcess.listfiles
	#listfiles = BuildProcess.folder_list_files(myfolder)
	#foldersize = BuildProcess.folder_size(myfolder)
	#BuildProcess.open_folder(myfolder)
	#BuildProcess.open_file(r'D:\WorkDev\DBAlbumsTEST\TECHNO\Download\Nouveau document RTF.nfo')
	


