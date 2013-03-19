# -*- coding: utf-8 -*-

############################################################################

import sqlite3
import inspect
import sys
import os

############################################################################

class Database():

	last_query = ''
	_query     = {}

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

		self.clear_query()

	############################################################################

	def __del__(self):
		if self.conn:
			self.conn.close()

	############################################################################

	def dict_factory(self, cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d

	############################################################################

	def clear_query(self):
		self._query = {
			'table':  '',
			'where':  '',
			'limit':  '',
			'values': {},
		}

	############################################################################

	def _build_query(self, qtype = 'select'):
		table = self._query['table']

		if qtype in ['select', 'update']:
			where = 'WHERE ' + self._query['where'] if self._query['where'] else ''

		if qtype is 'select':
			self.last_query = 'SELECT * FROM %s %s;' % (table, where)

		if qtype is 'insert':
			keys   = '`, `'.join([unicode(t) for t in self._query['values'].keys()])
			values = []
			for v in self._query['values'].values():
				values.append(unicode(v).replace('"',''))
			values = '", "'.join(values)
			self.last_query = 'INSERT INTO %s (`%s`) VALUES ("%s");' % (table, keys, values)

		if qtype is 'update':
			# keys   = '`, `'.join([unicode(t) for t in self._query['values'].keys()])
			values = []
			for k,v in self._query['values'].items():
				values.append( '`%s`="%s"' % (k, unicode(v).replace('"','')) )
			values = ', '.join(values)
			self.last_query = 'UPDATE %s SET %s %s;' % (table, values, where)



		self.clear_query()
		return self.last_query

	############################################################################

	def table(self, table):
		self._query['table'] = table
		return self

	def where(self, key, o, val):
		if self._query['where']: self._query['where'] += ' AND '
		self._query['where'] += '`%s`%s"%s"' % (key, o, val)
		return self

	def where_in(self, key, items):
		if self._query['where']: self._query['where'] += ' AND '
		self._query['where'] += '`%s` IN ("%s")' % (key, '", "'.join(items))
		return self

	def values(self, values):
		for k,v in values.items():
			self._query['values'][k] = v
		return self

	############################################################################

	def get(self, table):
		self.table(table)
		self.cursor.execute( self._build_query() )
		return self.cursor

	def insert(self, table, data):
		self.table(table)
		self.values(data)
		self.cursor.execute( self._build_query('insert') )
		return self.cursor.lastrowid

	def update(self, table, data):
		self.table(table)
		self.values(data)
		self.cursor.execute( self._build_query('update') )
		return self.cursor.rowcount

	def commit(self):
		self.conn.commit()

############################################################################