# -*- coding: utf-8 -*-

############################################################################

import ConfigParser
import sys
import os
import inspect

############################################################################

def die(msg):
	print 'SETTINGS ERROR:', msg
	sys.exit(1)

############################################################################

class Config():
	config_file = ''

	def __init__(self, config_file):
		self.config_file = config_file

	def validate_config(self, config):

		# [general]
		if not config.has_section('general'):
			die("No [general] section found.")

		# [general] > targets
		if not config.has_option('general', 'targets'):
			die("No targets= item in [general] found.")

		targets = config.get('general', 'targets')
		targets = [t.strip() for t in targets.split(',')]

		for target in targets:
			if target not in config.sections():
				die("No [%s] section found." % target)

	def load_config(self):
		path   = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		config = ConfigParser.ConfigParser()

		config.read(path + '/' + self.config_file)

		self.validate_config(config)

		print config.items('netcat_trac')