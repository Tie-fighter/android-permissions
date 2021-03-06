#!/usr/bin/env python
# This file is part of android-permissions and licensed under The MIT License (MIT).

import sys
import os
import re
import psycopg2
import time
import Queue
import logging

import CrawlerThread
import ProcessorThread

from config import *


def print_usage():
    print 'USAGE:'
    print '--continue: continue discovered but uncrawled apps'
    print '--recrawl: recrawl the google play store'
    print '--update: recrawl and update already visited apps'
    print ''

def main():

    contin = False;
    recrawl = False;
    update = False;

    # check arguments
    if (len(sys.argv) < 1 or len(sys.argv) > 4):
	    print_usage()
	    exit()
 
    for arg in sys.argv:
        if (arg is sys.argv[0]):
            pass
        elif (arg == "--continue"):
            contin = True;
        elif (arg == "--recrawl"):
            recrawl = True;
        elif (arg == "--update"):
            update = True;
        else:
            print 'unknown argument: "'+arg+'"'
            print_usage()
            exit()

    config = Config()
    config.read_config()

    # connect to database
    db_conn = psycopg2.connect(host = config.db_host, user = config.db_user, password = config.db_password, database = config.db_database)
    db_cursor = db_conn.cursor()

    
    logger = logging.getLogger('myapp')
    hdlr = logging.FileHandler('android-permissions.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.INFO)
    logger.info("starting")

    crawling_queue = Queue.Queue()		# [ url ]						will be crawled
    crawled_dict = dict()				# { url: "crawled" }			was crawled
    discovered_dict = dict()			# { identifier: url }			is known, will be ignored when found while crawling
    processing_queue = Queue.Queue()	# [ identifier, url, html ]		will be processed
    processed_dict = dict()				# { identifier: "processed" }	was processed

    # load a list of already found apps
    db_cursor.execute('SELECT "identifier", "last_time_processed" FROM "public"."applications" WHERE last_time_processed is null;')
    print str(db_cursor.rowcount) + " unprocessed apps found in the database"
    logger.info(str(db_cursor.rowcount) + " unprocessed apps found in the database")
    apps = db_cursor.fetchall()

    for app in apps:
        discovered_dict[app[0]] = config.app_url + app[0] + "&hl=en"
        if (contin is True):
            crawling_queue.put(config.app_url + app[0] + "&hl=en")


    # load a list of already processed apps
    db_cursor.execute('SELECT "identifier", "last_time_processed" FROM "public"."applications" WHERE name is not null;')
    print str(db_cursor.rowcount) + " apps found in the database"
    logger.info(str(db_cursor.rowcount) + " apps found in the database")
    apps = db_cursor.fetchall()
    
    # if recrawling
    if (recrawl is True or (crawling_queue.qsize() == 0 and len(apps) == 0)):
        # add featured to visiting queue
        for i in range(0, 48, 24):
            crawling_queue.put(config.market_url + "collection/featured?start=" + str(i) + "&num=24&hl=en")
        # add categories to visiting_queue
        db_cursor.execute('SELECT "value" FROM "public"."categories"')
        categories = db_cursor.fetchall()
        for category in categories:
            for i in range(0, 480, 24):
                #https://play.google.com/store/apps/category/ARCADE/collection/topselling_paid?start=24&num=24&hl=en
                crawling_queue.put(config.market_url + "category/" + category[0] + "/collection/topselling_paid?start=" + str(i) +"&num=24&hl=en")
                #https://play.google.com/store/apps/category/ARCADE/collection/topselling_free?start=456&num=24&hl=en
                crawling_queue.put(config.market_url + "category/" + category[0] + "/collection/topselling_free?start=" + str(i) +"&num=24&hl=en")


    # if updating
    if (update is True):
        for app in apps:
            crawling_queue.put(config.app_url + app[0] + "&hl=en")
            discovered_dict[app[0]] = config.app_url + app[0] + "&hl=en"
    else:
        for app in apps:
            discovered_dict[app[0]] = config.app_url + app[0] + "&hl=en"
            processed_dict[app[0]] = (app[1])

    # start crawlers
    for i in range(config.crawlers):
        crawler = CrawlerThread.CrawlerThread(logger, crawling_queue, crawled_dict, discovered_dict, processing_queue, processed_dict)
        crawler.setDaemon(True)
        crawler.start()


    # start processors
    for i in range(config.processors):
        processor = ProcessorThread.ProcessorThread(logger, processing_queue, processed_dict)
        processor.setDaemon(True)
        processor.start()

    # display status
    while (crawling_queue.empty() is False or processing_queue.empty is False):
        print "crawl:", crawling_queue.qsize(), "/ crawled:", len(crawled_dict), "/ discovered apps:", len(discovered_dict), "/ process:", processing_queue.qsize(), "/ processed:", len(processed_dict)
        logger.info("crawl: " +str(crawling_queue.qsize())+ " / crawled: " +str(len(crawled_dict))+ " / discovered apps: " +str(len(discovered_dict))+ " / process: " +str(processing_queue.qsize())+ " / processed: "+ str(len(processed_dict)))
        # TODO: restarted crashed threads
        time.sleep(10)


    crawling_queue.join()
    processing_queue.join()

    db_conn.close()

if __name__ == '__main__':
    main()
