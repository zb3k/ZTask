# -*- coding: utf-8 -*-

############################################################################

class TaskService(object):
	def __init__(self, config, target):
		self.config  = config
		self.target  = target

		self.validate_config(config, target)

		# log.name(target).info("Working on [{0}]", self.target)

	@classmethod
	def validate_config(cls, config, target):
		cls.default_priority = ''
		if config.has_option(target, 'default_priority'):
			cls.default_priority = config.get(target, 'default_priority')

		# if config.has_option(target, 'project'):
		# 	cls.project = config.get(target, 'project')


	def tasks(self):
		raise NotImplementedError

	def get_id(self, task):
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