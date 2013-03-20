# -*- coding: utf-8 -*-

############################################################################

class TaskService(object):

	config = {}
	target = {}

	def __init__(self, config, target):
		self.validate_config(config, target)
		# log.name(target).info("Working on [{0}]", self.target)

	@classmethod
	def validate_config(cls, config, target):
		cls.default_priority = ''
		if config.has_option(target, 'default_priority'):
			cls.default_priority = config.get(target, 'default_priority')

	############################################################################

	def projects(self):
		raise NotImplementedError

	def tasks(self):
		raise NotImplementedError

	def task(self, task):
		raise NotImplementedError

	############################################################################

	def get_id(self, task):
		raise NotImplementedError

	def get_status(self, task):
		raise NotImplementedError

	def get_project(self, task):
		raise NotImplementedError

	def get_name(self, task):
		raise NotImplementedError

	def get_url(self, task):
		raise NotImplementedError

	def get_description(self, task):
		raise NotImplementedError

	def get_actual_time(self, task):
		raise NotImplementedError

	def get_estimated_time(self, task):
		raise NotImplementedError

	def get_priority(self, task):
		raise NotImplementedError

	def get_date_start(self, task):
		raise NotImplementedError

	def get_date_deadline(self, task):
		raise NotImplementedError

	def get_date_finished(self, task):
		raise NotImplementedError

	def get_date_added(self, task):
		raise NotImplementedError

	def get_date_modified(self, task):
		raise NotImplementedError

############################################################################

from thehitlist import TheHitList

SERVICES = {
	'thehitlist': TheHitList
}

############################################################################

def service(config, target):
	return SERVICES[config.get(target, 'service')](config, target)

############################################################################