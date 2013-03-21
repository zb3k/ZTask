# -*- coding: utf-8 -*-

############################################################################

import os
import sys
import inspect
import httplib2
import time
from datetime import datetime
from dateutil import parser
from dateutil.tz import tzlocal

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run

from services import TaskService
from ztask import status


############################################################################

class GTasks(TaskService):

	def __init__(self, *args, **kw):
		super(GTasks, self).__init__(*args, **kw)

		path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

		self.flow    = flow_from_clientsecrets(path + '/client_secrets.json', scope=['https://www.googleapis.com/auth/tasks'])
		self.service = None
		self.http    = None

		self.storage = Storage(path + '/gtasks_storage.dat')
		credentials  = self.storage.get()

		if credentials is None or credentials.invalid:
			credentials = run(self.flow, self.storage)

		# Create an httplib2.Http object to handle our HTTP requests and authorize it
		# with our good Credentials.
		self.http = credentials.authorize( httplib2.Http() )

		self.service = build('tasks', 'v1', http=self.http)

	############################################################################

	@classmethod
	def validate_config(self, config, target):
		TaskService.validate_config(config, target)

		# self.config['appname'] = 'The Hit List'
		# if config.has_option(target, 'appname'):
		# 	self.config['appname'] = config.get(target, 'appname')

	############################################################################

	def projects(self):
		projects = []
		result = self.service.tasklists().list().execute(http=self.http).get('items')
		for p in result:
			projects.append({
				'id':      p['id'],
				'name':    p['title'],
			})
		return projects

	############################################################################

	def tasks(self):

		updatedMin = self.synch_date.strftime('%Y-%m-%dT%H:%M:%S%z')

		# Projects
		projects = self.filter_projects( self.projects() )

		tasks = []
		for p in projects:
			result = self.service.tasks().list(tasklist=p['id'], updatedMin=updatedMin).execute(http=self.http).get('items')
			if result is not None:
				for t in result:
					tasks.append({
						'id':             t['id'],
						'project':        p['name'],
						'date_modified':  self._date(t['updated']),
						'name':           t['title'],
						'url':            t['selfLink'],
						'description':    t['notes'] if 'notes' in t else None,
						'priority':       None,
						'status':         'completed' if t['status'] == 'completed' else 'accepted',
						'date_start':     None,
						'date_deadline':  self._date(t['due']) if 'due' in t else None,
						'date_finished':  self._date(t['completed']) if 'completed' in t else None,
						'date_added':     None,
						'actual_time':    None,
						'estimated_time': None,
					})
		# for t in tasks:
		# 	print t['name'], t['date_modified'], '|', t['date_finished']
		# exit()
		return tasks

	############################################################################

	def _date(self, datestr):
		return parser.parse(datestr)
		# return datetime.strptime(datestr[:19], '%Y-%m-%dT%H:%M:%S')


