import sqlite3
import pandas as pd
import PhQ 

class database:
    def __init__(self):
        self.spec_conn = sqlite3.connect(r'./database.db')
        self.name_conn = sqlite3.connect(r'./name.db')

    def readFile(self, path):
        #df = pd.read_csv(path, sep='\t', engine='python')
        tVals = []
        fVals = []
        with open(path) as f :
            lines = f.readlines()
            for line in lines :
                line = line.replace('\n', '')
                values = line.split('	')
                tVals.append(values[0])
                fVals.append(values[1])
        df = pd.DataFrame({'tVals': tVals, 'fVals': fVals})
        f.close
        return df
        
    def insert(self, key):
        name, freqVals, tVals = key.getValues()
        #store name in name database---
        
        #---|
        spectrum = pd.DataFrame({'FreqVals': freqVals, 'TVals': tVals})
        spectrum.to_sql('trm', self.conn, if_exists='append', index=False)
        
        #insert name to name.db
        
        return 0
            
    def remove(self):
        return 0

    def deviceList(self):
        return 0

    def keyList(self):
        return 0

    def exitDB(self):
        self.spec_conn.close()
        self.name_conn.close()


# Load data into Pandas DataFrame
#spectra = pd.read_csv('E190909A 2p0P 0p7W 146 Pol.0.dpt', delimiter=r'\s+', header=None)

# Connect to SQLite database
#conn = sqlite3.connect(r'/home/pi/SeniorDesign/464_FH18/database.db')
#conn = sqlite3.connect(r'./database.db')

# Write the data to a sqlite table
#spectra.to_sql('trm', conn, if_exists='append', index=False)

# Create a cursor object
#cur = conn.cursor()
# Fetch and display result
#for row in cur.execute("SELECT * FROM trm"):
#    print(row)
# Close connection to SQLite database
#conn.close()
