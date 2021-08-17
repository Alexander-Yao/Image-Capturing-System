# -*- coding: utf-8 -*-
# __author__ = 'Yao Jia Wei'

import pymssql

class MSSQL:
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
 
    def GetConnect(self):
        if not self.db:
            raise(NameError,'No data')
        self.conn = pymssql.connect(server=self.host,user=self.user,password=self.pwd,database=self.db,charset='utf8')
        cur = self.conn.cursor()
        print("Connection Success!")
        if not cur:
            raise(NameError,'Connect Failure')
        else:
            return cur

    def inser_map(self, lat, lon, map_provider, capture_url):
        val = (lat, lon, map_provider, capture_url,'whole')
        c = self.GetConnect()
        idd = c.execute("INSERT INTO location_photos(lat,lng,map_provider,capture_url,quarter) VALUES (%s,%s,%s,%s,%s)",val)
        self.conn.commit()
        self.conn.close()
        print("Records created successfully")
        return idd

