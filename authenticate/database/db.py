import sqlite3
import pandas as pd
import numpy as np
import PhQ as phq


class database:
    def __init__(self):
        """default constructor of database object"""
        self.spec_conn = sqlite3.connect(r'./database.db')
        self.name_conn = sqlite3.connect(r'./name.db')

    def readFile(self, path):
        # df = pd.read_csv(path, sep='\t', engine='python')
        tVals = []
        fVals = []
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                values = line.split('	')
                tVals.append(values[0])
                fVals.append(values[1])
        df = pd.DataFrame({'tVals': tVals, 'fVals': fVals})
        f.close
        return df

    def insert(self, key):
        name, freqVals, tVals = key.getValues()
        # store name in name database---

        # ---|
        spectrum = pd.DataFrame({'FreqVals': freqVals, 'TVals': tVals})
        nameDF = pd.DataFrame({'Names': [name]})

        spectrum.to_sql('db_spec', self.spec_conn, if_exists='append', index=False)

        # insert name to name.db
        nameDF.to_sql('db_name', self.name_conn, if_exists='append', index=False)

        return 0

    def remove(self):
        return 0

    def deviceList(self):
        """Return the list of devices
        
        Only Device is raspberry pi 4 board called 'Guadalupe'
        """
        deviceList = ['Guadalupe']
        return deviceList

    def keyList(self):
        nameDF = pd.read_sql_query("SELECT * FROM db_name", self.name_conn)
        specDF = pd.read_sql_query("SELECT * FROM db_spec", self.spec_conn)
        nameList = []
        specList = []
        freqVals = []
        tVals = []
        PhQ_list = []

        for i in range(len(nameDF['Names'])) :
            nameList.append(nameDF['Names'][i])

        i = 1
        j = 0
        while i <= int(len(specDF['TVals'])/5000) :
            while j < i*5000 :
                freqVals.append(float(specDF['FreqVals'][j]))
                tVals.append(float(specDF['TVals'][j]))
                j = j+1
            specList.append(freqVals)
            specList.append(tVals)
            i = i+1

        for i in range(len(nameList)) :
            key = phq.PhQ(nameList[i], np.asarray(specList[i]), np.asarray(specList[i+1]))
            PhQ_list.append(key)

        return PhQ_list

    def exitDB(self):
        self.spec_conn.close()
        self.name_conn.close()