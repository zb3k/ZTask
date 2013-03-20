#!/usr/bin/python
# -*- coding: utf-8 -*-

############################################################################

# import optparse
import sys
import os
from datetime import datetime
import time

import notifications as notify
import services
from config import Config
import db

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
		c = Config('config.ini')
		self.config = c.load_config()

		c.validate_config(self.config)

		self.targets = c.get_targets_list(self.config)

		notify.init(self.config)

		self.db = db.Database()

	############################################################################

	def get_settings(self, key, default = None, fn = None):
		row = self.db.where('key', '=', key).get('settings').fetchone();
		result = default
		if row is not None:
			result = row['value']
		if fn is not None:
			return fn(result)
		return result

	############################################################################

	def set_settings(self, key, value):
		row = self.db.where('key', '=', key).get('settings').fetchone();
		if row is None:
			self.db.insert('settings', dict(
				key   = key,
				value = value
			));
		else:
			self.db.where('key', '=', key).update('settings', dict(
				value = value
			));
		self.db.commit();

	############################################################################

	def date_now(self):
		return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	############################################################################

	def date(self, value):
		return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

	############################################################################

	def last_synch(self, val = None):
		if val is None:
			return self.get_settings('last_synch', '2012-01-01 00:00:00', self.date)
		else:
			self.set_settings('last_synch', val)
			return val

	############################################################################

	def pull(self):
		# get last pull
		last_synch = self.last_synch()

		for target in self.targets:

			print 'Pull target:', target

			service = services.service(self.config, target)

			# Pull target tasks
			tasks = service.tasks()

			task_ids = []
			for t in tasks: task_ids.append(service.get_id(t))

			# Find exist tasks
			self.db.where('target','=',target)
			self.db.where_in('id_b', task_ids);
			exist = {}
			for rel in self.db.get('relations').fetchall():
				exist[rel['id_b']] = rel['id_a']

			# Fill insert/update lists
			insert_tasks = []
			update_tasks = []
			for t in tasks:
				task_key = service.get_id(t)
				if task_key in exist:
					if service.get_date_modified(t) > last_synch:
						t['id'] = exist[task_key]
						update_tasks.append(t)
				else:
					insert_tasks.append(t)



			print '  Update:', len(update_tasks)
			print '  Insert:', len(insert_tasks)


			for task in update_tasks:
				task_id = task['id']
				task = service.task(task)
				del task['id']
				self.db.where('id','=', task_id).update('tasks', task);

			for task in insert_tasks:
				task = service.task(task)
				id_b = task['id']
				del task['id']
				task['source_target'] = target
				task_id = self.db.insert('tasks', task);
				self.db.insert('relations', dict(
					target = target,
					id_b   = id_b,
					id_a   = str(task_id),
					type   = 'tasks'
				));

			self.db.commit();

		self.last_synch(self.date_now())


############################################################################
############################################################################
############################################################################

if __name__ == '__main__':
	ztask = zTask()
	print '[START]'

	ztask.pull()

	# ztask.display_tasks()
	# ztask.display_projects()


	print '[END]'

############################################################################