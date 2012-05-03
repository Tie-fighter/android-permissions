#!/usr/bin/env python
# This file is part of android-permissions and licensed under GNU LGPL.

import threading
import re
import psycopg2

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
            number_downloads = self.extract_number_downloads(html)
            size = self.extract_size(html)
            price = self.extract_price(html)
            content_rating = self.extract_content_rating(html)
            permissions = self.extract_permissions(html)
            
            self.logger.debug("extracted:" +name+ " " +developer+ " " +rating+ " " +rating_count+ " " +update_date+ " " +version+ " " +category+ " " +number_downloads+ " " +size+ " " +price+ " " +content_rating+ " " +str(permissions))

            self.update_database(identifier, name, developer, rating, rating_count, update_date, version, category, number_downloads, size, price, content_rating, permissions)
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

    def extract_number_downloads(self, html):
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


    def update_database(self, identifier, name, developer, rating, rating_count, update_date, version, category, downloads, size, price, content_rating, permissions):

        perms = ""
        for perm in permissions:
            perms = perms + perm + ', '
        perms = perms.rstrip(' ,')
  
        # try update app
        self.db_cursor.execute('UPDATE "public"."applications" SET last_time_processed = now(), name = '+name+', developer = '+developer+', rating = '+rating+', rating_count = '+rating_count+', update_date = '+update_date+', version = '+version+', category = (SELECT id FROM categories WHERE name = '+category+'), downloads = '+downloads+', size = '+size+', price = '+price+', content_rating = '+content_rating+', permissions = \''+perms+'\' WHERE identifier = \''+identifier+'\';')
        self.logger.debug('UPDATE "public"."applications" SET last_time_processed = now(), name = '+name+', developer = '+developer+', rating = '+rating+', rating_count = '+rating_count+', update_date = '+update_date+', version = '+version+', category = (SELECT id FROM categories WHERE name = '+category+'), downloads = '+downloads+', size = '+size+', price = '+price+', content_rating = '+content_rating+', permissions = \''+perms+'\' WHERE identifier = \''+identifier+'\';')
        
        # try insert app
        self.db_cursor.execute('INSERT INTO "public"."applications" (identifier, last_time_processed, name, developer, rating, rating_count, update_date, version, category, downloads, size, price, content_rating, permissions) SELECT \''+identifier+'\', now(), '+name+', '+developer+', '+rating+', '+rating_count+', '+update_date+', '+version+', (SELECT id FROM categories WHERE name = '+category+'), '+downloads+', '+size+', '+price+', '+content_rating+', \''+perms+'\' WHERE NOT EXISTS (SELECT 1 FROM "public"."applications" WHERE identifier = \''+identifier+'\');')
        self.logger.debug('INSERT INTO "public"."applications" (identifier, last_time_processed, name, developer, rating, rating_count, update_date, version, category, downloads, size, price, content_rating, permissions) SELECT \''+identifier+'\', now(), '+name+', '+developer+', '+rating+', '+rating_count+', '+update_date+', '+version+', (SELECT id FROM categories WHERE name = '+category+'), '+downloads+', '+size+', '+price+', '+content_rating+', \''+perms+'\' WHERE NOT EXISTS (SELECT 1 FROM "public"."applications" WHERE identifier = \''+identifier+'\');')

        self.db_conn.commit()        

        # + permissions
        self.db_cursor.execute('DELETE FROM "public"."applications_permissions" WHERE application_id IN (SELECT id FROM "public"."applications" WHERE identifier = \''+identifier+'\');')
        for perm in permissions:
            try:
                self.db_cursor.execute('SELECT id FROM "public"."permissions" WHERE regex = \''+perm+'\'')
                id = self.db_cursor.fetchone()
                if (id != None):
                    id = int(id[0])
                    self.db_cursor.execute('INSERT INTO "public"."applications_permissions" (application_id, permission_id) VALUES ( (SELECT id FROM "public"."applications" WHERE identifier = \''+identifier+'\'), '+str(id)+' );')
                else:
                    self.logger.error("not found in Database: " + perm)
                    ###
                    self.db_cursor.execute('INSERT INTO "public"."permissions" (name, description, regex) VALUES ( \'unknown\', Null, \''+perm+'\' )');
                    self.db_cursor.execute('SELECT id FROM "public"."permissions" WHERE regex = \''+perm+'\'')
                    id = self.db_cursor.fetchone()[0]
                    self.db_cursor.execute('INSERT INTO "public"."applications_permissions" (application_id, permission_id) VALUES ( (SELECT id FROM "public"."applications" WHERE identifier = \''+identifier+'\'), '+str(id)+' );')
                    continue
                # commit
                self.db_conn.commit()
            except Exception, err:
                self.logger.error("Exception - " + str(err))
                






