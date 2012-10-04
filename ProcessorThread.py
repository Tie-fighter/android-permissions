#!/usr/bin/env python
# This file is part of android-permissions and licensed under GNU LGPL.

import threading
import re
import psycopg2
import time

import traceback

from config import *


class ProcessorThread(threading.Thread):
    def __init__(self, logger, processing_queue, processed_dict):
        threading.Thread.__init__(self)
        self.logger = logger
        self.processing_queue = processing_queue
        self.processed_dict = processed_dict

        self.config = Config()
        self.config.read_config()

        # connect to database
        self.db_conn = psycopg2.connect(host = self.config.db_host, user = self.config.db_user, password = self.config.db_password, database = self.config.db_database)
        self.db_cursor = self.db_conn.cursor()

    def __del__(self):
        self.logger.info("processor died")
        self.db_conn.close()

    def run(self):
        self.logger.info("processor spawned")
        while True:
            item = self.processing_queue.get()
            identifier = item[0]
            url = item[1]
            html = item[2]
            self.logger.debug("processing: " + identifier)

            name = self.extract_name(html).replace("\\", "\\\\")
            developer = self.extract_developer(html).replace("\\", "\\\\")
            rating = self.extract_rating(html)
            rating_count = self.extract_rating_count(html)
            update_date = self.extract_update_date(html)
            version = self.extract_version(html)
            category = self.extract_category(html)
            download = self.extract_download(html)
            size = self.extract_size(html)
            price = self.extract_price(html)
            content_rating = self.extract_content_rating(html)
            permissions = self.extract_permissions(html)
            
            self.logger.debug("extracted:" +name+ " " +developer+ " " +rating+ " " +rating_count+ " " +update_date+ " " +version+ " " +category+ " " +download+ " " +size+ " " +price+ " " +content_rating+ " " +str(permissions))

            self.update_database(identifier, name, developer, rating, rating_count, update_date, version, category, download, size, price, content_rating, permissions)
            self.processed_dict[identifier] = [ url, "processed" ]

            self.processing_queue.task_done()


    def fetch_page(self, url):
        f = urllib.urlopen(url)
        return ''.join(f.readlines())

    def extract_name(self, html):
        #<h1 class="doc-banner-title">Dream Heights</h1>
        match = re.findall('<h1 class="doc-banner-title">(.*?)<\/h1>', html)
        if match:
            return '\'' + match[0] + '\''
        else:
            return 'NULL'

    def extract_developer(self, html):
        #<a href="/store/apps/developer?id=Zynga" class="doc-header-link">Zynga</a>
        match = re.findall('class="doc-header-link">(.*?)</a>', html)
        if match:
            return '\'' + match[0] + '\''
        else:
            return 'NULL'
        
    def extract_rating(self, html):
        #<div class="ratings goog-inline-block" title="Rating: 4.8 stars (Above average)" itemprop="ratingValue" content="4.8">
        match = re.findall('itemprop="ratingValue" content="([0-9,.]*?)"', html)
        if match:
            return '\'' + match[0] + '\''
        else:
            return 'NULL'

    def extract_rating_count(self,html):
        #<span itemprop="ratingCount" content="3402">3,402</span>
        match = re.findall('itemprop="ratingCount" content="([0-9]*?)"', html)
        if match:
            return '\'' + match[0] + '\''
        else:
            return '\'0\''

    def extract_update_date(self, html):
        #<time itemprop="datePublished">March 30, 2012</time>
        match = re.findall('itemprop="datePublished">(.*?)<', html)
        if match:
            return '\'' + match[0] + '\''
        else:
            return 'NULL'

    def extract_version(self, html):
        #<dd itemprop="softwareVersion">1.0.1</dd>
        match = re.findall('itemprop="softwareVersion">(.*?)<', html)
        if match:
            return '\'' + match[0] + '\''
        else:
            return 'NULL'

    def extract_category(self, html):
        #<dt>Category:</dt>\w<dd><a href="/store/apps/category/BRAIN?feature=category-nav">Brain &amp; Puzzle</a></dd>
        match = re.findall('<dt>Category:<\/dt>\s?<dd><a href="\/store\/apps\/category\/([A-Z\_]*)', html)
        if match:
            return '\'' + match[0] + '\''
        else:
            return 'NULL'

    def extract_download(self, html):
        #<dd itemprop="numDownloads">100,000 - 500,000<div class="normalized-daily-installs-chart" style="width: 105px;">
        match = re.findall('itemprop="numDownloads">(.*?)<', html)
        if match:
            return '\'' + match[0] + '\''
        else:
            return 'NULL'

    def extract_size(self, html):
        #<dd itemprop="fileSize">19M</dd>
        match = re.findall('itemprop="fileSize">(.*?)<', html)
        if match:
            return '\'' + match[0] + '\''
        else:
            return 'NULL'

    def extract_price(self, html):
        #<meta itemprop="price" content="0,76&nbsp;">
        match = re.findall('itemprop="price" content="([0-9,]*).*?"', html)
        if match:
            return '\'' + match[0].replace(',', '.') + '\''
        else:
            return 'NULL'

    def extract_content_rating(self, html):
        #<dd itemprop="contentRating">Low Maturity</dd>
        match = re.findall('itemprop="contentRating">(.*?)<', html)
        if match:
            return '\'' + match[0] + '\''
        else:
            return 'NULL'


    def extract_permissions(self, html):
        #<div class="doc-permission-description">coarse (network-based) location</div>
        match = re.findall('class="doc-permission-description">(.*?)<', html)
        if match:
            return list(match)
        else:
            return ('None',)


    def update_database(self, identifier, name, developer, rating, rating_count, update_date, version, category, download, size, price, content_rating, permissions):

        perms = ""
        perm_dict = dict()
        for perm in permissions:
            perm_dict[perm] = ''
        for perm in perm_dict:
            perms = perms + perm + ', '
        perms = perms.rstrip(' ,')


        # 
        # try all the values and insert if necessary
        
        try:
            # developers
            self.db_cursor.execute('SELECT id FROM "public"."developers" WHERE value = '+developer+'')
            developer_id = self.db_cursor.fetchone()
            if (developer_id != None):
                developer_id = int(developer_id[0])
            else:
                self.logger.verbose("developer not found in Database: " + developer + " -> inserting")
                self.db_cursor.execute('INSERT INTO "public"."developers" (value) VALUES ('+developer+')')
                self.db_cursor.execute('SELECT id FROM "public"."developers" WHERE value = '+developer+'')
                developer_id = int(self.db_cursor.fetchone()[0])

            # categories
            self.db_cursor.execute('SELECT id FROM "public"."categories" WHERE value = '+category+'')
            category_id = self.db_cursor.fetchone()
            if (category_id != None):
                category_id = int(category_id[0])
            else:
                self.logger.verbose("category not found in Database: " + category + " -> inserting")
                self.db_cursor.execute('INSERT INTO "public"."categories" (value) VALUES ('+category+')')
                self.db_cursor.execute('SELECT id FROM "public"."categories" WHERE value = '+category+'')
                category_id = int(self.db_cursor.fetchone()[0])

            # icons
            # TODO

            # ratings
            self.db_cursor.execute('SELECT id FROM "public"."ratings" WHERE value = '+rating+'')
            rating_id = self.db_cursor.fetchone()
            if (rating_id != None):
                rating_id = int(rating_id[0])
            else:
                self.logger.verbose("rating not found in Database: " + rating + " -> inserting")
                self.db_cursor.execute('INSERT INTO "public"."ratings" (value) VALUES ('+rating+')')
                self.db_cursor.execute('SELECT id FROM "public"."ratings" WHERE value = '+rating+'')
                rating_id = int(self.db_cursor.fetchone()[0])

            # rating_count
            self.db_cursor.execute('SELECT id FROM "public"."rating_counts" WHERE value = '+rating_count+'')
            rating_count_id = self.db_cursor.fetchone()
            if (rating_count_id != None):
                rating_count_id = int(rating_count_id[0])
            else:
                self.logger.verbose("rating_count not found in Database: " + rating_count + " -> inserting")
                self.db_cursor.execute('INSERT INTO "public"."rating_counts" (value) VALUES ('+rating_count+')')
                self.db_cursor.execute('SELECT id FROM "public"."rating_counts" WHERE value = '+rating_count+'')
                rating_count_id = int(self.db_cursor.fetchone()[0])

            # downloads
            self.db_cursor.execute('SELECT id FROM "public"."downloads" WHERE value = '+download+'')
            download_id = self.db_cursor.fetchone()
            if (download_id != None):
                download_id = int(download_id[0])
            else:
                self.logger.verbose("download not found in Database: " + download + " -> inserting")
                self.db_cursor.execute('INSERT INTO "public"."downloads" (value) VALUES ('+download+')')
                self.db_cursor.execute('SELECT id FROM "public"."downloads" WHERE value = '+download+'')
                download_id = int(self.db_cursor.fetchone()[0])

            # size
            self.db_cursor.execute('SELECT id FROM "public"."sizes" WHERE value = '+size+'')
            size_id = self.db_cursor.fetchone()
            if (size_id != None):
                size_id = int(size_id[0])
            else:
                self.logger.verbose("size not found in Database: " + size + " -> inserting")
                self.db_cursor.execute('INSERT INTO "public"."sizes" (value) VALUES ('+size+')')
                self.db_cursor.execute('SELECT id FROM "public"."sizes" WHERE value = '+size+'')
                size_id = int(self.db_cursor.fetchone()[0])

            # price
            self.db_cursor.execute('SELECT id FROM "public"."prices" WHERE value = '+price+'')
            price_id = self.db_cursor.fetchone()
            if (price_id != None):
                price_id = int(price_id[0])
            else:
                self.logger.verbose("price not found in Database: " + price + " -> inserting")
                self.db_cursor.execute('INSERT INTO "public"."prices" (value) VALUES ('+price+')')
                self.db_cursor.execute('SELECT id FROM "public"."prices" WHERE value = '+price+'')
                price_id = int(self.db_cursor.fetchone()[0])

            # update dates
            self.db_cursor.execute('SELECT id FROM "public"."update_dates" WHERE value = '+update_date+'')
            update_date_id = self.db_cursor.fetchone()
            if (update_date_id != None):
                update_date_id = int(update_date_id[0])
            else:
                self.logger.verbose("price not found in Database: " + update_date+ " -> inserting")
                self.db_cursor.execute('INSERT INTO "public"."update_dates" (value) VALUES ('+update_date+')')
                self.db_cursor.execute('SELECT id FROM "public"."update_dates" WHERE value = '+update_date+'')
                update_date_id = int(self.db_cursor.fetchone()[0])

            # versions
            self.db_cursor.execute('SELECT id FROM "public"."versions" WHERE value = '+version+'')
            version_id = self.db_cursor.fetchone()
            if (version_id != None):
                version_id = int(version_id[0])
            else:
                self.logger.verbose("price not found in Database: " + version+ " -> inserting")
                self.db_cursor.execute('INSERT INTO "public"."versions" (value) VALUES ('+version+')')
                self.db_cursor.execute('SELECT id FROM "public"."versions" WHERE value = '+version+'')
                version_id = int(self.db_cursor.fetchone()[0])


            now = str(time.time())

            # application
            self.db_cursor.execute('UPDATE "public"."applications" SET last_time_processed = to_timestamp(\''+str(now)+'\'), name = '+name+' WHERE identifier = \''+identifier+'\';')
            self.db_cursor.execute('SELECT id FROM "public"."applications" WHERE identifier = \''+identifier+'\';')
            application_id =  int(self.db_cursor.fetchone()[0])

            # point in time
            self.db_cursor.execute('INSERT INTO "public"."pointsintime" (timestamp, application_id, developer_id, category_id, rating_id, rating_count_id, download_id, size_id, price_id, update_date_id, version_id) VALUES ( to_timestamp(\''+str(now)+'\'), \''+str(application_id)+'\', \''+str(developer_id)+'\', \''+str(category_id)+'\', \''+str(rating_id)+'\', \''+str(rating_count_id)+'\', \''+str(download_id)+'\', \''+str(size_id)+'\', \''+str(price_id)+'\', \''+str(update_date_id)+'\', \''+str(version_id)+'\')')
            self.db_cursor.execute('SELECT id FROM "public"."pointsintime" WHERE timestamp = to_timestamp('+str(now)+') AND application_id = \''+str(application_id)+'\'')
            pointintime_id = int(self.db_cursor.fetchone()[0])

            # permissions
            for perm in perm_dict:
                self.db_cursor.execute('SELECT id FROM "public"."permissions" WHERE regex = \''+perm+'\'')
                perm_id = self.db_cursor.fetchone()
                if (perm_id != None):
                    perm_id = int(perm_id[0])
                else:
                    self.logger.verbose("permission not found in Database: " +perm+ " -> inserting")
                    self.db_cursor.execute('INSERT INTO "public"."permissions" (name, description, regex) VALUES ( \'unknown\', Null, \''+perm+'\' )');
                    self.db_cursor.execute('SELECT id FROM "public"."permissions" WHERE regex = \''+perm+'\'')
                    perm_id = int(self.db_cursor.fetchone()[0])
                self.db_cursor.execute('INSERT INTO "public"."pointintime_permissions" (pointintime_id, permission_id) VALUES ( '+str(pointintime_id)+', '+str(perm_id)+' );')
     

            self.db_conn.commit()
        except Exception, err:
            self.logger.error("Exception - " + str(err))
            self.db_conn.rollback()


