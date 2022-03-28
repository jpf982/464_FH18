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
                # be careful about this, check for system
                if values[0]%2 != 1:
                    fVals.append(float(values[0]))
                    tVals.append(float(values[1]))
        df = pd.DataFrame({'tVals': tVals, 'fVals': fVals})
        f.close
        return df

    def insert(self, key):
        name, freqVals, tVals = key.getValues()
        # store name in name database---

        # ---|
        spectrum = pd.DataFrame({'FreqVals': freqVals, 'TVals': tVals})
        spectrum.loc[len(spectrum.index)] = [-1.0, -1.0]
        print(spectrum)
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
        #specDF = pd.read_sql_query("SELECT * FROM db_spec", self.spec_conn)
        specDF = self.spec_conn.execute("SELECT * FROM db_spec")
        nameList = []
        specList = []
        freqVals = []
        tVals = []
        PhQ_list = []

        for i in range(len(nameDF['Names'])) :
            nameList.append(nameDF['Names'][i])

        for row in specDF:
            if row[0] != -1.0 :
                tVals.append(row[1])
                freqVals.append(row[0])
            else :
                specList.append(freqVals)
                specList.append(tVals)
                freqVals = []
                tVals = []

        for i in range(len(nameList)) :
            key = phq.PhQ(nameList[i], np.asarray(specList[i*2]), np.asarray(specList[(i*2)+1]))
            PhQ_list.append(key)

        return PhQ_list

    def exitDB(self):
        self.spec_conn.close()
        self.name_conn.close()
