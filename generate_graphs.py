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

    # apps_per_category
    db_cursor.execute('SELECT category, COUNT(name) from applications GROUP BY category ORDER BY count DESC')
    app_count = db_cursor.fetchall()

    app_count_names = []
    app_count_data = []

    for group in app_count:
        app_count_names.append(str(group[0]))
        app_count_data.append(int(group[1]))

    cairoplot.vertical_bar_plot ( path + 'apps_per_category.svg', app_count_data, 1200, 300, border = 20, display_values = True, grid = False, x_labels = app_count_names)



    ####
    categories = 'a b c d e f g h'.split()
    permissions_average = [ 3, 2, 7, 9, 5, 3, 2, 4]
   
    t = [x*0.1 for x in range(0,40)]
    f = [math.exp(x) for x in t]
    g = [10*math.cos(x) for x in t]
    h = [10*math.sin(x) for x in t]
    erx = [0.1*random.random() for x in t]
    ery = [5*random.random() for x in t]
    data = {"exp" : [t,f], "cos" : [t,g], "sin" : [t,h]}
    series_colors = [ (1,0,0), (0,0,0), (0,0,1) ]

    cairoplot.scatter_plot ( path + 'test.svg', data = data, errory = [ery,ery], width = 800, height = 600, border = 20, 
                             axis = True, discrete = False, dots = 5, grid = True, 
                             x_title = "t", y_title = "f(t) g(t)", series_legend=True, series_colors = ["red", "blue", "orange"])


if __name__ == '__main__':
    main()