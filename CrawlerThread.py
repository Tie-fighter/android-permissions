#!/usr/bin/env python
# This file is part of android-permissions and licensed under GNU LGPL.

import threading
import urllib
import re
import time
import psycopg2

from config import *

class HttpError(BaseException):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class CrawlerThread(threading.Thread):
    def __init__(self, logger, crawling_queue, crawled_dict, discovered_dict, processing_queue, processed_dict):
        threading.Thread.__init__(self)
        self.logger = logger
        self.crawling_queue = crawling_queue
        self.crawled_dict = crawled_dict
        self.discovered_dict = discovered_dict
        self.processing_queue = processing_queue
        self.processed_dict = processed_dict

        self.config = Config()
        self.config.read_config()

        # connect to database
        self.db_conn = psycopg2.connect(host = self.config.db_host, user = self.config.db_user, password = self.config.db_password, database = self.config.db_database)
        self.db_cursor = self.db_conn.cursor()

    def __del__(self):
        self.logger.info("crawled died")
        self.db_conn.close()

    def run(self):
        self.logger.info("crawler spawned")
        while True:
            url = self.crawling_queue.get()
            self.logger.debug("crawling " + url)
            try:
                html = self.fetch_page(url)
            except HttpError as e:
                self.logger.info("HttpError: Code " + e.value + " at " + url)
                if (re.match('https:\/\/play.google.com\/store\/apps\/details\?id=[^&"?#<>()]*', url) != None):
                    identifier = re.findall('\/store\/apps\/details\?id=([^&"?#<>()]*)', url)[0]
#                    print('INSERT INTO "public"."pointsintime" (timestamp, application_id) VALUES ( now(), (SELECT id FROM "public"."applications" WHERE identifier = \''+identifier+'\' ))')
#                    self.db_cursor.execute('INSERT INTO "public"."pointsintime" (timestamp, application_id) VALUES ( now(), (SELECT id FROM "public"."applications" WHERE identifier = \''+identifier+'\' ))')
#                    self.db_conn.commit()
                continue

            # add found apps to queue
            identifiers = self.find_identifiers(html)
            for identifier in identifiers:
                self.logger.debug("found " + identifier + " at " + url)
                if (self.discovered_dict.has_key(identifier) is False):
                    url_app = self.config.app_url + identifier + "&hl=en"
                    self.crawling_queue.put(url_app)
                    self.discovered_dict[identifier] = url_app
                    self.db_cursor.execute('INSERT INTO "public"."applications" (identifier) SELECT \''+identifier+'\' WHERE NOT EXISTS (SELECT 1 FROM "public"."applications" WHERE identifier = \''+identifier+'\');')
                    self.logger.debug("added for visit: " + url_app)
                    # commit
                    self.db_conn.commit()

            # check if this page is to be processed
            # TODO: use escaped self.config.app_url
            if (re.match('https:\/\/play.google.com\/store\/apps\/details\?id=[^&"?#<>()]*', url) != None):
                identifier = re.findall('\/store\/apps\/details\?id=([^&"?#<>()]*)', url)[0]
                if (self.discovered_dict.has_key(identifier) is False):
                    self.discovered_dict[identifier] = url
                self.logger.debug("added for processing: " + identifier + " from " + url)
                item = (identifier, url, html)
                self.processing_queue.put(item)

            self.crawled_dict[url] = "crawled"
            self.crawling_queue.task_done()
            time.sleep(1)

    def fetch_page(self, url):
        f = urllib.urlopen(url)

        code = str(f.getcode())

        if (re.findall('(2\\d\\d|3\\d\\d)', code)):
            return ''.join(f.readlines())
        else:
            raise HttpError(str(f.getcode()))

    def find_identifiers(self, html):
        identifiers = re.findall('\/store\/apps\/details\?id=([^&"?#<>()]*)', html)
        return list(identifiers)
