#!/usr/bin/env python
# This file is part of android-permissions and licensed under The MIT License (MIT).

import threading
import re
import psycopg2

from config import *



config = Config()
config.read_config()

# connect to database
db_conn = psycopg2.connect(host = config.db_host, user = config.db_user, password = config.db_password, database = config.db_database)
db_cursor = db_conn.cursor()

db_cursor.execute('SELECT "identifier", "permissions" FROM "public"."applications" WHERE name is not null;')
apps = db_cursor.fetchall()

unknown_permissions = {}
permissions = {}


for app in apps:
    identifier = app[0]
    perms = app[1]
    perms = perms.split(', ')
    for perm in perms:
        permissions[perm] = ''

    db_cursor.execute('DELETE FROM "public"."applications_permissions" WHERE identifier = \''+identifier+'\';')
    for perm in permissions:
        db_cursor.execute('INSERT INTO "public"."applications_permissions" (identifier, name) SELECT \''+identifier+'\', name FROM "public"."permissions" WHERE regex = \''+perm+'\';')
        if (db_cursor.rowcount == 0):
            unknown_permissions[perm] = ''

    db_conn.commit()


print ''
print "unknown permissions: ", unknown_permissions
print ''
