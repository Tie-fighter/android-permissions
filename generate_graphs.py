#!/usr/bin/env python
# This file is part of android-permissions and licensed under GNU LGPL.

import psycopg2
import math
import random

import HTMLParser

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot

from config import *

def main():

    path = '/var/lib/android-permissions/'

    h = HTMLParser.HTMLParser()

    config = Config()
    config.read_config()

    # connect to database
    db_conn = psycopg2.connect(host = config.db_host, user = config.db_user, password = config.db_password, database = config.db_database)
    db_cursor = db_conn.cursor()

    db_cursor.execute('SELECT "identifier", "last_time_processed" FROM "public"."applications" WHERE name is not null;')
    app_count = db_cursor.rowcount
    print str(app_count) + " processed apps found in the database"
    apps_processed = db_cursor.fetchall()

    ###
    # apps_per_category
    db_cursor.execute('SELECT (SELECT name FROM categories WHERE id = category) AS category, COUNT(name) from applications GROUP BY category ORDER BY count DESC')
    app_data = db_cursor.fetchall()

    app_count_names = []
    app_count_data = []

    for group in app_data:
        app_count_names.insert(0, str(group[0]).lower().replace('_', ' '))
        app_count_data.insert(0, int(group[1]))

    fig = pyplot.figure(figsize=(8, 7))
    fig.subplots_adjust(left=0.25)
    pyplot.barh(bottom=drange(0.5, len(app_count_names)*1.5+0.5, 1.5), width=app_count_data)
    pyplot.title('Applications per category')
    pyplot.xlabel('number of applications (n='+str(app_count)+')')
    pos = drange(0.9, len(app_count_names)*1.5+0.9, 1.5)
    pyplot.yticks(pos, app_count_names)
    pyplot.grid(True)
    pyplot.savefig( path + 'apps_per_category.svg')



    ###
    # top 25 permissions
    db_cursor.execute('SELECT (SELECT regex from permissions WHERE id = permission_id) AS permission, COUNT(*)::float/(SELECT COUNT(name)::float FROM applications) AS percent FROM applications_permissions GROUP BY permission_id ORDER BY percent DESC LIMIT 25')
    top25permissions_data = db_cursor.fetchall()

    top25permissions_count_names = []
    top25permissions_count_data = []

    for group in top25permissions_data:
        top25permissions_count_names.insert(0, str(h.unescape(group[0])))
        top25permissions_count_data.insert(0, float(group[1]))

    fig = pyplot.figure(figsize=(12, 6))
    fig.subplots_adjust(left=0.5)
    pyplot.barh(bottom=drange(0.5, len(top25permissions_count_names)*1.5+0.5, 1.5), width=top25permissions_count_data)
    pyplot.title('Top 25 requested permissions')
    pyplot.xlabel('percentage of applications (n='+str(app_count)+')')
    pos = drange(0.9, len(top25permissions_count_names)*1.5+0.9, 1.5)
    pyplot.yticks(pos, top25permissions_count_names)
    pyplot.grid(True)
    pyplot.savefig( path + 'top25permissions.svg')
    


    ###
    # top 25 developers
    db_cursor.execute('SELECT developer, COUNT(developer) FROM applications GROUP BY developer ORDER BY count DESC LIMIT 25')
    top25developers_data = db_cursor.fetchall()

    top25developers_count_names = []
    top25developers_count_data = []

    for group in top25developers_data:
        top25developers_count_names.insert(0, str(h.unescape(group[0])))
        top25developers_count_data.insert(0, int(group[1]))

    fig = pyplot.figure()
    fig.subplots_adjust(left=0.35)
    pyplot.barh(bottom=drange(0.5, len(top25developers_count_names)*1.5+0.5, 1.5), width=top25developers_count_data)
    pyplot.title('Top 25 developers')
    pyplot.xlabel('number of applications (n='+str(app_count)+')')
    pos = drange(0.9, len(top25developers_count_names)*1.5+0.9, 1.5)
    pyplot.yticks(pos, top25developers_count_names)
    pyplot.grid(True)
    pyplot.savefig( path + 'top25developers.svg')

    ###
    # SELECT (SELECT COUNT(name) FROM applications WHERE price = '0') AS "Free", (SELECT COUNT(name) FROM applications WHERE price != '0') AS "Paid"


    ###
    # Free vs Paid

    db_cursor.execute('WITH  c AS ( \
                       SELECT sum((a.price > 0)::int) AS cc \
                             ,sum((a.price = 0)::int) AS cf \
                       FROM   applications a \
                       ), p AS ( \
                       SELECT p.id \
                             ,p.regex \
                             ,sum((a.price > 0)::int) AS pc \
                             ,sum((a.price = 0)::int) AS pf \
                       FROM   permissions p \
                       LEFT   JOIN applications_permissions ap ON ap.permission_id = p.id \
                       LEFT   JOIN applications a ON a.id = ap.application_id \
                       GROUP  BY 1, 2 \
                       ) \
                   SELECT p.id \
                        ,p.regex \
                        ,pc / cc::float AS commercial \
                        ,pf / cf::float AS free \
                        ,CASE WHEN pc = 0 THEN 0 \
                         ELSE ((pf / cf::float) - (pc / cc::float)) / (pc / cc::float) \
                         END as rel_difference \
                   FROM   c, p \
                   WHERE  p.regex is not Null \
                   ORDER BY  1;')
    permissions_data = db_cursor.fetchall()




    permissions_ids = []
    permissions_names = []
    permissions_commcount = []
    permissions_freecount = []
    permissions_difference = []
  
    for permission in permissions_data:
        permissions_ids.insert(0, int(permission[0]))
        permissions_names.insert(0, str(h.unescape(permission[1])))
        permissions_commcount.insert(0, float(permission[2]))
        permissions_freecount.insert(0, float(permission[3]))
        permissions_difference.insert(0, float(permission[4]))

    print permissions_difference

    fig = pyplot.figure(figsize=(12, 12))
    sb411 = fig.add_subplot(411)
    sb412 = fig.add_subplot(412, sharex=sb411)

    sb411.plot(permissions_ids, permissions_commcount, 'r.', label="commercial")
    sb411.plot(permissions_ids, permissions_freecount, 'b.', label="free")
    sb411.fill_between(permissions_ids, permissions_commcount, permissions_freecount, facecolor='green')
    sb411.set_title('Characteristic line')
#    sb411.set_yscale('log')
    sb411.set_ylabel('percentage of applications')
    sb411.legend()
    sb411.grid(True)


    sb412.plot(permissions_ids, permissions_difference, 'g.', label="difference")
    sb412.fill_between(permissions_ids, permissions_difference, 0)
#    sb412.set_yscale('log')
#    sb412.set_xlim(35, 50)
    sb412.set_xlim(0, max(permissions_ids))
    sb412.set_ylim(-1, 4)
    sb412.set_xlabel('permission id')
    sb412.set_ylabel('relative difference')
    sb412.grid(True)


    pyplot.savefig( path + 'characteristic.svg')


#    fig = pyplot.figure(figsize=(36, 36))
#    fig.subplots_adjust(left=0.22)
#    pos = np.arange(len(permissions_names))
#    height = 0.35
#    rects1 = pyplot.barh(pos, width=permissions_commcount, height=0.35, color='r')
#    rects2 = pyplot.barh(pos-height, width=permissions_freecount, height=0.35, color='g')
#    pyplot.legend( (rects1[0], rects2[0]), ('Commercial', 'Free') )
#    pyplot.title('Commercial vs free applications')
#    pyplot.xlabel('percentage of applications')
#    pyplot.yticks(pos, permissions_names)
#    pyplot.grid(True)
#    pyplot.savefig( path + 'freevscommpermissions.svg')


    ###
    # permissions per category
    db_cursor.execute('SELECT (SELECT regex from permissions WHERE id = permission_id) AS permission, COUNT(*) from applications_permissions GROUP BY permission_id ORDER BY count DESC')

    ####
    #categories = 'a b c d e f g h'.split()
    #permissions_average = [ 3, 2, 7, 9, 5, 3, 2, 4]
   
    #t = [x*0.1 for x in range(0,40)]
    #f = [math.exp(x) for x in t]
    #g = [10*math.cos(x) for x in t]
    #h = [10*math.sin(x) for x in t]
    #erx = [0.1*random.random() for x in t]
    #ery = [5*random.random() for x in t]
    #data = {"exp" : [t,f], "cos" : [t,g]}
    #series_colors = [ (1,0,0), (0,0,0), (0,0,1) ]

    #cairoplot.scatter_plot ( path + 'test.svg', data = data, errory = [ery,ery], width = 800, height = 600, border = 20, 
    #                         axis = True, discrete = False, dots = 5, grid = True, 
    #                         x_title = "t", y_title = "f(t) g(t)", series_legend=True, series_colors = ["red", "blue", "orange"])


def drange(start, stop, step):
    list = []
    steps = int(math.floor((stop-start)/step))
    
    for i in range(steps):
        list.append(start+i*step)

    return list

if __name__ == '__main__':
    main()

































