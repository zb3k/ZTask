# -*- coding: utf-8 -*-

############################################################################

import sqlite3
import inspect
import sys
import os

############################################################################

class Database():
	def __init__(self):
		path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

		try:
			self.conn = sqlite3.connect(path + '/library.sqlite3')

			self.conn.row_factory = self.dict_factory

			self.cursor = self.conn.cursor()

		except sqlite3.Error, e:
			# DOTO: add die()
			print "Error %s:" % e.args[0]
			sys.exit(1)

	def __del__(self):
		print 'CLOSE'
		if self.conn:
			self.conn.close()

	def dict_factory(cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d

