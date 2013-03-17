#!/usr/bin/python
# -*- coding: utf-8 -*-

############################################################################

import optparse
import sys
import os

import notifications as notify
import services
from config import Config

############################################################################

status = dict(
	# created   = dict(name='создана', key='created'),
	# assigned  = dict(name='назначена', key='assigned'),
	accepted  = dict(name='принята', key='accepted'),
	# rejected  = dict(name='отклонена', key='rejected'),
	# done      = dict(name='условно завершена', key='done'),
	completed = dict(name='завершена', key='completed'),
	# delayed   = dict(name='поставлена на паузу', key='delayed'),
	canceled  = dict(name='отменена', key='canceled'),
	# expired   = dict(name='провалена', key='expired'),
)

############################################################################

class zTask():

	config  = {}
	targets = []

	def __init__(self):

		# Get config items
		c = Config('settings.ini')
		self.config = c.load_config()

		c.validate_config(self.config)

		notify.init(self.config)

		self.targets = c.get_targets_list(self.config)

	############################################################################

	def synch(self):
		for target in self.targets:
			service = services.service(self.config, target)

			# Pull target data
			tasks = service.tasks()

			for t in tasks:
				print t['priority'] , ' ', t['status'], '|', t['name'], t['date_added']


############################################################################
############################################################################
############################################################################

if __name__ == '__main__':
	ztask = zTask()

	ztask.synch()
	# ztask.display_tasks()
	# ztask.display_projects()

############################################################################