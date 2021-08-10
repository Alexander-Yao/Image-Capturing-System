# -*- coding: utf-8 -*-
# __author__ = 'Yao Jia Wei'

import sqlite3


def is_exists(dbPath, qk):
    """
    Does qk exist in db
    :param dbPath:
    :param qk:
    :return:
    """
    b = False
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    sql = "select count(*) from bing where qk=?"
    cursor.execute(sql, (qk,))
    for row in cursor:
        count = row[0]
        if count>0:
            b = True
    conn.close()
    return b

def insert(dbPath, providerName, lat, lon, zoomLevel, buffer):
    """
    :param dbPath:
    :param rar:
    :return:
    """
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    print("Opened database successfully")
    val = [providerName, lat, lon, zoomLevel, sqlite3.Binary(buffer)]

    c.execute("INSERT INTO map(provider_name, lat, lon, zoom_level, picture) VALUES (?,?,?,?,?)",val)

    conn.commit()
    print("Records created successfully")
    conn.close()
    pass

def create_db(dbPath):
    """

    :param dbPath:
    :return:
    """
    conn = sqlite3.connect(dbPath)
    print("Create db successfully" + dbPath)
    conn.close()
    _create_table(dbPath)
    pass

def _create_table(dbPath):
    """

    :param dbPath:
    :return:
    """
    conn = sqlite3.connect(dbPath)
    print("Opened database successfully")
    c = conn.cursor()
    c.execute('''CREATE TABLE bing
           (qk text PRIMARY KEY     NOT NULL,
           picture         BLOB);''')
    print("Table created successfully")
    conn.commit()
    conn.close()
    pass

def save_images(dbPath, qk):
    """
    Show images
    :param dbPath:
    :param qk:
    :return:
    """
    conn = sqlite3.connect(dbPath)
    print("Opened database successfully")
    c = conn.cursor()
    cursor = c.execute("select picture from bing where qk="+ qk)

    for row in cursor:
        data = row[0]
        pic_name = 'map/bing/'+ qk + '.png'
        with open(pic_name, 'wb') as out_file:
            out_file.write(data)

    conn.close()
