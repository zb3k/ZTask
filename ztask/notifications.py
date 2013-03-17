# -*- coding: utf-8 -*-

############################################################################

config = {
	'enabled': False,
	'driver':  '',
	'sticky':  False,

	'title': 'ZTask',
	'icon':  '/Applications/The Hit List.app/Contents/Resources/sync.png',
}

############################################################################

def init(conf):
	global config

	conf_section = 'notifications'

	if conf.has_section(conf_section):
		if conf.has_option(conf_section, 'enabled'):
			config['enabled'] = conf.getboolean(conf_section, 'enabled')

		if conf.has_option(conf_section, 'driver'):
			config['driver'] = conf.get(conf_section, 'driver')

		if conf.has_option(conf_section, 'sticky'):
			config['sticky'] = conf.getboolean(conf_section, 'sticky')

############################################################################

def send(msg):
	if config['enabled'] != True:
		return

	# Growl Notification (Mac OS)
	if config['driver'] == 'Growl':
		import gntp.notifier

		growl = gntp.notifier.GrowlNotifier(
			applicationName      = "ZTask",
			notifications        = ["New Updates", "New Messages"],
			defaultNotifications = ["New Messages"],
		)
		growl.register()

		icon = open(config['icon'], 'rb').read()

		growl.notify(
			noteType    = "New Messages",
			title       = config['title'],
			description = msg,
			icon        = icon,
			sticky      = config['sticky'],
			priority    = 1,
		)

	# Mac OS Notification Center
	if config['driver'] == 'OSX':
		from pync import Notifier
		Notifier.notify('Hello World', title=config['title'])

############################################################################