# -*- coding: utf-8 -*-

############################################################################

class TaskService(object):

	config     = {}
	target     = {}
	synch_date = None

	def __init__(self, config, target):
		self.validate_config(config, target)
		# log.name(target).info("Working on [{0}]", self.target)

	@classmethod
	def validate_config(cls, config, target):
		cls.config['default_priority'] = ''
		if config.has_option(target, 'default_priority'):
			cls.config['default_priority'] = config.get(target, 'default_priority')

		cls.config['projects'] = False
		if config.has_option(target, 'projects'):
			projects = config.get(target, 'projects')
			if projects:
				cls.config['projects'] = [l.strip().decode('utf-8') for l in projects.split(',')]

	############################################################################

	def set_synch_date(self, synch_date):
		self.synch_date = synch_date

	############################################################################

	def projects(self):
		raise NotImplementedError

	def tasks(self):
		raise NotImplementedError

	def task(self, task):
		return {
			'id':             self.get_id(task),
			'project':        self.get_project(task),
			'date_modified':  self.get_date_modified(task),
			'name':           self.get_name(task),
			'url':            self.get_url(task),
			'description':    self.get_description(task),
			'priority':       self.get_priority(task),
			'status':         self.get_status(task),
			'date_start':     self.get_date_start(task),
			'date_deadline':  self.get_date_deadline(task),
			'date_finished':  self.get_date_finished(task),
			'date_added':     self.get_date_added(task),
			'actual_time':    self.get_actual_time(task),
			'estimated_time': self.get_estimated_time(task),
		};

	############################################################################

	def filter_projects(self, all_projects):
		if self.config['projects'] is False or self.config['projects'] is True:
			projects = all_projects
		else:
			projects = []
			for pr in all_projects:
				if pr['name'] in self.config['projects']:
					projects.append(pr)
		return projects

	############################################################################

	def get_id(self, task):
		return task['id']

	def get_status(self, task):
		return task['status']

	def get_project(self, task):
		return task['project']

	def get_name(self, task):
		return task['name']

	def get_url(self, task):
		return task['url'] if 'url' in task else None

	def get_description(self, task):
		return task['description'] if 'description' in task else None

	def get_actual_time(self, task):
		return task['actual_time'] if 'actual_time' in task else None

	def get_estimated_time(self, task):
		return task['estimated_time'] if 'estimated_time' in task else None

	def get_priority(self, task):
		return task['priority'] if 'priority' in task else None

	def get_date_start(self, task):
		return task['date_start'] if 'date_start' in task else None

	def get_date_deadline(self, task):
		return task['date_deadline'] if 'date_deadline' in task else None

	def get_date_finished(self, task):
		return task['date_finished'] if 'date_finished' in task else None

	def get_date_added(self, task):
		return task['date_added'] if 'date_added' in task else None

	def get_date_modified(self, task):
		return task['date_modified'] if 'date_modified' in task else None

############################################################################

from thehitlist import TheHitList
from gtasks import GTasks

SERVICES = {
	'thehitlist': TheHitList,
	'gtasks':     GTasks,
}

############################################################################

def service(config, target):
	return SERVICES[config.get(target, 'service')](config, target)

############################################################################