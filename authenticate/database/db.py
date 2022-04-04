import sqlite3
import pandas as pd
import numpy as np
import PhQ as phq


class database:
    def __init__(self):
        """default constructor of database object"""
        self.spec_conn = sqlite3.connect(r'./database.db')
        #self.name_conn = sqlite3.connect(r'./name.db')

    def readFile(self, path):
        # df = pd.read_csv(path, sep='\t', engine='python')
        tVals = []
        fVals = []
        #try:
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                values = line.split('	')
        #catch
                # be careful about this, check for system
                if float(values[0])%2 != 1:
                    fVals.append(float(values[0]))
                    tVals.append(float(values[1]))
        df = pd.DataFrame({'tVals': tVals, 'fVals': fVals})
        f.close
        return df

    def insert(self, key):
        """Insert key variable in to the database
        
        Parameters
        ----------
        key : Phq Object
            contains the name string and lists of freqVals and tVals of the key
        """
        try:
            name, freqVals, tVals = key.getValues()
            # normalize to largest value in transmission spectrum
            maxT = np.amax(tVals)
            tVals = (1/maxT)*tVals
            spectrum = pd.DataFrame({'FreqVals': freqVals, 'TVals': tVals})
            spectrum.loc[len(spectrum.index)] = [-1.0, -1.0]
            spectrum.insert(2, 'Name', name)
            #print(spectrum)
            spectrum.to_sql('db_spec', self.spec_conn, if_exists='append', index=False)
            return True
        except:
            return False


    def remove(self, keyName):
        execution = "DELETE FROM db_spec WHERE Name = \"" + keyName + "\""
        self.spec_conn.execute(execution)

    def deviceList(self):
        """Return the list of devices
        
        Only Device is raspberry pi 4 board, arbitrarilty called 'Guadalupe'
        """
        deviceList = ['Guadalupe']
        return deviceList

    def keyList(self):
        nameDF = pd.read_sql_query("SELECT * FROM db_spec", self.spec_conn)
        #specDF = pd.read_sql_query("SELECT * FROM db_spec", self.spec_conn)
        cursor = self.spec_conn.execute("SELECT * FROM db_spec")
        nameList = []
        specList = []
        freqVals = []
        tVals = []
        PhQ_list = []

        nameList = nameDF.Name.unique()
        #print(nameList)
        #for i in range(len(specDF['Name'])) :
        #    nameList.append(specDF['Name'][i])

        for row in cursor:
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

    def clearTable(self):
        cursor = self.spec_conn.cursor()
        cursor.execute("DELETE FROM db_spec")

    def exitDB(self):
        self.spec_conn.close()
        #self.name_conn.close()
