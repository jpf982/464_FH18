import sqlite3
import pandas as pd
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
        spectrum.to_sql('db_spec', self.spec_conn, if_exists='append', index=False)



        # insert name to name.db
        name.to_sql('db_name', self.spec_conn, if_exists='append', index=False)

        

        return 0

    def remove(self):
        return 0

    def deviceList(self):
        return "Guadlupe"

    def keyList(self):
        nameDF = pd.read_sql_query("SELECT * FROM db_name", self.name_conn)
        specDF = pd.read_sql_query("SELECT * FROM db_spectra", self.spec_conn)
        PhQ_list = []
        for name, freqVals, tVals in nameDF, specDF:
            key = phq.PhQ(name, freqVals, tVals)
            PhQ_list.append(key)
        return PhQ_list

    def exitDB(self):
        self.spec_conn.close()
        self.name_conn.close()


# Load data into Pandas DataFrame
#spectra = pd.read_csv('E190909A 2p0P 0p7W 146 Pol.0.dpt', delimiter=r'\s+', header=None)
def insert():
    # Connect to SQLite database
    conn = sqlite3.connect(r'/home/pi/SeniorDesign/464_FH18/database.db')
    #conn = sqlite3.connect(r'./database.db')

    # Write the data to a sqlite table
    key.name.to_sql('db_name', conn, if_exists='append', index=False)
    spectra = [key.freqvals, key.Tvals]
    spectra.to_sql('db_spectra', conn, if_exists='append', index=False)


# Close connection to SQLite database
con.close()
