#!/usr/bin/python
# -*- coding: utf-8 -*-

############################################################################

# import optparse
import time
import sys
import os
from twiggy import log
from datetime import datetime
from dateutil import parser
from dateutil.tz import tzlocal


import notifications as notify
import services
from config import Config
from config import die
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
		return datetime.now(tzlocal())

	############################################################################

	def date(self, value):
		return parser.parse(value)

	############################################################################

	def synch_date(self, key='',val = None):
		if val is None:
			return self.get_settings('synch_date_'+key, '2012-01-01 00:00:00+0000', self.date)
		else:
			self.set_settings('synch_date_'+key, val)
			return val

	############################################################################

	def pull(self):
		# get last pull

		log.info(' [pull]')

		for target in self.targets:
			log.info(' [{0}]', target)

			service = services.service(self.config, target)

			synch_date = self.synch_date(target)
			service.set_synch_date( synch_date )

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
					# print t['name'], service.get_date_modified(t), parser.parse(synch_date)
					if service.get_date_modified(t) > synch_date:
						t['id'] = exist[task_key]
						update_tasks.append(t)
				else:
					insert_tasks.append(t)


			log.info(' INSERT:{0} | UPDATE:{1}', len(insert_tasks), len(update_tasks))

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

			self.synch_date(target, self.date_now())


############################################################################
############################################################################
############################################################################

if __name__ == '__main__':

	ztask = zTask()

	ztask.pull()

	# ztask.display_tasks()
	# ztask.display_projects()

	log.info(' [END]')

############################################################################