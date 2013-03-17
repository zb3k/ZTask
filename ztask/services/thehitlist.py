# -*- coding: utf-8 -*-

############################################################################

from appscript import *
import sys
import os
import time

from services import TaskService
from ztask import status

############################################################################

class TheHitList(TaskService):
	def __init__(self, *args, **kw):
		super(TheHitList, self).__init__(*args, **kw)

		self.app = app(self.appname)

	############################################################################

	@classmethod
	def validate_config(self, config, target):
		TaskService.validate_config(config, target)

		self.appname = 'The Hit List'
		if config.has_option(target, 'appname'):
			self.appname = config.get(target, 'appname')

		self.lists = False
		if config.has_option(target, 'lists'):
			lists = config.get(target, 'lists')
			if lists:
				self.lists = [l.strip().decode('utf-8') for l in lists.split(',')]

	############################################################################

	def projects(self):
		result = []
		try:
			for f in self.app.folders_group.folders.get():
				for lst in f.lists.get():
					result.append({
						'id':   lst.id.get(),
						'name': lst.name.get(),
						'_obj': lst
					})
		except:
			None

		return result

	############################################################################

	def tasks(self):

		# Projects
		all_projects = self.projects()
		if self.lists is False or self.lists is True:
			projects = all_projects
		else:
			projects = []
			for pr in all_projects:
				if pr['name'] in self.lists:
					projects.append(pr)

		# Tasks
		tasks = []
		for pr in projects:
			project_tasks = []
			try:
				project_tasks = pr['_obj'].tasks.get()
			except: None

			for t in project_tasks:
				tasks.append({
					'id':            self.get_id(t),
					'project_id':    pr['id'],
					'name':          self.get_name(t),
					'description':   self.get_description(t),
					'priority':      self.get_priority(t),
					'status':        self.get_status(t),
					'date_start':    self.get_date_start(t),
					'date_deadline': self.get_date_deadline(t),
					'date_finished': self.get_date_finished(t),
					'date_added':    self.get_date_added(t),
					'date_modified': self.get_date_modified(t),
				})

		return tasks

	############################################################################

	def get_id(self, t):
		return t.id.get()

	############################################################################

	def get_status(self, t):
		try:
			if t.completed.get(): return status['completed']['key']
		except: None
		try:
			if t.canceled.get(): return status['canceled']['key']
		except: None
		return status['accepted']['key']

	############################################################################

	def get_name(self, t):
		return t.title.get()

	############################################################################

	def get_description(self, t):
		return t.notes.get()

	############################################################################

	def get_priority(self, t):
		return {
			1:'H', 2:'H', 3:'H',
			4:'M', 5:'M', 6:'M',
			7:'L', 8:'L', 9:'L',
		}.get(t.priority.get(), self.default_priority)

	############################################################################

	def _date(self, t, key):
		d = getattr(t, key).get()
		if d == k.missing_value:
			return None
		else:
			d = d
		return d

	def get_date_start(self, t):
		return self._date(t, 'start_date')

	def get_date_deadline(self, t):
		return self._date(t, 'due_date')

	def get_date_finished(self, t):
		return self._date(t, 'completed_date')

	def get_date_added(self, t):
		return self._date(t, 'created_date')

	def get_date_modified(self, t):
		return self._date(t, 'modified_date')

	############################################################################