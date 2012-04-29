#!/usr/bin/env python
# This file is part of android-permissions and licensed under GNU LGPL.

import ConfigParser		# read_config

class Config():

	def read_config(self):
		config = ConfigParser.ConfigParser()
		config.read('config.ini')

        # General
		if config.get('General', 'crawlers') == '':
			print 'ERROR: crawlers not set'
			print_usage()
			exit()
		else:
			self.crawlers = int(config.get('General', 'crawlers'))

		if config.get('General', 'processors') == '':
			print 'ERROR: processors not set'
			print_usage()
			exit()
		else:
			self.processors = int(config.get('General', 'processors'))

        # Market
		if config.get('Market', 'market_url') == '':
			print 'ERROR: market_url not set'
			print_usage()
			exit()
		else:
			self.market_url = config.get('Market', 'market_url')

		if config.get('Market', 'app_url') == '':
			print 'ERROR: app_url not set'
			print_usage()
			exit()
		else:
			self.app_url = config.get('Market', 'app_url')

        # Database
		if config.get('Database', 'host') == '':
			print 'ERROR: Database host not set'
			print_usage()
			exit()
		else:
			self.db_host = config.get('Database', 'host')

		if config.get('Database', 'user') == '':
			print 'ERROR: Database user not set'
			print_usage()
			exit()
		else:
			self.db_user = config.get('Database', 'user')

		if config.get('Database', 'password') == '':
			print 'ERROR: Database password not set'
			print_usage()
			exit()
		else:
			self.db_password = config.get('Database', 'password')

		if config.get('Database', 'database') == '':
			print 'ERROR: Database database not set'
			print_usage()
			exit()
		else:
			self.db_database = config.get('Database', 'database')
		return

