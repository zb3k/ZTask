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
					'id':      self.get_id({'_obj':t}),
					'_obj':    t,
					'project': pr['name'],
				})
		return tasks

	############################################################################

	def task(self, t):
		return {
			'id':             self.get_id(t),
			# 'project_id':     self.get_date_modified(t),
			'project':        self.get_project(t),
			'date_modified':  self.get_date_modified(t),
			'name':           self.get_name(t),
			'description':    self.get_description(t),
			'priority':       self.get_priority(t),
			'status':         self.get_status(t),
			'date_start':     self.get_date_start(t),
			'date_deadline':  self.get_date_deadline(t),
			'date_finished':  self.get_date_finished(t),
			'date_added':     self.get_date_added(t),
			'actual_time':    self.get_actual_time(t),
			'estimated_time': self.get_estimated_time(t),
		};

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
		}.get(t['_obj'].priority.get(), self.default_priority)

	############################################################################

	def _date(self, t, key):
		d = getattr(t['_obj'], key).get()
		if d == k.missing_value:
			return None
		else: d = d
		return d

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