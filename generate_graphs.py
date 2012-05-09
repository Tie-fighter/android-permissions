#!/usr/bin/env python
# This file is part of android-permissions and licensed under GNU LGPL.

import psycopg2
import math
import random

import cairoplot

from config import *

def main():

    path = '/var/lib/android-permissions/'

    config = Config()
    config.read_config()

    # connect to database
    db_conn = psycopg2.connect(host = config.db_host, user = config.db_user, password = config.db_password, database = config.db_database)
    db_cursor = db_conn.cursor()

    db_cursor.execute('SELECT "identifier", "last_time_processed" FROM "public"."applications" WHERE name is not null;')
    print str(db_cursor.rowcount) + " processed apps found in the database"
    apps_processed = db_cursor.fetchall()

    ###
    # apps_per_category
    db_cursor.execute('SELECT (SELECT name FROM categories WHERE id = category) AS category, COUNT(name) from applications GROUP BY category ORDER BY count DESC')
    app_data = db_cursor.fetchall()

    app_count_names = []
    app_count_data = []

    for group in app_data:
        app_count_names.append(str(group[0]))
        app_count_data.append(int(group[1]))

    cairoplot.vertical_bar_plot ( path + 'apps_per_category.svg', app_count_data, 800, 700, border = 20, display_values = True, grid = False, series_labels = app_count_names) 


    ###
    # top 25 permissions (TODO: percent)
    db_cursor.execute('SELECT (SELECT regex from permissions WHERE id = permission_id), COUNT(*) from applications_permissions GROUP BY permission_id ORDER BY count DESC LIMIT 25')
    top25permissions_data = db_cursor.fetchall()

    top25permissions_count_names = []
    top25permissions_count_data = []

    for group in top25permissions_data:
        top25permissions_count_names.append(str(group[0]))
        top25permissions_count_data.append(int(group[1]))

    cairoplot.vertical_bar_plot ( path + 'top25permissions.svg', top25permissions_count_data, 800, 500, border = 5, display_values = True, grid = False, series_labels = top25permissions_count_names)


    ###
    # top 25 developers
    db_cursor.execute('SELECT developer, COUNT(developer) from applications GROUP BY developer ORDER BY count DESC LIMIT 25')
    top25developers_data = db_cursor.fetchall()

    top25developers_count_names = []
    top25developers_count_data = []

    for group in top25developers_data:
        top25developers_count_names.append(str(group[0]))
        top25developers_count_data.append(int(group[1]))

    cairoplot.vertical_bar_plot ( path + 'top25developers.svg', top25developers_count_data, 800, 700, border = 5, display_values = True, grid = False, series_labels = top25developers_count_names)


    ###
    # SELECT (SELECT COUNT(name) FROM applications WHERE price = '0') AS "Free", (SELECT COUNT(name) FROM applications WHERE price != '0') AS "Paid"


    ###
    # Free vs Paid

#SELECT p.id
#     ,(100 * sum((a.price > 0)::int)) / cc.ct AS commercial
#     ,(100 * sum((a.price = 0)::int)) / cf.ct AS free
#FROM  (SELECT count(*)::float AS ct FROM applications WHERE price > 0) AS cc
#      ,(SELECT count(*)::float AS ct FROM applications WHERE price = 0) AS cf
#      ,permissions p
#LEFT   JOIN applications_permissions ap ON ap.permission_id = p.id
#LEFT   JOIN applications a ON a.id = ap.application_id
#WHERE p.regex is not Null
#GROUP  BY 1, cc.ct, cf.ct
#ORDER  BY 2 DESC, 3 DESC, 1;

    db_cursor.execute('SELECT (SELECT regex FROM permissions WHERE id = applications_permissions.permission_id) AS "regex", 100::float * COUNT(*)/(SELECT COUNT(name) FROM applications WHERE price = \'0\') AS "percent" FROM applications, applications_permissions WHERE applications.id = applications_permissions.application_id AND applications.price = \'0\' GROUP BY applications_permissions.permission_id ORDER BY percent DESC')
    freepermissions_data = db_cursor.fetchall()
    db_cursor.execute('SELECT (SELECT regex FROM permissions WHERE id = applications_permissions.permission_id) AS "regex", 100::float * COUNT(*)/(SELECT COUNT(name) FROM applications WHERE price != \'0\') AS "percent" FROM applications, applications_permissions WHERE applications.id = applications_permissions.application_id AND applications.price != \'0\' GROUP BY applications_permissions.permission_id ORDER BY percent DESC')
    paidpermissions_data = db_cursor.fetchall()

    freepermissions_names = []
    freepermissions_count = []
    paidpermissions_names = []
    paidpermissions_count = []

    for permission in freepermissions_data:
        freepermissions_names.append(str(permission[0]))
        freepermissions_count.append(int(permission[1]))

    for permisssion in paidpermissions_data:
        paidpermissions_names.append(str(permission[0]))
        paidpermissions_count.append(int(permission[1]))

    cairoplot.vertical_bar_plot ( path + 'freevspaid.svg', data = {'Free': freepermissions_count, 'Paid': paidpermissions_count},
                                  width = 8000, height = 600, border = 5,
                                  display_values = True,
                                  grid = True)


    ###
    # permissions per category
    db_cursor.execute('SELECT (SELECT regex from permissions WHERE id = permission_id) AS permission, COUNT(*) from applications_permissions GROUP BY permission_id ORDER BY count DESC')



    ####
    categories = 'a b c d e f g h'.split()
    permissions_average = [ 3, 2, 7, 9, 5, 3, 2, 4]
   
    t = [x*0.1 for x in range(0,40)]
    f = [math.exp(x) for x in t]
    g = [10*math.cos(x) for x in t]
    h = [10*math.sin(x) for x in t]
    erx = [0.1*random.random() for x in t]
    ery = [5*random.random() for x in t]
    data = {"exp" : [t,f], "cos" : [t,g]}
    series_colors = [ (1,0,0), (0,0,0), (0,0,1) ]

    cairoplot.scatter_plot ( path + 'test.svg', data = data, errory = [ery,ery], width = 800, height = 600, border = 20, 
                             axis = True, discrete = False, dots = 5, grid = True, 
                             x_title = "t", y_title = "f(t) g(t)", series_legend=True, series_colors = ["red", "blue", "orange"])


if __name__ == '__main__':
    main()