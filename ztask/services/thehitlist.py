# -*- coding: utf-8 -*-

############################################################################

from appscript import *
import sys
import os
import time
from datetime import datetime
from dateutil.tz import tzlocal
from dateutil import parser

from services import TaskService
from ztask import status

############################################################################

class TheHitList(TaskService):

	def __init__(self, *args, **kw):
		super(TheHitList, self).__init__(*args, **kw)
		self.app = app(self.config['appname'])

	############################################################################

	@classmethod
	def validate_config(self, config, target):
		TaskService.validate_config(config, target)

		self.config['appname'] = 'The Hit List'
		if config.has_option(target, 'appname'):
			self.config['appname'] = config.get(target, 'appname')

	############################################################################

	def projects(self):
		result = []
		for f in self.app.folders_group.folders.get():
			try:
				for lst in f.lists.get():
					result.append({
						'id':   lst.id.get(),
						'name': lst.name.get(),
						'_obj': lst
					})
			except: None
		return result

	############################################################################

	def tasks(self):

		# Projects
		projects = self.filter_projects( self.projects() )

		# Tasks
		tasks = []
		for pr in projects:
			project_tasks = []
			try:
				project_tasks = pr['_obj'].tasks.get()
			except: None

			for t in project_tasks:
				tasks.append({
					'id':      self.get_id({'_obj':t}),
					'project': pr['name'],
					'_obj':    t,
				})
		return tasks

	############################################################################

	def get_id(self, t):
		if 'id' in t: return t['id']
		return t['_obj'].id.get()

	############################################################################

	def get_project(self, t):
		return t['project']

	############################################################################

	def get_status(self, t):
		if 'status' in t: return t['status']
		try:
			if t['_obj'].completed.get(): return status['completed']['key']
		except: None
		try:
			if t['_obj'].canceled.get(): return status['canceled']['key']
		except: None
		return status['accepted']['key']

	############################################################################

	def get_name(self, t):
		if 'name' in t: return t['name']
		return t['_obj'].title.get()

	############################################################################

	def get_description(self, t):
		if 'description' in t: return t['description']
		return t['_obj'].notes.get()

	############################################################################

	def get_actual_time(self, t):
		if 'actual_time' in t: return t['actual_time']
		return t['_obj'].actual_time.get()

	def get_estimated_time(self, t):
		if 'estimated_time' in t: return t['estimated_time']
		return t['_obj'].estimated_time.get()

	############################################################################

	def get_priority(self, t):
		if 'priority' in t: return t['priority']
		return {
			1:'H', 2:'H', 3:'H',
			4:'M', 5:'M', 6:'M',
			7:'L', 8:'L', 9:'L',
		}.get(t['_obj'].priority.get(), self.config['default_priority'])

	############################################################################

	def _date(self, t, key):
		d = getattr(t['_obj'], key).get()
		if d == k.missing_value:
			return None
		else:
			d = d

		toffset = datetime.now(tzlocal()).strftime('%z')
		return parser.parse(d.strftime('%Y-%m-%d %H:%M:%S'+toffset))

	def get_date_start(self, t):
		if 'start_date' in t: return t['start_date']
		return self._date(t, 'start_date')

	def get_date_deadline(self, t):
		if 'due_date' in t: return t['due_date']
		return self._date(t, 'due_date')

	def get_date_finished(self, t):
		if 'completed_date' in t: return t['completed_date']
		return self._date(t, 'completed_date')

	def get_date_added(self, t):
		if 'created_date' in t: return t['created_date']
		return self._date(t, 'created_date')

	def get_date_modified(self, t):
		if 'modified_date' in t: return t['modified_date']
		return self._date(t, 'modified_date')

	############################################################################