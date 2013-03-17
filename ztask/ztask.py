#!/usr/bin/python
# -*- coding: utf-8 -*-

############################################################################

import optparse
import sys
import os

import notifications
from config import Config

############################################################################

class zTask():

	config = {}

	def __init__(self):

		# Get config items
		c = Config('settings.ini')
		self.config = c.load_config()

		notifications.init(self.config)

		# notifications.send('hello')

		# print self.config


############################################################################

if __name__ == '__main__':
	ztask = zTask()

	# ztask.pull()
	# ztask.synch()
	# ztask.display_tasks()
	# ztask.display_projects()

############################################################################